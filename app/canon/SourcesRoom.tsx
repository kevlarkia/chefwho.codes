"use client";

import { useState } from "react";
import { barFor, formatWeight } from "@/lib/canon/rule";
import type { SourceKind } from "@/lib/canon/types";
import { SEASONED_AT, SOURCE_KINDS } from "@/lib/canon/types";
import { useCanon } from "./CanonProvider";

export function SourcesRoom() {
  const { state, setStanding, addSource } = useCanon();
  const bar = barFor(state.sources);
  const seasoned = state.sources.filter(
    (source) => source.standing >= SEASONED_AT,
  ).length;
  const [name, setName] = useState("");
  const [kind, setKind] = useState<SourceKind>("primary");
  const [standing, setNewStanding] = useState("");

  return (
    <section className="canon-stack">
      <h2>Sources</h2>
      <p>
        Standing can rise or fall. Sources are not deleted. The bar is{" "}
        {formatWeight(bar)}.
        {seasoned < 3
          ? " Fewer than three seasoned sources exist, so the bar is 64."
          : " It is the middle standing of the seasoned sources, held between 58 and 80."}
      </p>
      <h3>Source weighting</h3>
      <p>Source weighting is about one source.</p>
      <ul className="canon-plain">
        <li>
          Its kind. Primary and record can carry. A witness can carry only at
          70 or above. Press, self, and hearsay cannot carry. They can inform
          only.
        </li>
        <li>
          Its standing. A number. It can be raised or lowered. Seasoned means
          50 or above.
        </li>
      </ul>
      <h3>Evidence weight</h3>
      <p>Evidence weight is about one claim, after those sources are applied.</p>
      <ul className="canon-plain">
        <li>
          An eligible source that supports it adds its full standing, and counts
          as a carrier.
        </li>
        <li>
          A source that supports it but cannot carry adds a quarter of its
          standing, and does not count as a carrier.
        </li>
        <li>A source that contests it subtracts its full standing.</li>
        <li>
          A contest is a fight when it is close and strong enough. No separate
          cutoff for those words was stored. Here, strong means the contesting
          weight is at least 58, and close means the gap between support and
          contest is at most the bar. A fight is not objective.
        </li>
        <li>
          It is objective only when at least one eligible source carries it, it
          is not a fight, and the total meets the bar.
        </li>
        <li>
          If you verify a claim the rule would not canonize, you hold it, and it
          stays subjective. That hold is not rewritten as proof.
        </li>
      </ul>
      <ul className="canon-sources">
        {state.sources.map((source) => (
          <li key={source.id} className="canon-claim">
            <h3>{source.name}</h3>
            <p>
              {source.kind}. Standing {formatWeight(source.standing)}.
            </p>
            <ol className="canon-journey">
              {source.history.map((change) => (
                <li key={`${change.at}-${change.standing}`}>
                  <time dateTime={change.at}>{formatWeight(change.standing)}</time>
                  <span>{change.note}</span>
                </li>
              ))}
            </ol>
            <StandingForm
              key={`${source.id}-${source.standing}`}
              id={source.id}
              current={source.standing}
              onSet={setStanding}
            />
          </li>
        ))}
      </ul>
      {state.sources.length === 0 ? <p>No source is in this browser.</p> : null}
      <h3>Add a source</h3>
      <form
        className="canon-form"
        onSubmit={(event) => {
          event.preventDefault();
          const next = Number(standing);
          if (!name.trim() || !Number.isFinite(next)) {
            return;
          }
          addSource({ name, kind, standing: next });
          setName("");
          setNewStanding("");
          setKind("primary");
        }}
      >
        <label htmlFor="source-name">Name</label>
        <input
          id="source-name"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
        <label htmlFor="source-kind">Kind</label>
        <select
          id="source-kind"
          value={kind}
          onChange={(event) => setKind(event.target.value as SourceKind)}
        >
          {SOURCE_KINDS.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
        <label htmlFor="source-standing">Standing</label>
        <input
          id="source-standing"
          inputMode="decimal"
          value={standing}
          onChange={(event) => setNewStanding(event.target.value)}
        />
        <button type="submit" className="primary-button">
          Add the source
        </button>
      </form>
    </section>
  );
}

function StandingForm({
  id,
  current,
  onSet,
}: {
  id: string;
  current: number;
  onSet: (id: string, standing: number, note: string) => void;
}) {
  const [value, setValue] = useState(String(current));
  const [note, setNote] = useState("");
  return (
    <form
      className="canon-form"
      onSubmit={(event) => {
        event.preventDefault();
        const next = Number(value);
        if (!Number.isFinite(next)) {
          return;
        }
        onSet(id, next, note);
        setNote("");
      }}
    >
      <label htmlFor={`standing-${id}`}>New standing</label>
      <input
        id={`standing-${id}`}
        inputMode="decimal"
        value={value}
        onChange={(event) => setValue(event.target.value)}
      />
      <label htmlFor={`standing-note-${id}`}>Note</label>
      <input
        id={`standing-note-${id}`}
        value={note}
        onChange={(event) => setNote(event.target.value)}
      />
      <button type="submit" className="secondary-button">
        Set standing
      </button>
    </form>
  );
}
