import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getAllPostsMeta, getPostBySlug } from "@/lib/posts";

type PostPageProps = { params: { slug: string } };

export async function generateStaticParams() {
  const posts = await getAllPostsMeta();
  return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({
  params,
}: PostPageProps): Promise<Metadata> {
  const post = await getPostBySlug(params.slug);

  if (!post) {
    return {
      title: "Post Not Found",
    };
  }

  return {
    title: post.title,
    description: post.summary,
  };
}

export default async function PostPage({ params }: PostPageProps) {
  const post = await getPostBySlug(params.slug);

  if (!post) {
    notFound();
  }

  return (
    <article className="panel post-article">
      <p className="post-date">{post.date}</p>
      <h1>{post.title}</h1>
      <p className="lede">{post.summary}</p>
      <div
        className="post-body"
        dangerouslySetInnerHTML={{ __html: post.html }}
      />
      <p>
        <Link href="/blog">← Back to blog</Link>
      </p>
    </article>
  );
}
