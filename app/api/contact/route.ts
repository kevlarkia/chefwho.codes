import { NextResponse } from "next/server";

type ContactPayload = {
  name?: unknown;
  email?: unknown;
  message?: unknown;
};

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const DEFAULT_RATE_LIMIT_WINDOW_SECONDS = 60;
const DEFAULT_RATE_LIMIT_MAX_REQUESTS = 5;

type RateLimitEntry = {
  count: number;
  resetAt: number;
};

const rateLimitStore = new Map<string, RateLimitEntry>();

function normalizeString(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function normalizePositiveNumber(value: string | undefined, fallback: number): number {
  const parsed = Number(value);

  if (!Number.isFinite(parsed) || parsed <= 0) {
    return fallback;
  }

  return Math.floor(parsed);
}

function getClientIp(request: Request): string {
  const forwardedFor = request.headers.get("x-forwarded-for");

  if (forwardedFor) {
    return forwardedFor.split(",")[0]?.trim() || "unknown";
  }

  const realIp = request.headers.get("x-real-ip");
  return realIp?.trim() || "unknown";
}

function checkRateLimit(clientIp: string): {
  limited: boolean;
  retryAfterSeconds: number;
} {
  const now = Date.now();
  const windowSeconds = normalizePositiveNumber(
    process.env.CONTACT_RATE_LIMIT_WINDOW_SECONDS,
    DEFAULT_RATE_LIMIT_WINDOW_SECONDS,
  );
  const maxRequests = normalizePositiveNumber(
    process.env.CONTACT_RATE_LIMIT_MAX_REQUESTS,
    DEFAULT_RATE_LIMIT_MAX_REQUESTS,
  );

  const windowMs = windowSeconds * 1000;
  const existing = rateLimitStore.get(clientIp);

  if (!existing || existing.resetAt <= now) {
    rateLimitStore.set(clientIp, {
      count: 1,
      resetAt: now + windowMs,
    });

    return {
      limited: false,
      retryAfterSeconds: windowSeconds,
    };
  }

  if (existing.count >= maxRequests) {
    return {
      limited: true,
      retryAfterSeconds: Math.max(1, Math.ceil((existing.resetAt - now) / 1000)),
    };
  }

  existing.count += 1;
  rateLimitStore.set(clientIp, existing);

  return {
    limited: false,
    retryAfterSeconds: Math.max(1, Math.ceil((existing.resetAt - now) / 1000)),
  };
}

async function deliverThroughSendGrid(params: {
  name: string;
  email: string;
  message: string;
  recipient: string;
  sender: string;
}) {
  const response = await fetch("https://api.sendgrid.com/v3/mail/send", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.CONTACT_SENDGRID_API_KEY}`,
    },
    body: JSON.stringify({
      personalizations: [
        {
          to: [{ email: params.recipient }],
          subject: `New contact message from ${params.name}`,
        },
      ],
      from: { email: params.sender, name: "chefwho.codes Contact Form" },
      reply_to: { email: params.email, name: params.name },
      content: [
        {
          type: "text/plain",
          value: [
            `Name: ${params.name}`,
            `Email: ${params.email}`,
            "",
            "Message:",
            params.message,
          ].join("\n"),
        },
      ],
    }),
  });

  if (!response.ok) {
    const responseBody = await response.text();
    throw new Error(`SendGrid request failed (${response.status}): ${responseBody}`);
  }
}

export async function POST(request: Request) {
  const clientIp = getClientIp(request);
  const rateLimit = checkRateLimit(clientIp);

  if (rateLimit.limited) {
    return NextResponse.json(
      {
        error:
          "Too many requests from this IP. Please wait a minute before trying again.",
      },
      {
        status: 429,
        headers: {
          "Retry-After": String(rateLimit.retryAfterSeconds),
        },
      },
    );
  }

  let payload: ContactPayload;

  try {
    payload = (await request.json()) as ContactPayload;
  } catch {
    return NextResponse.json(
      { error: "Invalid JSON body." },
      { status: 400 },
    );
  }

  const name = normalizeString(payload.name);
  const email = normalizeString(payload.email).toLowerCase();
  const message = normalizeString(payload.message);

  if (name.length < 2) {
    return NextResponse.json(
      { error: "Please provide your name (at least 2 characters)." },
      { status: 400 },
    );
  }

  if (!EMAIL_REGEX.test(email)) {
    return NextResponse.json(
      { error: "Please provide a valid email address." },
      { status: 400 },
    );
  }

  if (message.length < 20) {
    return NextResponse.json(
      { error: "Message should be at least 20 characters long." },
      { status: 400 },
    );
  }

  if (message.length > 4000) {
    return NextResponse.json(
      { error: "Message is too long. Please keep it under 4000 characters." },
      { status: 400 },
    );
  }

  const recipientEmail = normalizeString(process.env.CONTACT_EMAIL_TO);
  const senderEmail =
    normalizeString(process.env.CONTACT_EMAIL_FROM) || "no-reply@chefwho.codes";
  const hasSendGridConfig =
    Boolean(normalizeString(process.env.CONTACT_SENDGRID_API_KEY)) &&
    recipientEmail.length > 0;

  if (hasSendGridConfig) {
    try {
      await deliverThroughSendGrid({
        name,
        email,
        message,
        recipient: recipientEmail,
        sender: senderEmail,
      });
    } catch (error) {
      console.error("Failed to deliver contact submission via SendGrid", {
        error,
        receivedAt: new Date().toISOString(),
      });

      return NextResponse.json(
        {
          error: "Unable to send your message right now. Please try again later.",
        },
        { status: 502 },
      );
    }
  }

  // Fallback behavior for local/staging when an outbound provider isn't configured.
  console.info("New contact submission", {
    name,
    email,
    message,
    delivery: hasSendGridConfig ? "sendgrid" : "log-only",
    recipientEmail: recipientEmail || null,
    senderEmail,
    receivedAt: new Date().toISOString(),
  });

  return NextResponse.json({
    ok: true,
    message: "Thanks for reaching out. I will get back to you soon.",
  });
}
