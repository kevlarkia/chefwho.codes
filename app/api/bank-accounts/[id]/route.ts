import { NextResponse } from "next/server";
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
    const bankAccount = await stripe.v2.core.vault.usBankAccounts.retrieve(id);

    return NextResponse.json({
      ok: true,
      data: bankAccount as unknown as USBankAccount,
    });
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
    const bankAccount = await stripe.v2.core.vault.usBankAccounts.update(
      id,
      updateData,
    );

    return NextResponse.json({
      ok: true,
      data: bankAccount as unknown as USBankAccount,
    });
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
