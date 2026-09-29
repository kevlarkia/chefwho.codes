import type { Metadata } from "next";
import { SourcesRoom } from "../SourcesRoom";

export const metadata: Metadata = {
  title: "Sources · Canon",
};

export default function SourcesPage() {
  return <SourcesRoom />;
}
