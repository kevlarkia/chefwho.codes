"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import type { USBankAccount } from "@/lib/types/stripe-bank-account";
import Link from "next/link";

export default function BankAccountDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [account, setAccount] = useState<USBankAccount | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [archiving, setArchiving] = useState(false);
  const [sendingMicrodeposits, setSendingMicrodeposits] = useState(false);
  const [confirmingMicrodeposits, setConfirmingMicrodeposits] = useState(false);
  const [microdepositAmounts, setMicrodepositAmounts] = useState({ amount1: "", amount2: "" });

  useEffect(() => {
    fetchAccount();
  }, [id]);

  const fetchAccount = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`/api/bank-accounts/${id}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to fetch bank account");
      }

      setAccount(data.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleArchive = async () => {
    if (!confirm("Are you sure you want to archive this bank account?")) {
      return;
    }

    try {
      setArchiving(true);
      const response = await fetch(`/api/bank-accounts/${id}/archive`, {
        method: "POST",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to archive bank account");
      }

      router.push("/bank-accounts");
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to archive bank account");
    } finally {
      setArchiving(false);
    }
  };

  const handleSendMicrodeposits = async () => {
    try {
      setSendingMicrodeposits(true);
      const response = await fetch(`/api/bank-accounts/${id}/send-microdeposits`, {
        method: "POST",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to send microdeposits");
      }

      alert(data.message || "Microdeposits sent successfully!");
      await fetchAccount();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to send microdeposits");
    } finally {
      setSendingMicrodeposits(false);
    }
  };

  const handleConfirmMicrodeposits = async () => {
    const amount1 = parseInt(microdepositAmounts.amount1, 10);
    const amount2 = parseInt(microdepositAmounts.amount2, 10);

    if (isNaN(amount1) || isNaN(amount2) || amount1 <= 0 || amount2 <= 0) {
      alert("Please enter valid amounts");
      return;
    }

    try {
      setConfirmingMicrodeposits(true);
      const response = await fetch(`/api/bank-accounts/${id}/confirm-microdeposits`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amounts: [amount1, amount2] }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to confirm microdeposits");
      }

      alert(data.message || "Bank account verified successfully!");
      setMicrodepositAmounts({ amount1: "", amount2: "" });
      await fetchAccount();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to confirm microdeposits");
    } finally {
      setConfirmingMicrodeposits(false);
    }
  };

  if (loading) {
    return (
      <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem" }}>
        <div style={{ textAlign: "center", padding: "3rem", color: "#666" }}>
          Loading bank account...
        </div>
      </div>
    );
  }

  if (error || !account) {
    return (
      <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem" }}>
        <div style={{
          backgroundColor: "#fee2e2",
          border: "1px solid #ef4444",
          color: "#991b1b",
          padding: "1rem",
          borderRadius: "0.5rem",
        }}>
          <strong>Error:</strong> {error || "Account not found"}
        </div>
        <Link
          href="/bank-accounts"
          style={{
            display: "inline-block",
            marginTop: "1rem",
            color: "#0070f3",
            textDecoration: "none",
          }}
        >
          ← Back to Bank Accounts
        </Link>
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    const styles: Record<string, React.CSSProperties> = {
      verified: {
        backgroundColor: "#10b981",
        color: "white",
        padding: "0.5rem 1rem",
        borderRadius: "9999px",
        fontSize: "0.875rem",
        fontWeight: "600",
      },
      new: {
        backgroundColor: "#f59e0b",
        color: "white",
        padding: "0.5rem 1rem",
        borderRadius: "9999px",
        fontSize: "0.875rem",
        fontWeight: "600",
      },
      verification_failed: {
        backgroundColor: "#ef4444",
        color: "white",
        padding: "0.5rem 1rem",
        borderRadius: "9999px",
        fontSize: "0.875rem",
        fontWeight: "600",
      },
      errored: {
        backgroundColor: "#ef4444",
        color: "white",
        padding: "0.5rem 1rem",
        borderRadius: "9999px",
        fontSize: "0.875rem",
        fontWeight: "600",
      },
    };

    return (
      <span style={styles[status] || styles.new}>
        {status.replace(/_/g, " ").toUpperCase()}
      </span>
    );
  };

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem" }}>
      <Link
        href="/bank-accounts"
        style={{
          display: "inline-block",
          marginBottom: "1rem",
          color: "#0070f3",
          textDecoration: "none",
        }}
      >
        ← Back to Bank Accounts
      </Link>

      <div style={{
        backgroundColor: "white",
        border: "1px solid #e5e7eb",
        borderRadius: "0.5rem",
        padding: "2rem",
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: "2rem" }}>
          <div>
            <h1 style={{ fontSize: "2rem", fontWeight: "bold", margin: "0 0 0.5rem 0" }}>
              {account.bank_name || "Unknown Bank"}
            </h1>
            {getStatusBadge(account.status)}
          </div>
        </div>

        <div style={{ display: "grid", gap: "1rem", marginBottom: "2rem" }}>
          <div>
            <h3 style={{ fontSize: "0.875rem", color: "#666", margin: "0 0 0.25rem 0", fontWeight: "600" }}>
              Account ID
            </h3>
            <p style={{ margin: 0, fontFamily: "monospace", fontSize: "0.875rem" }}>{account.id}</p>
          </div>

          <div>
            <h3 style={{ fontSize: "0.875rem", color: "#666", margin: "0 0 0.25rem 0", fontWeight: "600" }}>
              Account Holder Name
            </h3>
            <p style={{ margin: 0 }}>{account.account_holder_name}</p>
          </div>

          <div>
            <h3 style={{ fontSize: "0.875rem", color: "#666", margin: "0 0 0.25rem 0", fontWeight: "600" }}>
              Account Holder Type
            </h3>
            <p style={{ margin: 0, textTransform: "capitalize" }}>{account.account_holder_type}</p>
          </div>

          <div>
            <h3 style={{ fontSize: "0.875rem", color: "#666", margin: "0 0 0.25rem 0", fontWeight: "600" }}>
              Account Type
            </h3>
            <p style={{ margin: 0, textTransform: "capitalize" }}>{account.account_type}</p>
          </div>

          <div>
            <h3 style={{ fontSize: "0.875rem", color: "#666", margin: "0 0 0.25rem 0", fontWeight: "600" }}>
              Routing Number
            </h3>
            <p style={{ margin: 0, fontFamily: "monospace" }}>{account.routing_number}</p>
          </div>

          <div>
            <h3 style={{ fontSize: "0.875rem", color: "#666", margin: "0 0 0.25rem 0", fontWeight: "600" }}>
              Account Number (Last 4)
            </h3>
            <p style={{ margin: 0, fontFamily: "monospace" }}>••••{account.last4}</p>
          </div>

          <div>
            <h3 style={{ fontSize: "0.875rem", color: "#666", margin: "0 0 0.25rem 0", fontWeight: "600" }}>
              Country / Currency
            </h3>
            <p style={{ margin: 0 }}>{account.country} / {account.currency.toUpperCase()}</p>
          </div>

          <div>
            <h3 style={{ fontSize: "0.875rem", color: "#666", margin: "0 0 0.25rem 0", fontWeight: "600" }}>
              Created
            </h3>
            <p style={{ margin: 0 }}>{new Date(account.created * 1000).toLocaleString()}</p>
          </div>
        </div>

        {account.status === "new" && (
          <div style={{
            backgroundColor: "#fffbeb",
            border: "1px solid #fbbf24",
            borderRadius: "0.5rem",
            padding: "1.5rem",
            marginBottom: "2rem",
          }}>
            <h3 style={{ fontSize: "1.125rem", fontWeight: "600", marginTop: 0 }}>
              Verification Required
            </h3>
            <p style={{ color: "#666", marginBottom: "1rem" }}>
              This bank account needs to be verified before it can be used for payments.
            </p>
            
            <button
              onClick={handleSendMicrodeposits}
              disabled={sendingMicrodeposits}
              style={{
                padding: "0.75rem 1.5rem",
                backgroundColor: sendingMicrodeposits ? "#9ca3af" : "#0070f3",
                color: "white",
                border: "none",
                borderRadius: "0.5rem",
                fontSize: "1rem",
                cursor: sendingMicrodeposits ? "not-allowed" : "pointer",
                fontWeight: "500",
                marginBottom: "1rem",
              }}
            >
              {sendingMicrodeposits ? "Sending..." : "Send Microdeposits"}
            </button>

            <div style={{ borderTop: "1px solid #fbbf24", paddingTop: "1rem" }}>
              <h4 style={{ fontSize: "1rem", fontWeight: "600", marginTop: 0 }}>
                Already received microdeposits?
              </h4>
              <p style={{ fontSize: "0.875rem", color: "#666", marginBottom: "1rem" }}>
                Enter the two deposit amounts (in cents) to verify your account:
              </p>
              <div style={{ display: "flex", gap: "1rem", alignItems: "end" }}>
                <div style={{ flex: 1 }}>
                  <label style={{ display: "block", fontSize: "0.875rem", marginBottom: "0.5rem" }}>
                    Amount 1 (cents)
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="99"
                    value={microdepositAmounts.amount1}
                    onChange={(e) => setMicrodepositAmounts(prev => ({ ...prev, amount1: e.target.value }))}
                    placeholder="32"
                    style={{
                      width: "100%",
                      padding: "0.5rem",
                      border: "1px solid #d1d5db",
                      borderRadius: "0.375rem",
                    }}
                  />
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ display: "block", fontSize: "0.875rem", marginBottom: "0.5rem" }}>
                    Amount 2 (cents)
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="99"
                    value={microdepositAmounts.amount2}
                    onChange={(e) => setMicrodepositAmounts(prev => ({ ...prev, amount2: e.target.value }))}
                    placeholder="45"
                    style={{
                      width: "100%",
                      padding: "0.5rem",
                      border: "1px solid #d1d5db",
                      borderRadius: "0.375rem",
                    }}
                  />
                </div>
                <button
                  onClick={handleConfirmMicrodeposits}
                  disabled={confirmingMicrodeposits}
                  style={{
                    padding: "0.5rem 1.5rem",
                    backgroundColor: confirmingMicrodeposits ? "#9ca3af" : "#10b981",
                    color: "white",
                    border: "none",
                    borderRadius: "0.375rem",
                    cursor: confirmingMicrodeposits ? "not-allowed" : "pointer",
                    fontWeight: "500",
                  }}
                >
                  {confirmingMicrodeposits ? "Verifying..." : "Verify"}
                </button>
              </div>
            </div>
          </div>
        )}

        <div style={{ display: "flex", gap: "1rem" }}>
          <button
            onClick={handleArchive}
            disabled={archiving}
            style={{
              padding: "0.75rem 1.5rem",
              backgroundColor: archiving ? "#d1d5db" : "#fee2e2",
              color: archiving ? "#666" : "#991b1b",
              border: "1px solid #fecaca",
              borderRadius: "0.5rem",
              fontSize: "1rem",
              cursor: archiving ? "not-allowed" : "pointer",
              fontWeight: "500",
            }}
          >
            {archiving ? "Archiving..." : "Archive Bank Account"}
          </button>
        </div>
      </div>
    </div>
  );
}
