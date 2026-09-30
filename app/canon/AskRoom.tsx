"use client";

import { useState } from "react";
import { useCanon } from "./CanonProvider";
import { useCanonVoice } from "./use-voice";

const CHECKS = [
  "When did the Bodleian open to readers?",
  "Do canon and cannon share a root?",
];

export function AskRoom() {
  const { state, setKeepTalks, askQuestion, keepThisAnswer, setSynopsis } =
    useCanon();
  const { speak } = useCanonVoice();
  const [question, setQuestion] = useState("");
  const [lines, setLines] = useState<string[]>([]);
  const [stored, setStored] = useState(false);
  const [asked, setAsked] = useState("");

  function run(nextQuestion: string) {
    const trimmed = nextQuestion.trim();
    setAsked(trimmed);
    if (!trimmed) {
      setLines([]);
      setStored(false);
      return;
    }
    const result = askQuestion(trimmed);
    setLines(result.lines);
    setStored(result.stored);
  }

  return (
    <section className="canon-stack">
      <h2>Ask</h2>
      <p>
        The record answers first. No model is connected, so the lines
        themselves are the answer. A model may only rephrase those lines. It
        cannot write the record.
      </p>
      <label className="canon-check">
        <input
          type="checkbox"
          checked={state.keepTalks}
          onChange={(event) => setKeepTalks(event.target.checked)}
        />
        Keep talks. Turning this off does not erase what is already kept.
      </label>
      <form
        className="canon-form"
        onSubmit={(event) => {
          event.preventDefault();
          run(question);
        }}
      >
        <label htmlFor="ask-question">Question</label>
        <textarea
          id="ask-question"
          value={question}
          rows={3}
          onChange={(event) => setQuestion(event.target.value)}
        />
        <button type="submit" className="primary-button">
          Ask
        </button>
      </form>
      <div className="canon-actions">
        {CHECKS.map((item) => (
          <button
            key={item}
            type="button"
            className="secondary-button"
            onClick={() => {
              setQuestion(item);
              run(item);
            }}
          >
            {item}
          </button>
        ))}
      </div>
      <div aria-live="polite">
        {asked.length === 0 ? null : lines.length === 0 ? (
          <p>An empty question is not sent.</p>
        ) : (
          <div className="canon-ruling">
            {lines.map((line) => (
              <p key={line}>{line}</p>
            ))}
            <div className="canon-actions">
              <button
                type="button"
                className="secondary-button"
                onClick={() => speak(lines.join(" "))}
              >
                Hear it
              </button>
              {!stored ? (
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => {
                    keepThisAnswer(asked, lines);
                    setStored(true);
                  }}
                >
                  Keep this answer
                </button>
              ) : (
                <p>Kept in this browser.</p>
              )}
            </div>
          </div>
        )}
      </div>
      <h3>Talks</h3>
      <p>
        A synopsis is a note you write: what that stretch actually changed. A
        model does not write it. Agreement is not proof.
      </p>
      <p>These talks live in this browser. They are not yet a second home.</p>
      {state.talks.length === 0 ? <p>No talk is kept.</p> : null}
      <ul className="canon-sources">
        {state.talks.map((talk) => (
          <li key={talk.id} className="canon-claim">
            <p className="canon-kicker">{talk.question}</p>
            {talk.lines.map((line) => (
              <p key={line}>{line}</p>
            ))}
            <label htmlFor={`synopsis-${talk.id}`}>Synopsis</label>
            <textarea
              id={`synopsis-${talk.id}`}
              rows={3}
              value={talk.synopsis}
              placeholder="What this stretch actually changed"
              onChange={(event) => setSynopsis(talk.id, event.target.value)}
            />
          </li>
        ))}
      </ul>
    </section>
  );
}
