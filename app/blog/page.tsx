import Link from "next/link";
import { getAllPostMetadata } from "@/lib/posts";

export default function BlogPage() {
  const posts = getAllPostMetadata();

  return (
    <section className="panel">
      <header>
        <h1>Blog</h1>
        <p>
          Published notes, case studies, and build logs will live here.
        </p>
      </header>

      {posts.length === 0 ? (
        <p>No posts published yet.</p>
      ) : (
        <ul className="post-list">
          {posts.map((post) => (
            <li key={post.slug} className="card">
              <p className="post-date">{post.date}</p>
              <h2>
                <Link href={`/blog/${post.slug}`}>{post.title}</Link>
              </h2>
              <p>{post.summary}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
