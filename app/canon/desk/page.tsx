import type { Metadata } from "next";
import { DeskRoom } from "../DeskRoom";

export const metadata: Metadata = {
  title: "Desk · Canon",
};

export default function DeskPage() {
  return <DeskRoom />;
}
