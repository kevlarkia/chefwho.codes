"use client";

import { useEffect, useState } from "react";
import type { USBankAccount } from "@/lib/types/stripe-bank-account";
import Link from "next/link";

export default function BankAccountList() {
  const [accounts, setAccounts] = useState<USBankAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [archiving, setArchiving] = useState<string | null>(null);

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch("/api/bank-accounts");
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to fetch bank accounts");
        }

        setAccounts(data.data.data || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchAccounts();
  }, []);

  const handleArchive = async (id: string) => {
    if (!confirm("Are you sure you want to archive this bank account?")) {
      return;
    }

    try {
      setArchiving(id);
      const response = await fetch(`/api/bank-accounts/${id}/archive`, {
        method: "POST",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to archive bank account");
      }

      const refreshResponse = await fetch("/api/bank-accounts");
      const refreshData = await refreshResponse.json();
      if (refreshResponse.ok) {
        setAccounts(refreshData.data.data || []);
      }
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to archive bank account");
    } finally {
      setArchiving(null);
    }
  };

  const getStatusBadge = (status: string) => {
    const styles: Record<string, React.CSSProperties> = {
      verified: {
        backgroundColor: "#10b981",
        color: "white",
        padding: "0.25rem 0.75rem",
        borderRadius: "9999px",
        fontSize: "0.75rem",
        fontWeight: "600",
      },
      new: {
        backgroundColor: "#f59e0b",
        color: "white",
        padding: "0.25rem 0.75rem",
        borderRadius: "9999px",
        fontSize: "0.75rem",
        fontWeight: "600",
      },
      verification_failed: {
        backgroundColor: "#ef4444",
        color: "white",
        padding: "0.25rem 0.75rem",
        borderRadius: "9999px",
        fontSize: "0.75rem",
        fontWeight: "600",
      },
      errored: {
        backgroundColor: "#ef4444",
        color: "white",
        padding: "0.25rem 0.75rem",
        borderRadius: "9999px",
        fontSize: "0.75rem",
        fontWeight: "600",
      },
    };

    return (
      <span style={styles[status] || styles.new}>
        {status.replace(/_/g, " ").toUpperCase()}
      </span>
    );
  };

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "3rem", color: "#666" }}>
        Loading bank accounts...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        backgroundColor: "#fee2e2",
        border: "1px solid #ef4444",
        color: "#991b1b",
        padding: "1rem",
        borderRadius: "0.5rem",
      }}>
        <strong>Error:</strong> {error}
      </div>
    );
  }

  if (accounts.length === 0) {
    return (
      <div style={{
        textAlign: "center",
        padding: "3rem",
        backgroundColor: "#f9fafb",
        borderRadius: "0.5rem",
        border: "2px dashed #d1d5db",
      }}>
        <p style={{ fontSize: "1.125rem", color: "#666", marginBottom: "0.5rem" }}>
          No bank accounts found
        </p>
        <p style={{ fontSize: "0.875rem", color: "#999" }}>
          Add your first bank account to get started
        </p>
      </div>
    );
  }

  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      {accounts.map((account) => (
        <div
          key={account.id}
          style={{
            backgroundColor: "white",
            border: "1px solid #e5e7eb",
            borderRadius: "0.5rem",
            padding: "1.5rem",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div style={{ flex: 1 }}>
            <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "0.5rem" }}>
              <h3 style={{ fontSize: "1.125rem", fontWeight: "600", margin: 0 }}>
                {account.bank_name || "Unknown Bank"}
              </h3>
              {getStatusBadge(account.status)}
            </div>
            <div style={{ color: "#666", fontSize: "0.875rem" }}>
              <p style={{ margin: "0.25rem 0" }}>
                <strong>Account Holder:</strong> {account.account_holder_name}
              </p>
              <p style={{ margin: "0.25rem 0" }}>
                <strong>Account Type:</strong> {account.account_type}
              </p>
              <p style={{ margin: "0.25rem 0" }}>
                <strong>Last 4:</strong> ••••{account.last4}
              </p>
              <p style={{ margin: "0.25rem 0" }}>
                <strong>Routing:</strong> {account.routing_number}
              </p>
            </div>
          </div>
          <div style={{ display: "flex", gap: "0.5rem", flexDirection: "column" }}>
            <Link
              href={`/bank-accounts/${account.id}`}
              style={{
                padding: "0.5rem 1rem",
                backgroundColor: "#f3f4f6",
                color: "#374151",
                border: "1px solid #d1d5db",
                borderRadius: "0.375rem",
                fontSize: "0.875rem",
                textDecoration: "none",
                textAlign: "center",
                cursor: "pointer",
              }}
            >
              View Details
            </Link>
            <button
              onClick={() => handleArchive(account.id)}
              disabled={archiving === account.id}
              style={{
                padding: "0.5rem 1rem",
                backgroundColor: archiving === account.id ? "#d1d5db" : "#fee2e2",
                color: archiving === account.id ? "#666" : "#991b1b",
                border: "1px solid #fecaca",
                borderRadius: "0.375rem",
                fontSize: "0.875rem",
                cursor: archiving === account.id ? "not-allowed" : "pointer",
              }}
            >
              {archiving === account.id ? "Archiving..." : "Archive"}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
