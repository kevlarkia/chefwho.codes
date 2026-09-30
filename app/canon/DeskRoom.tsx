"use client";

import { ClaimList } from "./ClaimCard";
import { useCanon } from "./CanonProvider";

export function DeskRoom() {
  const { state } = useCanon();
  const waiting = state.entries.filter(
    (entry) => entry.disposition === "desk" || entry.disposition === "subjective",
  );

  return (
    <section className="canon-stack">
      <h2>Desk</h2>
      <p>
        What the rule will not decide. You verify or reject. Verification does
        not make it objective. A hold you make is not dropped in silence if
        standing later moves.
      </p>
      {waiting.length === 0 ? <p>The desk is clear.</p> : null}
      <ClaimList entries={waiting} />
    </section>
  );
}
