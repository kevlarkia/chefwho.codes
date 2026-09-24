import { NextResponse } from "next/server";
import { stripe, mapStripeErrorToResponse } from "@/lib/stripe";
import type { USBankAccount } from "@/lib/types/stripe-bank-account";

type RouteContext = {
  params: Promise<{ id: string }>;
};

type ConfirmMicrodepositsRequest = {
  amounts?: [number, number];
  descriptor_code?: string;
};

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

  let payload: Partial<ConfirmMicrodepositsRequest>;

  try {
    payload = (await request.json()) as Partial<ConfirmMicrodepositsRequest>;
  } catch {
    return NextResponse.json(
      { error: "Invalid JSON body." },
      { status: 400 },
    );
  }

  if (!payload.amounts && !payload.descriptor_code) {
    return NextResponse.json(
      { error: "Either amounts or descriptor_code must be provided." },
      { status: 400 },
    );
  }

  if (payload.amounts) {
    if (
      !Array.isArray(payload.amounts) ||
      payload.amounts.length !== 2 ||
      !payload.amounts.every((amount) => typeof amount === "number" && amount > 0 && amount < 100)
    ) {
      return NextResponse.json(
        { error: "Amounts must be an array of two positive numbers less than 100." },
        { status: 400 },
      );
    }
  }

  try {
    const bankAccount = await stripe.v2.core.vault.usBankAccounts.confirmMicrodeposits(
      id,
      payload,
    );

    return NextResponse.json({
      ok: true,
      data: bankAccount as unknown as USBankAccount,
      message: "Bank account verified successfully.",
    });
  } catch (error) {
    console.error("Failed to confirm microdeposits", {
      error,
      id,
      timestamp: new Date().toISOString(),
    });

    const errorResponse = mapStripeErrorToResponse(error);
    return NextResponse.json(errorResponse, { status: 400 });
  }
}
