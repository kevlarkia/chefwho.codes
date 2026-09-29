"use client";

import { useState } from "react";
import { canCarry, formatWeight, weigh } from "@/lib/canon/rule";
import type { Entry } from "@/lib/canon/types";
import { useCanon } from "./CanonProvider";

const LABELS: Record<Entry["disposition"], string> = {
  objective: "Held by the rule",
  desk: "Not canon",
  subjective: "Held by you. Still subjective",
  fallen: "Fell. Still visible",
  disproved: "Disproved, and kept",
  rejected: "Rejected, and kept",
};

export function ClaimCard({ entry }: { entry: Entry }) {
  const { state, doubt, revise, verify, reject, disprove } = useCanon();
  const weighing = weigh(entry.cites, state.sources);
  const [panel, setPanel] = useState<"doubt" | "revise" | "disprove" | null>(
    null,
  );
  const [draft, setDraft] = useState("");

  function open(next: "doubt" | "revise" | "disprove") {
    setPanel(next);
    setDraft(next === "revise" ? entry.text : "");
  }

  const locked =
    entry.disposition === "disproved" || entry.disposition === "rejected";

  return (
    <article className="canon-claim">
      <p className="canon-kicker">{LABELS[entry.disposition]}</p>
      <h3>{entry.text}</h3>
      <p className="canon-weigh">
        Support {formatWeight(weighing.support)}. Contest{" "}
        {formatWeight(weighing.contest)}. Net {formatWeight(weighing.net)}.
        Carriers {weighing.carriers}. Bar {formatWeight(weighing.bar)}.
        {weighing.fight ? " A fight. Not objective." : ""}
      </p>
      <ul className="canon-cites">
        {entry.cites.map((cite) => {
          const source = state.sources.find((item) => item.id === cite.sourceId);
          if (!source) {
            return (
              <li key={`${cite.sourceId}-${cite.role}`}>
                A cited source is not in this browser. {cite.role}.
              </li>
            );
          }
          const carries = cite.role === "support" && canCarry(source);
          return (
            <li key={`${cite.sourceId}-${cite.role}`}>
              {source.name}. {source.kind}. Standing {formatWeight(source.standing)}.{" "}
              {cite.role === "support" ? "Supporting." : "Contesting."}{" "}
              {cite.role === "contest"
                ? "Subtracts its full standing."
                : carries
                  ? "Carrier."
                  : "Informs only."}
            </li>
          );
        })}
      </ul>
      <details>
        <summary>Journey</summary>
        <ol className="canon-journey">
          {entry.journey.map((event) => (
            <li key={event.id}>
              <time dateTime={event.at}>{event.kind}</time>
              <span>{event.note}</span>
            </li>
          ))}
        </ol>
      </details>
      <div className="canon-actions">
        <button type="button" className="secondary-button" onClick={() => open("doubt")}>
          Keep a doubt
        </button>
        <button type="button" className="secondary-button" onClick={() => open("revise")}>
          Revise
        </button>
        {!locked && entry.disposition !== "objective" ? (
          <button type="button" className="secondary-button" onClick={() => verify(entry.id)}>
            Verify
          </button>
        ) : null}
        {entry.disposition !== "objective" && !locked ? (
          <button type="button" className="secondary-button" onClick={() => reject(entry.id)}>
            Reject, and keep
          </button>
        ) : null}
        {entry.disposition !== "disproved" ? (
          <button
            type="button"
            className="secondary-button"
            onClick={() => open("disprove")}
          >
            Disprove, and keep
          </button>
        ) : null}
      </div>
      {panel === "doubt" ? (
        <form
          className="canon-inline"
          onSubmit={(event) => {
            event.preventDefault();
            doubt(entry.id, draft);
            setDraft("");
            setPanel(null);
          }}
        >
          <label htmlFor={`doubt-${entry.id}`}>Doubt</label>
          <textarea
            id={`doubt-${entry.id}`}
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            rows={3}
          />
          <button type="submit" className="primary-button">
            Keep this doubt
          </button>
        </form>
      ) : null}
      {panel === "revise" ? (
        <form
          className="canon-inline"
          onSubmit={(event) => {
            event.preventDefault();
            revise(entry.id, draft);
            setPanel(null);
          }}
        >
          <label htmlFor={`revise-${entry.id}`}>Revised wording</label>
          <textarea
            id={`revise-${entry.id}`}
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            rows={3}
          />
          <button type="submit" className="primary-button">
            Keep the revision
          </button>
        </form>
      ) : null}
      {panel === "disprove" ? (
        <form
          className="canon-inline"
          onSubmit={(event) => {
            event.preventDefault();
            disprove(entry.id, draft);
            setDraft("");
            setPanel(null);
          }}
        >
          <label htmlFor={`disprove-${entry.id}`}>What failed</label>
          <textarea
            id={`disprove-${entry.id}`}
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            rows={3}
          />
          <button type="submit" className="primary-button">
            Disprove, and keep
          </button>
        </form>
      ) : null}
    </article>
  );
}

export function ClaimList({ entries }: { entries: Entry[] }) {
  if (entries.length === 0) {
    return null;
  }
  return (
    <div className="canon-claims">
      {entries.map((entry) => (
        <ClaimCard key={entry.id} entry={entry} />
      ))}
    </div>
  );
}
