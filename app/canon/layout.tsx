import type { Metadata } from "next";
import type { ReactNode } from "react";
import { CanonShell } from "./CanonShell";
import "./canon.css";

export const metadata: Metadata = {
  title: "Canon · chefwho.codes",
  description:
    "A two-track record. The rule canonizes what sources can carry. The rest waits.",
};

export default function CanonLayout({ children }: { children: ReactNode }) {
  return <CanonShell>{children}</CanonShell>;
}
