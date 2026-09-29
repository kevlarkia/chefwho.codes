import type { Metadata } from "next";
import { CanonRoom } from "./CanonRoom";

export const metadata: Metadata = {
  title: "Canon · chefwho.codes",
};

export default function CanonPage() {
  return <CanonRoom />;
}
