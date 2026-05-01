import type { Metadata } from "next";
import Link from "next/link";
import ContactForm from "./ContactForm";

export const metadata: Metadata = {
  title: "Contact",
  description: "Get in touch with chefwho.codes.",
};

export default function ContactPage() {
  return (
    <section className="content-card">
      <h1>Contact</h1>
      <p>
        Ready to collaborate? Send a message through the form below and I will
        get back to you.
      </p>
      <ContactForm />
      <div className="actions">
        <Link className="secondary-button" href="/">
          Back home
        </Link>
      </div>
      <p className="note">
        Tip: for production, connect this endpoint to your email provider or
        CRM and add rate limiting.
      </p>
    </section>
  );
}
