import type { Metadata } from "next";
import { AskRoom } from "../AskRoom";

export const metadata: Metadata = {
  title: "Ask · Canon",
};

export default function AskPage() {
  return <AskRoom />;
}
