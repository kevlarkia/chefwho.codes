import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Smart Workforce System",
  description: "Readiness view for the Smart Workforce System rollout.",
};

const readinessItems = [
  "Legacy connection mapping reviewed",
  "Core connection paths are linked and active",
  "Rollout communication path is in place",
];

export default function SmartWorkforceSystemPage() {
  return (
    <section className="content-card">
      <h1>Smart Workforce System</h1>
      <p>
        The Smart Workforce System workspace is now connected into the site and
        ready for next-phase implementation updates.
      </p>
      <ul className="card-list">
        {readinessItems.map((item) => (
          <li key={item} className="card">
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}
