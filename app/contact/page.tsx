import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Contact",
  description: "Get in touch with chefwho.codes.",
};

export default function ContactPage() {
  return (
    <section className="content-card">
      <h1>Contact</h1>
      <p>
        Ready to collaborate? This starter keeps contact simple until forms and
        automation are connected.
      </p>
      <div className="actions">
        <a className="primary-button" href="mailto:hello@chefwho.codes">
          Email hello@chefwho.codes
        </a>
        <Link className="secondary-button" href="/">
          Back home
        </Link>
      </div>
      <p className="note">
        Tip: replace this with a hosted form endpoint, CRM integration, or
        scheduling link as your workflow matures.
      </p>
    </section>
  );
}
