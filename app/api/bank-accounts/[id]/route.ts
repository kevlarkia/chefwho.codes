import { NextResponse } from "next/server";
import Stripe from "stripe";
import { stripe, mapStripeErrorToResponse } from "@/lib/stripe";
import type {
  UpdateBankAccountRequest,
  USBankAccount,
} from "@/lib/types/stripe-bank-account";

type RouteContext = {
  params: Promise<{ id: string }>;
};

function normalizeString(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

export async function GET(
  request: Request,
  context: RouteContext,
) {
  const { id } = await context.params;

  if (!id || typeof id !== "string") {
    return NextResponse.json(
      { error: "Invalid bank account ID." },
      { status: 400 },
    );
  }

  try {
    const customers = await stripe.customers.list({ limit: 100 });
    
    for (const customer of customers.data) {
      try {
        const bankAccount = await stripe.customers.retrieveSource(
          customer.id,
          id,
        ) as Stripe.BankAccount;

        const response: USBankAccount = {
          id: bankAccount.id,
          object: "us_bank_account",
          account_holder_name: bankAccount.account_holder_name || "",
          account_holder_type: (bankAccount.account_holder_type || "individual") as "individual" | "company",
          account_type: bankAccount.account_type || "checking",
          bank_name: bankAccount.bank_name || null,
          country: bankAccount.country,
          currency: bankAccount.currency,
          fingerprint: bankAccount.fingerprint || "",
          last4: bankAccount.last4,
          routing_number: bankAccount.routing_number || "",
          status: bankAccount.status as "new" | "verified" | "verification_failed" | "errored",
          created: Math.floor(Date.now() / 1000),
          livemode: false,
          metadata: { customer_id: customer.id },
        };

        return NextResponse.json({
          ok: true,
          data: response,
        });
      } catch {
        continue;
      }
    }

    return NextResponse.json(
      { error: "Bank account not found." },
      { status: 404 },
    );
  } catch (error) {
    console.error("Failed to retrieve US bank account", {
      error,
      id,
      timestamp: new Date().toISOString(),
    });

    const errorResponse = mapStripeErrorToResponse(error);
    return NextResponse.json(errorResponse, { status: 400 });
  }
}

export async function POST(
  request: Request,
  context: RouteContext,
) {
  const { id } = await context.params;

  if (!id || typeof id !== "string") {
    return NextResponse.json(
      { error: "Invalid bank account ID." },
      { status: 400 },
    );
  }

  let payload: Partial<UpdateBankAccountRequest>;

  try {
    payload = (await request.json()) as Partial<UpdateBankAccountRequest>;
  } catch {
    return NextResponse.json(
      { error: "Invalid JSON body." },
      { status: 400 },
    );
  }

  const updateData: UpdateBankAccountRequest = {};

  if (payload.account_holder_name) {
    const accountHolderName = normalizeString(payload.account_holder_name);
    if (accountHolderName.length < 2) {
      return NextResponse.json(
        { error: "Account holder name must be at least 2 characters long." },
        { status: 400 },
      );
    }
    updateData.account_holder_name = accountHolderName;
  }

  if (payload.account_holder_type) {
    if (
      payload.account_holder_type !== "individual" &&
      payload.account_holder_type !== "company"
    ) {
      return NextResponse.json(
        { error: "Account holder type must be 'individual' or 'company'." },
        { status: 400 },
      );
    }
    updateData.account_holder_type = payload.account_holder_type;
  }

  if (payload.metadata) {
    updateData.metadata = payload.metadata;
  }

  try {
    const customers = await stripe.customers.list({ limit: 100 });
    
    for (const customer of customers.data) {
      try {
        await stripe.customers.retrieveSource(
          customer.id,
          id,
        );

        const bankAccount = await stripe.customers.updateSource(
          customer.id,
          id,
          {
            account_holder_name: updateData.account_holder_name,
            account_holder_type: updateData.account_holder_type,
            metadata: updateData.metadata,
          },
        ) as Stripe.BankAccount;

        const response: USBankAccount = {
          id: bankAccount.id,
          object: "us_bank_account",
          account_holder_name: bankAccount.account_holder_name || "",
          account_holder_type: (bankAccount.account_holder_type || "individual") as "individual" | "company",
          account_type: bankAccount.account_type || "checking",
          bank_name: bankAccount.bank_name || null,
          country: bankAccount.country,
          currency: bankAccount.currency,
          fingerprint: bankAccount.fingerprint || "",
          last4: bankAccount.last4,
          routing_number: bankAccount.routing_number || "",
          status: bankAccount.status as "new" | "verified" | "verification_failed" | "errored",
          created: Math.floor(Date.now() / 1000),
          livemode: false,
          metadata: { customer_id: customer.id },
        };

        return NextResponse.json({
          ok: true,
          data: response,
        });
      } catch {
        continue;
      }
    }

    return NextResponse.json(
      { error: "Bank account not found." },
      { status: 404 },
    );
  } catch (error) {
    console.error("Failed to update US bank account", {
      error,
      id,
      timestamp: new Date().toISOString(),
    });

    const errorResponse = mapStripeErrorToResponse(error);
    return NextResponse.json(errorResponse, { status: 400 });
  }
}
