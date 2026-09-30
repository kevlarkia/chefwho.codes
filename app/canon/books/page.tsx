import type { Metadata } from "next";
import { BooksRoom } from "../BooksRoom";

export const metadata: Metadata = {
  title: "Books · Canon",
};

export default function BooksPage() {
  return <BooksRoom />;
}