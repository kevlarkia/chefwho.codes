import { parseCopy, specimenIsLoad } from "./copy";
import { answerQuestion } from "./pipe";
import { dedupeCites, isSourceKind, isUsableStanding, weigh } from "./rule";
import { moveBook, seedShelf } from "./shelf";
import { specimenEntries, specimenSources } from "./specimen";
import type {
  BookPlace,
  Cite,
  Entry,
  JourneyEvent,
  JourneyKind,
  RecordState,
  Source,
  SourceKind,
} from "./types";

export function createInitialState(): RecordState {
  return {
    blanked: false,
    sources: specimenSources(),
    entries: specimenEntries(),
    talks: [],
    keepTalks: true,
    shelf: seedShelf(),
  };
}

function withId(prefix: string): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${prefix}-${Date.now()}`;
}

function event(
  id: string,
  at: string,
  kind: JourneyKind,
  note: string,
): JourneyEvent {
  return { id, at, kind, note };
}

export function resolveDisposition(
  entry: Entry,
  objective: boolean,
): Entry["disposition"] {
  if (entry.disposition === "disproved" || entry.disposition === "rejected") {
    return entry.disposition;
  }
  if (entry.humanHold && !objective) {
    return "subjective";
  }
  if (objective) {
    return "objective";
  }
  if (entry.disposition === "objective" || entry.disposition === "fallen") {
    return "fallen";
  }
  return "desk";
}

export function rerule(entry: Entry, sources: Source[], at: string): Entry {
  const weighing = weigh(entry.cites, sources);
  const next = resolveDisposition(entry, weighing.objective);
  if (next === entry.disposition) {
    return entry;
  }
  const journey = [...entry.journey];
  if (entry.disposition === "objective" && next === "fallen") {
    journey.push({
      id: withId("fell"),
      at,
      kind: "fell",
      note: "It fell when standing moved. It stays visible.",
    });
  }
  if (next === "objective" && entry.disposition !== "objective") {
    journey.push({
      id: withId("held"),
      at,
      kind: "held",
      note: "Held by the rule.",
    });
  }
  return { ...entry, disposition: next, journey };
}

export function setStanding(
  state: RecordState,
  sourceId: string,
  standing: number,
  note: string,
  at: string,
): RecordState {
  if (!isUsableStanding(standing)) {
    return state;
  }
  const sources = state.sources.map((source) => {
    if (source.id !== sourceId || source.standing === standing) {
      return source;
    }
    return {
      ...source,
      standing,
      history: [
        ...source.history,
        {
          at,
          standing,
          note: note.trim() || `Standing set to ${standing}.`,
        },
      ],
    };
  });
  const entries = state.entries.map((entry) => rerule(entry, sources, at));
  return { ...state, sources, entries };
}

export function addSource(
  state: RecordState,
  input: { name: string; kind: SourceKind; standing: number },
  at: string,
): RecordState {
  const name = input.name.trim();
  if (!name || !isUsableStanding(input.standing) || !isSourceKind(input.kind)) {
    return state;
  }
  const source: Source = {
    id: withId("src"),
    name,
    kind: input.kind,
    standing: input.standing,
    history: [
      {
        at,
        standing: input.standing,
        note: "Source entered. Sources are not deleted.",
      },
    ],
  };
  const sources = [...state.sources, source];
  const entries = state.entries.map((entry) => rerule(entry, sources, at));
  return { ...state, sources, entries };
}

export function addEntry(
  state: RecordState,
  input: { text: string; cites: Cite[] },
  at: string,
): RecordState {
  const text = input.text.trim();
  if (!text) {
    return state;
  }
  const draft: Entry = {
    id: withId("ent"),
    text,
    cites: dedupeCites(input.cites),
    disposition: "desk",
    humanHold: false,
    journey: [
      {
        id: withId("entered"),
        at,
        kind: "entered",
        note: "Entered. The ruling was shown before it was kept.",
      },
    ],
  };
  const ruled = rerule(draft, state.sources, at);
  return { ...state, entries: [...state.entries, ruled] };
}

export function reviseEntry(
  state: RecordState,
  entryId: string,
  text: string,
  at: string,
): RecordState {
  const nextText = text.trim();
  if (!nextText) {
    return state;
  }
  const entries = state.entries.map((entry) => {
    if (entry.id !== entryId || entry.text === nextText) {
      return entry;
    }
    const revised: Entry = {
      ...entry,
      text: nextText,
      journey: [
        ...entry.journey,
        {
          id: withId("revised"),
          at,
          kind: "revised",
          note: `Wording revised. The earlier wording stays: ${entry.text}`,
        },
      ],
    };
    return rerule(revised, state.sources, at);
  });
  return { ...state, entries };
}

export function doubtEntry(
  state: RecordState,
  entryId: string,
  note: string,
  at: string,
): RecordState {
  const text = note.trim();
  if (!text) {
    return state;
  }
  const entries = state.entries.map((entry) => {
    if (entry.id !== entryId) {
      return entry;
    }
    return {
      ...entry,
      journey: [
        ...entry.journey,
        event(withId("doubt"), at, "doubt", text),
      ],
    };
  });
  return { ...state, entries };
}

export function verifyEntry(
  state: RecordState,
  entryId: string,
  at: string,
): RecordState {
  const entries = state.entries.map((entry) => {
    if (entry.id !== entryId) {
      return entry;
    }
    if (entry.disposition === "disproved" || entry.disposition === "rejected") {
      return entry;
    }
    const weighing = weigh(entry.cites, state.sources);
    if (weighing.objective) {
      return {
        ...entry,
        journey: [
          ...entry.journey,
          event(
            withId("verified"),
            at,
            "verified",
            "You verified it. The rule already holds it. Verification does not make a second kind of proof.",
          ),
        ],
      };
    }
    return {
      ...entry,
      humanHold: true,
      disposition: "subjective" as const,
      journey: [
        ...entry.journey,
        event(
          withId("verified"),
          at,
          "verified",
          "You hold it. It stays subjective. Verification is not proof.",
        ),
      ],
    };
  });
  return { ...state, entries };
}

export function rejectEntry(
  state: RecordState,
  entryId: string,
  at: string,
): RecordState {
  const entries = state.entries.map((entry) => {
    if (entry.id !== entryId) {
      return entry;
    }
    if (
      entry.disposition === "objective" ||
      entry.disposition === "disproved" ||
      entry.disposition === "rejected"
    ) {
      return entry;
    }
    return {
      ...entry,
      humanHold: false,
      disposition: "rejected" as const,
      journey: [
        ...entry.journey,
        event(withId("rejected"), at, "rejected", "Rejected, and kept."),
      ],
    };
  });
  return { ...state, entries };
}

export function disproveEntry(
  state: RecordState,
  entryId: string,
  note: string,
  at: string,
): RecordState {
  const entries = state.entries.map((entry) => {
    if (entry.id !== entryId || entry.disposition === "disproved") {
      return entry;
    }
    const reason = note.trim();
    return {
      ...entry,
      humanHold: false,
      disposition: "disproved" as const,
      journey: [
        ...entry.journey,
        event(
          withId("disproved"),
          at,
          "disproved",
          reason ? `Disproved, and kept. ${reason}` : "Disproved, and kept.",
        ),
      ],
    };
  });
  return { ...state, entries };
}

export function setKeepTalks(state: RecordState, keepTalks: boolean): RecordState {
  return { ...state, keepTalks };
}

export function ask(
  state: RecordState,
  question: string,
  at: string,
): { state: RecordState; lines: string[]; stored: boolean } {
  const lines = answerQuestion(question, state.entries, state.sources);
  if (lines.length === 0 || !state.keepTalks) {
    return { state, lines, stored: false };
  }
  return {
    state: {
      ...state,
      talks: [
        ...state.talks,
        {
          id: withId("talk"),
          at,
          question: question.trim(),
          lines,
          synopsis: "",
        },
      ],
    },
    lines,
    stored: true,
  };
}

export function keepAnswer(
  state: RecordState,
  question: string,
  lines: string[],
  at: string,
): RecordState {
  if (lines.length === 0) {
    return state;
  }
  return {
    ...state,
    talks: [
      ...state.talks,
      {
        id: withId("talk"),
        at,
        question: question.trim(),
        lines,
        synopsis: "",
      },
    ],
  };
}

export function setSynopsis(
  state: RecordState,
  talkId: string,
  synopsis: string,
): RecordState {
  return {
    ...state,
    talks: state.talks.map((talk) =>
      talk.id === talkId ? { ...talk, synopsis } : talk,
    ),
  };
}

export function placeBook(
  state: RecordState,
  bookId: string,
  place: BookPlace,
): RecordState {
  return { ...state, shelf: moveBook(state.shelf, bookId, place) };
}

export function blankRecord(state: RecordState): RecordState {
  return {
    ...state,
    blanked: true,
    sources: [],
    entries: [],
  };
}

export function loadSpecimen(state: RecordState): RecordState {
  if (state.sources.length > 0 || state.entries.length > 0) {
    return state;
  }
  return {
    ...state,
    blanked: false,
    sources: specimenSources(),
    entries: specimenEntries(),
  };
}

export function importRecord(state: RecordState, value: unknown): RecordState | null {
  const parsed = parseCopy(value);
  if (!parsed.ok) {
    return null;
  }
  return {
    ...state,
    blanked: parsed.copy.blanked,
    sources: parsed.copy.sources,
    entries: parsed.copy.entries,
  };
}

export function recordIsSpecimen(state: RecordState): boolean {
  return specimenIsLoad(state.sources, state.entries);
}
