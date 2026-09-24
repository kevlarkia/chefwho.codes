export type AccountHolderType = "individual" | "company";

export type VerificationStatus = 
  | "new"
  | "verified"
  | "verification_failed"
  | "errored";

export type USBankAccount = {
  id: string;
  object: "us_bank_account";
  account_holder_name: string;
  account_holder_type: AccountHolderType;
  account_type: string;
  bank_name: string | null;
  country: string;
  currency: string;
  fingerprint: string;
  last4: string;
  routing_number: string;
  status: VerificationStatus;
  created: number;
  livemode: boolean;
  metadata: Record<string, string>;
};

export type CreateBankAccountRequest = {
  account_holder_name: string;
  account_holder_type: AccountHolderType;
  account_number: string;
  routing_number: string;
  account_type?: "checking" | "savings";
  metadata?: Record<string, string>;
};

export type UpdateBankAccountRequest = {
  account_holder_name?: string;
  account_holder_type?: AccountHolderType;
  metadata?: Record<string, string>;
};

export type ListBankAccountsResponse = {
  object: "list";
  data: USBankAccount[];
  has_more: boolean;
  url: string;
};

export type VerificationRequest = {
  verification_method?: "instant" | "microdeposits";
};

export type StripeErrorResponse = {
  error: {
    type: string;
    code?: string;
    message: string;
    param?: string;
  };
};

export type APIErrorResponse = {
  error: string;
  code?: string;
  param?: string;
};

export type APISuccessResponse<T> = {
  ok: true;
  data: T;
};
