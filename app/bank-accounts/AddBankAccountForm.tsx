"use client";

import { useState } from "react";
import type { CreateBankAccountRequest } from "@/lib/types/stripe-bank-account";

type AddBankAccountFormProps = {
  onSuccess: () => void;
};

export default function AddBankAccountForm({ onSuccess }: AddBankAccountFormProps) {
  const [formData, setFormData] = useState<Partial<CreateBankAccountRequest>>({
    account_holder_name: "",
    account_holder_type: "individual",
    account_number: "",
    routing_number: "",
    account_type: "checking",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setError(null);
  };

  const validateForm = (): string | null => {
    if (!formData.account_holder_name || formData.account_holder_name.trim().length < 2) {
      return "Account holder name must be at least 2 characters long.";
    }

    if (!formData.routing_number || !/^\d{9}$/.test(formData.routing_number)) {
      return "Routing number must be exactly 9 digits.";
    }

    if (!formData.account_number || !/^\d{4,17}$/.test(formData.account_number)) {
      return "Account number must be between 4 and 17 digits.";
    }

    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await fetch("/api/bank-accounts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to add bank account");
      }

      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const inputStyle: React.CSSProperties = {
    width: "100%",
    padding: "0.75rem",
    border: "1px solid #d1d5db",
    borderRadius: "0.375rem",
    fontSize: "1rem",
  };

  const labelStyle: React.CSSProperties = {
    display: "block",
    marginBottom: "0.5rem",
    fontWeight: "500",
    fontSize: "0.875rem",
    color: "#374151",
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <div style={{
          backgroundColor: "#fee2e2",
          border: "1px solid #ef4444",
          color: "#991b1b",
          padding: "0.75rem",
          borderRadius: "0.375rem",
          marginBottom: "1rem",
          fontSize: "0.875rem",
        }}>
          {error}
        </div>
      )}

      <div style={{ display: "grid", gap: "1.5rem" }}>
        <div>
          <label htmlFor="account_holder_name" style={labelStyle}>
            Account Holder Name *
          </label>
          <input
            type="text"
            id="account_holder_name"
            name="account_holder_name"
            value={formData.account_holder_name}
            onChange={handleChange}
            required
            style={inputStyle}
            placeholder="John Doe"
          />
        </div>

        <div>
          <label htmlFor="account_holder_type" style={labelStyle}>
            Account Holder Type *
          </label>
          <select
            id="account_holder_type"
            name="account_holder_type"
            value={formData.account_holder_type}
            onChange={handleChange}
            required
            style={inputStyle}
          >
            <option value="individual">Individual</option>
            <option value="company">Company</option>
          </select>
        </div>

        <div>
          <label htmlFor="account_type" style={labelStyle}>
            Account Type *
          </label>
          <select
            id="account_type"
            name="account_type"
            value={formData.account_type}
            onChange={handleChange}
            required
            style={inputStyle}
          >
            <option value="checking">Checking</option>
            <option value="savings">Savings</option>
          </select>
        </div>

        <div>
          <label htmlFor="routing_number" style={labelStyle}>
            Routing Number *
          </label>
          <input
            type="text"
            id="routing_number"
            name="routing_number"
            value={formData.routing_number}
            onChange={handleChange}
            required
            pattern="\d{9}"
            maxLength={9}
            style={inputStyle}
            placeholder="110000000"
          />
          <p style={{ fontSize: "0.75rem", color: "#666", marginTop: "0.25rem" }}>
            9-digit routing number
          </p>
        </div>

        <div>
          <label htmlFor="account_number" style={labelStyle}>
            Account Number *
          </label>
          <input
            type="text"
            id="account_number"
            name="account_number"
            value={formData.account_number}
            onChange={handleChange}
            required
            pattern="\d{4,17}"
            maxLength={17}
            style={inputStyle}
            placeholder="000123456789"
          />
          <p style={{ fontSize: "0.75rem", color: "#666", marginTop: "0.25rem" }}>
            4-17 digit account number
          </p>
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "0.75rem 1.5rem",
            backgroundColor: loading ? "#9ca3af" : "#0070f3",
            color: "white",
            border: "none",
            borderRadius: "0.5rem",
            fontSize: "1rem",
            cursor: loading ? "not-allowed" : "pointer",
            fontWeight: "500",
          }}
        >
          {loading ? "Adding Bank Account..." : "Add Bank Account"}
        </button>
      </div>
    </form>
  );
}
