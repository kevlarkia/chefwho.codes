"use client";

import {
  createContext,
  useContext,
  useMemo,
  useSyncExternalStore,
  type ReactNode,
} from "react";
import {
  getCanonServerSnapshot,
  getCanonSnapshot,
  replaceCanon,
  subscribeCanon,
} from "@/lib/canon/browser-store";
import { parseCopy } from "@/lib/canon/copy";
import {
  addEntry as addEntryToRecord,
  addSource as addSourceToRecord,
  ask as askRecord,
  blankRecord as blankRecordState,
  disproveEntry,
  doubtEntry,
  keepAnswer as keepAnswerOnRecord,
  loadSpecimen as loadSpecimenState,
  placeBook as placeBookOnRecord,
  recordIsSpecimen,
  rejectEntry,
  reviseEntry,
  setKeepTalks as setKeepTalksOnRecord,
  setStanding as setStandingOnRecord,
  setSynopsis as setSynopsisOnRecord,
  verifyEntry,
} from "@/lib/canon/record";
import type {
  BookPlace,
  Cite,
  RecordState,
  SourceKind,
} from "@/lib/canon/types";

type AskResult = {
  lines: string[];
  stored: boolean;
};

type CanonContextValue = {
  ready: boolean;
  notice: string | null;
  state: RecordState;
  specimenIsLoad: boolean;
  acceptStoredReplacement: () => void;
  setStanding: (id: string, standing: number, note: string) => void;
  addSource: (input: { name: string; kind: SourceKind; standing: number }) => void;
  addEntry: (input: { text: string; cites: Cite[] }) => void;
  revise: (id: string, text: string) => void;
  doubt: (id: string, note: string) => void;
  verify: (id: string) => void;
  reject: (id: string) => void;
  disprove: (id: string, note: string) => void;
  setKeepTalks: (on: boolean) => void;
  askQuestion: (question: string) => AskResult;
  keepThisAnswer: (question: string, lines: string[]) => void;
  setSynopsis: (id: string, synopsis: string) => void;
  placeBook: (id: string, place: BookPlace) => void;
  blankThisBrowser: () => void;
  loadSpecimen: () => void;
  importCopy: (value: unknown) => string | null;
};

const CanonContext = createContext<CanonContextValue | null>(null);

function now(): string {
  return new Date().toISOString();
}

function withState(
  recipe: (state: RecordState) => RecordState,
): void {
  replaceCanon((current) => ({ ...current, state: recipe(current.state) }));
}

export function CanonProvider({ children }: { children: ReactNode }) {
  const snapshot = useSyncExternalStore(
    subscribeCanon,
    getCanonSnapshot,
    getCanonServerSnapshot,
  );

  const value = useMemo<CanonContextValue>(
    () => ({
      ready: snapshot.ready,
      notice: snapshot.notice,
      state: snapshot.state,
      specimenIsLoad: recordIsSpecimen(snapshot.state),
      acceptStoredReplacement: () => {
        replaceCanon((current) => ({
          ...current,
          notice: null,
          persist: true,
        }));
      },
      setStanding: (id, standing, note) => {
        withState((state) => setStandingOnRecord(state, id, standing, note, now()));
      },
      addSource: (input) => {
        withState((state) => addSourceToRecord(state, input, now()));
      },
      addEntry: (input) => {
        withState((state) => addEntryToRecord(state, input, now()));
      },
      revise: (id, text) => {
        withState((state) => reviseEntry(state, id, text, now()));
      },
      doubt: (id, note) => {
        withState((state) => doubtEntry(state, id, note, now()));
      },
      verify: (id) => {
        withState((state) => verifyEntry(state, id, now()));
      },
      reject: (id) => {
        withState((state) => rejectEntry(state, id, now()));
      },
      disprove: (id, note) => {
        withState((state) => disproveEntry(state, id, note, now()));
      },
      setKeepTalks: (on) => {
        withState((state) => setKeepTalksOnRecord(state, on));
      },
      askQuestion: (question) => {
        let result: AskResult = { lines: [], stored: false };
        replaceCanon((current) => {
          const next = askRecord(current.state, question, now());
          result = { lines: next.lines, stored: next.stored };
          return { ...current, state: next.state };
        });
        return result;
      },
      keepThisAnswer: (question, lines) => {
        withState((state) => keepAnswerOnRecord(state, question, lines, now()));
      },
      setSynopsis: (id, synopsis) => {
        withState((state) => setSynopsisOnRecord(state, id, synopsis));
      },
      placeBook: (id, place) => {
        withState((state) => placeBookOnRecord(state, id, place));
      },
      blankThisBrowser: () => {
        withState((state) => blankRecordState(state));
      },
      loadSpecimen: () => {
        withState((state) => loadSpecimenState(state));
      },
      importCopy: (imported) => {
        const parsed = parseCopy(imported);
        if (!parsed.ok) {
          return parsed.reason;
        }
        replaceCanon((current) => ({
          ...current,
          state: {
            ...current.state,
            blanked: parsed.copy.blanked,
            sources: parsed.copy.sources,
            entries: parsed.copy.entries,
          },
        }));
        return null;
      },
    }),
    [snapshot],
  );

  return <CanonContext.Provider value={value}>{children}</CanonContext.Provider>;
}

export function useCanon(): CanonContextValue {
  const value = useContext(CanonContext);
  if (!value) {
    throw new Error("Canon is only available inside the Canon instrument.");
  }
  return value;
}
