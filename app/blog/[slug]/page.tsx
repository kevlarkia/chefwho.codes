import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getPostBySlug, getPostSlugs } from "@/lib/posts";

type PostPageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateStaticParams() {
  return getPostSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: PostPageProps): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPostBySlug(slug);

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
  const { slug } = await params;
  const post = await getPostBySlug(slug);

  if (!post) {
    notFound();
  }

  return (
    <article className="panel post-article">
      <p className="post-date">{post.dateLabel}</p>
      <h1>{post.title}</h1>
      <p className="lede">{post.summary}</p>
      <div
        className="post-body"
        dangerouslySetInnerHTML={{ __html: post.contentHtml }}
      />
      <p>
        <Link href="/blog">← Back to blog</Link>
      </p>
    </article>
  );
}
