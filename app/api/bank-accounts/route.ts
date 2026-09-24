import { NextResponse } from "next/server";
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
  const accountType = payload.account_type || "checking";

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
    const bankAccount = await stripe.v2.core.vault.usBankAccounts.create({
      account_holder_name: accountHolderName,
      account_holder_type: accountHolderType,
      account_number: accountNumber,
      routing_number: routingNumber,
      account_type: accountType,
      metadata: payload.metadata || {},
    });

    return NextResponse.json({
      ok: true,
      data: bankAccount as unknown as USBankAccount,
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

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const limit = Math.min(
    parseInt(searchParams.get("limit") || "10", 10),
    100,
  );
  const startingAfter = searchParams.get("starting_after") || undefined;

  try {
    const bankAccounts = await stripe.v2.core.vault.usBankAccounts.list({
      limit,
      starting_after: startingAfter,
    });

    return NextResponse.json({
      ok: true,
      data: bankAccounts as unknown as ListBankAccountsResponse,
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
