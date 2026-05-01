const posts = [
  {
    title: "Welcome to chefwho.codes",
    summary:
      "A starting point for notes on software, shipping products, and practical engineering.",
    date: "2026-05-01",
  },
];

export default function BlogPage() {
  return (
    <section className="panel">
      <header>
        <h1>Blog</h1>
        <p>
          Published notes, case studies, and build logs will live here.
        </p>
      </header>

      <ul className="post-list">
        {posts.map((post) => (
          <li key={post.title} className="card">
            <p className="post-date">{post.date}</p>
            <h2>{post.title}</h2>
            <p>{post.summary}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
