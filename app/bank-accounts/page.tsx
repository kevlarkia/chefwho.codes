"use client";

import { useState } from "react";
import BankAccountList from "./BankAccountList";
import AddBankAccountForm from "./AddBankAccountForm";

export default function BankAccountsPage() {
  const [showAddForm, setShowAddForm] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleAccountAdded = () => {
    setShowAddForm(false);
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "2rem" }}>
      <div style={{ marginBottom: "2rem" }}>
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1rem",
        }}>
          <h1 style={{ fontSize: "2rem", fontWeight: "bold", margin: 0 }}>
            Bank Accounts
          </h1>
          {!showAddForm && (
            <button
              onClick={() => setShowAddForm(true)}
              style={{
                padding: "0.75rem 1.5rem",
                backgroundColor: "#0070f3",
                color: "white",
                border: "none",
                borderRadius: "0.5rem",
                fontSize: "1rem",
                cursor: "pointer",
                fontWeight: "500",
              }}
            >
              Add Bank Account
            </button>
          )}
        </div>
        <p style={{ color: "#666", margin: 0 }}>
          Manage your US bank accounts for ACH payments
        </p>
      </div>

      {showAddForm && (
        <div style={{
          backgroundColor: "#f5f5f5",
          padding: "2rem",
          borderRadius: "0.5rem",
          marginBottom: "2rem",
        }}>
          <div style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "1rem",
          }}>
            <h2 style={{ fontSize: "1.5rem", fontWeight: "600", margin: 0 }}>
              Add New Bank Account
            </h2>
            <button
              onClick={() => setShowAddForm(false)}
              style={{
                padding: "0.5rem 1rem",
                backgroundColor: "#666",
                color: "white",
                border: "none",
                borderRadius: "0.375rem",
                fontSize: "0.875rem",
                cursor: "pointer",
              }}
            >
              Cancel
            </button>
          </div>
          <AddBankAccountForm onSuccess={handleAccountAdded} />
        </div>
      )}

      <BankAccountList key={refreshTrigger} />
    </div>
  );
}
