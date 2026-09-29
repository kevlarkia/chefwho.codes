import type { Metadata } from "next";
import { EnterRoom } from "../EnterRoom";

export const metadata: Metadata = {
  title: "Enter · Canon",
};

export default function EnterPage() {
  return <EnterRoom />;
}
