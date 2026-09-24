import { NextResponse } from "next/server";
import { stripe, mapStripeErrorToResponse } from "@/lib/stripe";

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
    const customers = await stripe.customers.list({ limit: 100 });
    
    for (const customer of customers.data) {
      try {
        await stripe.customers.deleteSource(customer.id, id);

        return NextResponse.json({
          ok: true,
          data: { id, deleted: true },
          message: "Bank account archived successfully.",
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
    console.error("Failed to archive US bank account", {
      error,
      id,
      timestamp: new Date().toISOString(),
    });

    const errorResponse = mapStripeErrorToResponse(error);
    return NextResponse.json(errorResponse, { status: 400 });
  }
}
