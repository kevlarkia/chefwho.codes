"use client";

import { useState } from "react";
import { exportCopy } from "@/lib/canon/copy";
import { ClaimList } from "./ClaimCard";
import { useCanon } from "./CanonProvider";

export function CanonRoom() {
  const {
    state,
    specimenIsLoad,
    blankThisBrowser,
    loadSpecimen,
    importCopy,
  } = useCanon();
  const [message, setMessage] = useState<string | null>(null);
  const [blankArmed, setBlankArmed] = useState(false);
  const holding = state.entries.filter((entry) => entry.disposition === "objective");
  const visible = state.entries.filter((entry) =>
    entry.disposition === "fallen" ||
    entry.disposition === "disproved" ||
    entry.disposition === "rejected",
  );
  const empty = state.sources.length === 0 && state.entries.length === 0;

  function downloadCopy() {
    const copy = exportCopy(state.sources, state.entries, state.blanked);
    const blob = new Blob([JSON.stringify(copy, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "kanon-copy.json";
    link.click();
    URL.revokeObjectURL(url);
    setMessage(
      "A copy was downloaded. It holds sources and entries. It does not hold the shelf, the talks, or the voice choice.",
    );
  }

  return (
    <section className="canon-stack">
      <h2>What holds</h2>
      <p>
        A claim is canonical only when the sources on it can carry it. If they
        cannot, it waits. The rule decides when the claim comes in. Source
        weighting and evidence weight are on Sources.
      </p>
      {specimenIsLoad ? (
        <p>
          A worked specimen is loaded. These are specimens, not your canon,
          until you keep them.
        </p>
      ) : null}
      {holding.length === 0 ? <p>Nothing is held by the rule.</p> : null}
      <ClaimList entries={holding} />
      <h2>Still visible</h2>
      {visible.length === 0 ? (
        <p>No fallen, disproved, or rejected claim is in this browser.</p>
      ) : (
        <ClaimList entries={visible} />
      )}
      <h2>Copies</h2>
      <ol className="canon-plain">
        <li>This browser. It can vanish with the browser. It is not enough.</li>
        <li>
          A file you can download. Bringing it back replaces sources and
          entries in this browser. The file itself is not changed.
        </li>
        <li>
          A storage space. Not switched on. Old files would stay. Nothing would
          be deleted.
        </li>
      </ol>
      <div className="canon-actions">
        <button type="button" className="primary-button" onClick={downloadCopy}>
          Keep a copy
        </button>
        <label className="secondary-button canon-file">
          Bring a copy back
          <input
            type="file"
            accept="application/json,.json"
            onChange={async (event) => {
              const file = event.target.files?.[0];
              event.target.value = "";
              if (!file) {
                return;
              }
              try {
                const parsed: unknown = JSON.parse(await file.text());
                const reason = importCopy(parsed);
                setMessage(
                  reason ??
                    "The copy is in this browser. The file was not changed. The shelf and the talks stayed.",
                );
              } catch {
                setMessage("That file is not a canon copy.");
              }
            }}
          />
        </label>
      </div>
      {message ? <p role="status">{message}</p> : null}
      {empty ? (
        <button type="button" className="secondary-button" onClick={loadSpecimen}>
          Load the worked specimen
        </button>
      ) : null}
      {blankArmed ? (
        <div className="canon-notice">
          <p>
            This clears sources and entries in this browser. It does not clear
            the shelf, the talks, or the synopses.
          </p>
          <div className="canon-actions">
            <button
              type="button"
              className="primary-button"
              onClick={() => {
                blankThisBrowser();
                setBlankArmed(false);
                setMessage("Sources and entries in this browser were cleared.");
              }}
            >
              Blank sources and entries
            </button>
            <button
              type="button"
              className="secondary-button"
              onClick={() => setBlankArmed(false)}
            >
              Leave the record
            </button>
          </div>
        </div>
      ) : (
        <button
          type="button"
          className="secondary-button"
          onClick={() => setBlankArmed(true)}
        >
          Blank this browser&apos;s record
        </button>
      )}
      <h2>Five checks</h2>
      <p>All still open. Copy 3 is not switched on.</p>
      <ul className="canon-plain">
        <li>The storage space</li>
        <li>A key that only opens it</li>
        <li>The database</li>
        <li>The connection</li>
        <li>The test</li>
      </ul>
      <p>
        Do not send a key in a message. The plan for the data is sources,
        entries, and copies. A row can be updated. An id left out of a later
        file stays where it is. There is no delete. That door is written and
        not switched on.
      </p>
      <h2>Left open</h2>
      <ul className="canon-plain">
        <li>The words behind the acronym</li>
        <li>The Bitcoin title</li>
        <li>Whether the cut-off guide belongs on the shelf</li>
        <li>Copy 3</li>
        <li>Which mouth speaks, once the record has already closed</li>
        <li>A voice made for the instrument</li>
        <li>The listening decision</li>
      </ul>
    </section>
  );
}
