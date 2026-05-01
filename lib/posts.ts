import { promises as fs } from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { remark } from "remark";
import remarkHtml from "remark-html";

const POSTS_DIRECTORY = path.join(process.cwd(), "content", "blog");

type FrontMatter = {
  title?: string;
  summary?: string;
  date?: string;
};

export type PostMeta = {
  slug: string;
  title: string;
  summary: string;
  date: string;
};

export type Post = PostMeta & {
  html: string;
};

async function listPostFiles(): Promise<string[]> {
  try {
    const entries = await fs.readdir(POSTS_DIRECTORY, { withFileTypes: true });
    return entries
      .filter((entry) => entry.isFile())
      .map((entry) => entry.name)
      .filter((fileName) => fileName.endsWith(".md"));
  } catch (error) {
    if (
      error &&
      typeof error === "object" &&
      "code" in error &&
      error.code === "ENOENT"
    ) {
      return [];
    }

    throw error;
  }
}

function postFileToSlug(fileName: string): string {
  return fileName.replace(/\.md$/, "");
}

async function readPostSourceBySlug(slug: string): Promise<string | null> {
  const filePath = path.join(POSTS_DIRECTORY, `${slug}.md`);

  try {
    return await fs.readFile(filePath, "utf8");
  } catch (error) {
    if (
      error &&
      typeof error === "object" &&
      "code" in error &&
      error.code === "ENOENT"
    ) {
      return null;
    }

    throw error;
  }
}

function normalizeMeta(slug: string, data: FrontMatter): PostMeta {
  return {
    slug,
    title: data.title?.trim() || slug.replace(/-/g, " "),
    summary: data.summary?.trim() || "A new post on chefwho.codes.",
    date: data.date?.trim() || "1970-01-01",
  };
}

export async function getAllPostsMeta(): Promise<PostMeta[]> {
  const fileNames = await listPostFiles();

  const posts = await Promise.all(
    fileNames.map(async (fileName) => {
      const slug = postFileToSlug(fileName);
      const source = await readPostSourceBySlug(slug);

      if (!source) {
        return null;
      }

      const parsed = matter(source);
      return normalizeMeta(slug, parsed.data as FrontMatter);
    }),
  );

  return posts
    .filter((post): post is PostMeta => Boolean(post))
    .sort((a, b) => b.date.localeCompare(a.date));
}

export async function getPostBySlug(slug: string): Promise<Post | null> {
  const source = await readPostSourceBySlug(slug);

  if (!source) {
    return null;
  }

  const parsed = matter(source);
  const content = await remark().use(remarkHtml).process(parsed.content);

  return {
    ...normalizeMeta(slug, parsed.data as FrontMatter),
    html: content.toString(),
  };
}
