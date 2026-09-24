import Stripe from "stripe";

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error(
    "Missing STRIPE_SECRET_KEY environment variable. Please add it to your .env file.",
  );
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2026-08-26.dahlia",
  typescript: true,
});

export function isStripeError(error: unknown): error is Stripe.errors.StripeError {
  return (
    typeof error === "object" &&
    error !== null &&
    "type" in error &&
    typeof (error as { type: string }).type === "string"
  );
}

export function getStripeErrorMessage(error: unknown): string {
  if (isStripeError(error)) {
    return error.message || "An error occurred with Stripe.";
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "An unexpected error occurred.";
}

export function mapStripeErrorToResponse(error: unknown): {
  error: string;
  code?: string;
  param?: string;
} {
  if (isStripeError(error)) {
    return {
      error: error.message || "An error occurred with Stripe.",
      code: error.code,
      param: error.param,
    };
  }

  if (error instanceof Error) {
    return {
      error: error.message,
    };
  }

  return {
    error: "An unexpected error occurred.",
  };
}
