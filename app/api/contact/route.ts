import { NextResponse } from "next/server";

type ContactPayload = {
  name?: unknown;
  email?: unknown;
  message?: unknown;
};

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function normalizeString(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

export async function POST(request: Request) {
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

  // Placeholder behavior for now: log to server output.
  // Replace with email provider / CRM integration for production use.
  console.info("New contact submission", {
    name,
    email,
    message,
    receivedAt: new Date().toISOString(),
  });

  return NextResponse.json({
    ok: true,
    message: "Thanks for reaching out. I will get back to you soon.",
  });
}
