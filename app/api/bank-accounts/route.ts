import { NextResponse } from "next/server";
import Stripe from "stripe";
import { stripe, mapStripeErrorToResponse } from "@/lib/stripe";
import type {
  CreateBankAccountRequest,
  USBankAccount,
  ListBankAccountsResponse,
} from "@/lib/types/stripe-bank-account";

function validateRoutingNumber(routingNumber: string): boolean {
  return /^\d{9}$/.test(routingNumber);
}

function validateAccountNumber(accountNumber: string): boolean {
  return /^\d{4,17}$/.test(accountNumber);
}

function normalizeString(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

export async function POST(request: Request) {
  let payload: Partial<CreateBankAccountRequest>;

  try {
    payload = (await request.json()) as Partial<CreateBankAccountRequest>;
  } catch {
    return NextResponse.json(
      { error: "Invalid JSON body." },
      { status: 400 },
    );
  }

  const accountHolderName = normalizeString(payload.account_holder_name);
  const accountHolderType = payload.account_holder_type;
  const accountNumber = normalizeString(payload.account_number);
  const routingNumber = normalizeString(payload.routing_number);

  if (accountHolderName.length < 2) {
    return NextResponse.json(
      { error: "Account holder name must be at least 2 characters long." },
      { status: 400 },
    );
  }

  if (accountHolderType !== "individual" && accountHolderType !== "company") {
    return NextResponse.json(
      { error: "Account holder type must be 'individual' or 'company'." },
      { status: 400 },
    );
  }

  if (!validateRoutingNumber(routingNumber)) {
    return NextResponse.json(
      { error: "Routing number must be exactly 9 digits." },
      { status: 400 },
    );
  }

  if (!validateAccountNumber(accountNumber)) {
    return NextResponse.json(
      { error: "Account number must be between 4 and 17 digits." },
      { status: 400 },
    );
  }

  try {
    const token = await stripe.tokens.create({
      bank_account: {
        country: "US",
        currency: "usd",
        account_holder_name: accountHolderName,
        account_holder_type: accountHolderType,
        account_number: accountNumber,
        routing_number: routingNumber,
      },
    });

    const customer = await stripe.customers.create({
      metadata: payload.metadata || {},
    });

    const bankAccount = await stripe.customers.createSource(customer.id, {
      source: token.id,
    }) as Stripe.BankAccount;

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
  } catch (error) {
    console.error("Failed to create US bank account", {
      error,
      timestamp: new Date().toISOString(),
    });

    const errorResponse = mapStripeErrorToResponse(error);
    return NextResponse.json(errorResponse, { status: 400 });
  }
}

export async function GET() {
  const limit = 10;

  try {
    const customers = await stripe.customers.list({ limit: 100 });
    const allBankAccounts: USBankAccount[] = [];

    for (const customer of customers.data) {
      const sources = await stripe.customers.listSources(customer.id, {
        object: "bank_account",
        limit: 100,
      });

      for (const source of sources.data) {
        const bankAccount = source as Stripe.BankAccount;
        allBankAccounts.push({
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
        });
      }
    }

    const response: ListBankAccountsResponse = {
      object: "list",
      data: allBankAccounts.slice(0, limit),
      has_more: allBankAccounts.length > limit,
      url: "/api/bank-accounts",
    };

    return NextResponse.json({
      ok: true,
      data: response,
    });
  } catch (error) {
    console.error("Failed to list US bank accounts", {
      error,
      timestamp: new Date().toISOString(),
    });

    const errorResponse = mapStripeErrorToResponse(error);
    return NextResponse.json(errorResponse, { status: 400 });
  }
}
