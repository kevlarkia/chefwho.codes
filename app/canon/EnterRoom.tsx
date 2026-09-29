"use client";

import { useState } from "react";
import { closedLine } from "@/lib/canon/pipe";
import { formatWeight, weigh } from "@/lib/canon/rule";
import { resolveDisposition } from "@/lib/canon/record";
import type { Cite, Entry } from "@/lib/canon/types";
import { useCanon } from "./CanonProvider";

export function EnterRoom() {
  const { state, addEntry } = useCanon();
  const [text, setText] = useState("");
  const [cites, setCites] = useState<Cite[]>([]);
  const [sourceId, setSourceId] = useState(state.sources[0]?.id ?? "");
  const selectedSourceId = state.sources.some((source) => source.id === sourceId)
    ? sourceId
    : (state.sources[0]?.id ?? "");
  const [role, setRole] = useState<Cite["role"]>("support");
  const [kept, setKept] = useState<string | null>(null);

  const draft: Entry = {
    id: "preview",
    text: text.trim() || "The claim is not written yet.",
    cites,
    disposition: "desk",
    humanHold: false,
    journey: [],
  };
  const weighing = weigh(cites, state.sources);
  const preview: Entry = {
    ...draft,
    disposition: text.trim()
      ? resolveDisposition(draft, weighing.objective)
      : "desk",
  };

  return (
    <section className="canon-stack">
      <h2>Enter</h2>
      <p>
        Write a claim, cite sources as supporting or contesting, and read the
        ruling before it is kept.
      </p>
      <form
        className="canon-form"
        onSubmit={(event) => {
          event.preventDefault();
          if (!text.trim()) {
            return;
          }
          addEntry({ text, cites });
          setKept(text.trim());
          setText("");
          setCites([]);
        }}
      >
        <label htmlFor="claim-text">Claim</label>
        <textarea
          id="claim-text"
          value={text}
          rows={4}
          onChange={(event) => setText(event.target.value)}
        />
        <div className="canon-cite-row">
          <label htmlFor="cite-source">Source</label>
          <select
            id="cite-source"
            value={selectedSourceId}
            onChange={(event) => setSourceId(event.target.value)}
          >
            {state.sources.map((source) => (
              <option key={source.id} value={source.id}>
                {source.name}
              </option>
            ))}
          </select>
          <label htmlFor="cite-role">Role</label>
          <select
            id="cite-role"
            value={role}
            onChange={(event) => setRole(event.target.value as Cite["role"])}
          >
            <option value="support">Supporting</option>
            <option value="contest">Contesting</option>
          </select>
          <button
            type="button"
            className="secondary-button"
            onClick={() => {
              if (!selectedSourceId) {
                return;
              }
              setCites((current) => [
                ...current.filter((cite) => cite.sourceId !== selectedSourceId),
                { sourceId: selectedSourceId, role },
              ]);
            }}
          >
            Add the cite
          </button>
        </div>
        <ul className="canon-plain">
          {cites.map((cite) => {
            const source = state.sources.find((item) => item.id === cite.sourceId);
            return (
              <li key={cite.sourceId}>
                {source?.name ?? "A source that is not in this browser"}.{" "}
                {cite.role === "support" ? "Supporting." : "Contesting."}
              </li>
            );
          })}
        </ul>
        {text.trim() ? (
          <div className="canon-ruling">
            <p className="canon-kicker">Ruling, before it is kept</p>
            <p>{closedLine(preview, state.sources)}</p>
            <p className="canon-weigh">
              Support {formatWeight(weighing.support)}. Contest{" "}
              {formatWeight(weighing.contest)}. Net {formatWeight(weighing.net)}.
              Carriers {weighing.carriers}. Bar {formatWeight(weighing.bar)}.
              {weighing.fight ? " A fight. Not objective." : ""}
            </p>
          </div>
        ) : null}
        <button type="submit" className="primary-button">
          Commit to the record
        </button>
      </form>
      {kept ? <p role="status">Kept. {kept}</p> : null}
    </section>
  );
}
