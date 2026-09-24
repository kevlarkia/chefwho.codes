import { NextResponse } from "next/server";
import { stripe, mapStripeErrorToResponse } from "@/lib/stripe";
import type { USBankAccount } from "@/lib/types/stripe-bank-account";

type RouteContext = {
  params: Promise<{ id: string }>;
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

  try {
    const bankAccount = await stripe.v2.core.vault.usBankAccounts.archive(id);

    return NextResponse.json({
      ok: true,
      data: bankAccount as unknown as USBankAccount,
      message: "Bank account archived successfully.",
    });
  } catch (error) {
    console.error("Failed to archive US bank account", {
      error,
      id,
      timestamp: new Date().toISOString(),
    });

    const errorResponse = mapStripeErrorToResponse(error);
    return NextResponse.json(errorResponse, { status: 400 });
  }
}
