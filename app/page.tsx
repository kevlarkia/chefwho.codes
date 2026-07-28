const highlights = [
  "Built with Next.js App Router and TypeScript",
  "Ready-to-edit Home, About, Contact, and Blog pages",
  "Smart Workforce System page wired in and ready for rollout",
  "CI-enabled repository with templates and security docs",
];

export default function HomePage() {
  return (
    <section className="stack">
      <p className="eyebrow">ChefWho.codes</p>
      <h1>Build your digital home one clear step at a time.</h1>
      <p className="lede">
        This starter gives you a clean, maintainable baseline for your personal
        site. Replace this copy with your story, your work, and your call to
        action.
      </p>
      <ul className="card-list">
        {highlights.map((item) => (
          <li key={item} className="card">
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}
