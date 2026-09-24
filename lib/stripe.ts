import Stripe from "stripe";

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error(
    "Missing STRIPE_SECRET_KEY environment variable. Please add it to your .env file.",
  );
}

const apiVersion = (process.env.STRIPE_API_VERSION || "2026-08-26.preview") as Stripe.LatestApiVersion;

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion,
  typescript: true,
});

export function isStripeError(error: unknown): error is Stripe.StripeError {
  return (
    typeof error === "object" &&
    error !== null &&
    "type" in error &&
    typeof (error as Stripe.StripeError).type === "string"
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
