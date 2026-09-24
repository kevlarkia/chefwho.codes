import { NextResponse } from "next/server";
import Stripe from "stripe";
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
    const customers = await stripe.customers.list({ limit: 100 });
    
    for (const customer of customers.data) {
      try {
        await stripe.customers.retrieveSource(
          customer.id,
          id,
        );

        const verifiedBankAccount = await stripe.customers.verifySource(
          customer.id,
          id,
          {
            amounts: payload.amounts,
          },
        ) as Stripe.BankAccount;

        const response: USBankAccount = {
          id: verifiedBankAccount.id,
          object: "us_bank_account",
          account_holder_name: verifiedBankAccount.account_holder_name || "",
          account_holder_type: (verifiedBankAccount.account_holder_type || "individual") as "individual" | "company",
          account_type: verifiedBankAccount.account_type || "checking",
          bank_name: verifiedBankAccount.bank_name || null,
          country: verifiedBankAccount.country,
          currency: verifiedBankAccount.currency,
          fingerprint: verifiedBankAccount.fingerprint || "",
          last4: verifiedBankAccount.last4,
          routing_number: verifiedBankAccount.routing_number || "",
          status: verifiedBankAccount.status as "new" | "verified" | "verification_failed" | "errored",
          created: Math.floor(Date.now() / 1000),
          livemode: false,
          metadata: { customer_id: customer.id },
        };

        return NextResponse.json({
          ok: true,
          data: response,
          message: "Bank account verified successfully.",
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
    console.error("Failed to confirm microdeposits", {
      error,
      id,
      timestamp: new Date().toISOString(),
    });

    const errorResponse = mapStripeErrorToResponse(error);
    return NextResponse.json(errorResponse, { status: 400 });
  }
}
