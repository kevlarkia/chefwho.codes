"use client";

import type { ReaderView } from "@/lib/canon/reader";
import { useCanonVoice } from "./use-voice";

export function ReaderSidebar({
  phrase,
  view,
  asking,
  onClose,
}: {
  phrase: string | null;
  view: ReaderView | null;
  asking: boolean;
  onClose: () => void;
}) {
  const { voiceURI, setVoiceURI, voices, speak } = useCanonVoice();

  return (
    <aside className="canon-reader" aria-label="Reader">
      <div>
        <p className="canon-kicker">Reader</p>
        <p>
          Mark a word or a short phrase. The definition held now is shown, then
          the origin.
        </p>
      </div>
      {phrase ? (
        <div aria-live="polite">
          <p className="canon-phrase">{phrase}</p>
          {asking ? <p>Asking the wider base.</p> : null}
          {view ? (
            <>
              <p>{view.marker}</p>
              {view.definitions.map((definition) => (
                <p key={definition}>{definition}</p>
              ))}
              {view.origin ? (
                <p>
                  <span className="canon-kicker">Origin</span> {view.origin}
                </p>
              ) : null}
              {view.originMissing ? <p>The origin is not in the base.</p> : null}
              <div className="canon-actions">
                <button
                  type="button"
                  className="primary-button"
                  onClick={() => speak(phrase)}
                >
                  Say it
                </button>
                <button type="button" className="secondary-button" onClick={onClose}>
                  Close
                </button>
              </div>
              {view.audioUrl ? (
                <p>
                  <a href={view.audioUrl}>Recording</a>
                </p>
              ) : null}
            </>
          ) : null}
        </div>
      ) : (
        <p>Nothing is marked.</p>
      )}
      <div className="canon-voice">
        <label htmlFor="canon-voice">Voice</label>
        <select
          id="canon-voice"
          value={voiceURI ?? ""}
          onChange={(event) => setVoiceURI(event.target.value || null)}
        >
          <option value="">This device</option>
          {voices.map((voice) => (
            <option key={voice.voiceURI} value={voice.voiceURI}>
              {voice.name}
            </option>
          ))}
        </select>
        <p>
          Calm is the default. The rate is slower, the pitch is unchanged, and
          the device&apos;s own voice is used until you pick another English
          voice from this list. Nothing is spoken until Say it, or until Hear
          it on an answer.
        </p>
        <p>A voice made for this instrument is not made.</p>
        <p>
          The part that has to be heard before it can be decided is still open.
        </p>
      </div>
    </aside>
  );
}
