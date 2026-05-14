"use client";

import { FormEvent, useState } from "react";

type FormState = {
  status: "idle" | "submitting" | "success" | "error";
  message: string;
};

const initialState: FormState = {
  status: "idle",
  message: "",
};

export default function ContactForm() {
  const [state, setState] = useState<FormState>(initialState);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);

    const payload = {
      name: String(formData.get("name") ?? ""),
      email: String(formData.get("email") ?? ""),
      message: String(formData.get("message") ?? ""),
    };

    setState({ status: "submitting", message: "Sending your message..." });

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const result = (await response.json()) as { message?: string; error?: string };

      if (!response.ok) {
        setState({
          status: "error",
          message: result.error ?? "Unable to send your message.",
        });
        return;
      }

      setState({
        status: "success",
        message: result.message ?? "Message sent successfully.",
      });
      form.reset();
    } catch {
      setState({
        status: "error",
        message: "Network error. Please try again.",
      });
    }
  }

  return (
    <form className="contact-form" onSubmit={handleSubmit}>
      <label className="contact-field">
        Name
        <input
          name="name"
          type="text"
          required
          minLength={2}
          autoComplete="name"
          placeholder="Your name"
        />
      </label>

      <label className="contact-field">
        Email
        <input
          name="email"
          type="email"
          required
          autoComplete="email"
          placeholder="you@example.com"
        />
      </label>

      <label className="contact-field">
        Message
        <textarea
          name="message"
          required
          minLength={20}
          maxLength={4000}
          rows={6}
          placeholder="Tell me a little about what you are looking to build."
        />
      </label>

      <button className="primary-button" type="submit" disabled={state.status === "submitting"}>
        {state.status === "submitting" ? "Sending..." : "Send message"}
      </button>

      {state.message ? (
        <p
          className={state.status === "error" ? "form-feedback error" : "form-feedback"}
          role="status"
        >
          {state.message}
        </p>
      ) : null}
    </form>
  );
}
