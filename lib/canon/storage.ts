import { parseCopy } from "./copy";
import { createInitialState } from "./record";
import type { Book, BookPlace, RecordState, Talk } from "./types";
import { COPY_KIND, RECORD_STORAGE_KEY } from "./types";

export type StoredLoad = {
  state: RecordState;
  persist: boolean;
  notice: string | null;
};

const UNREADABLE =
  "The record stored in this browser could not be read. Nothing has been written over it.";

function isBookPlace(value: unknown): value is BookPlace {
  return value === "read" || value === "to-get";
}

function parseShelf(value: unknown): Book[] | null {
  if (!Array.isArray(value)) {
    return null;
  }
  const shelf: Book[] = [];
  for (const item of value) {
    if (!item || typeof item !== "object") {
      return null;
    }
    const book = item as Record<string, unknown>;
    if (typeof book.id !== "string" || typeof book.title !== "string") {
      return null;
    }
    if (typeof book.author !== "string" || !isBookPlace(book.place)) {
      return null;
    }
    if (book.note !== undefined && typeof book.note !== "string") {
      return null;
    }
    shelf.push({
      id: book.id,
      title: book.title,
      author: book.author,
      place: book.place,
      note: book.note,
    });
  }
  return shelf;
}

function parseTalks(value: unknown): Talk[] | null {
  if (!Array.isArray(value)) {
    return null;
  }
  const talks: Talk[] = [];
  for (const item of value) {
    if (!item || typeof item !== "object") {
      return null;
    }
    const talk = item as Record<string, unknown>;
    if (typeof talk.id !== "string" || typeof talk.at !== "string") {
      return null;
    }
    if (typeof talk.question !== "string" || typeof talk.synopsis !== "string") {
      return null;
    }
    if (!Array.isArray(talk.lines) || talk.lines.some((line) => typeof line !== "string")) {
      return null;
    }
    talks.push({
      id: talk.id,
      at: talk.at,
      question: talk.question,
      synopsis: talk.synopsis,
      lines: talk.lines as string[],
    });
  }
  return talks;
}

export function parseStoredRecord(raw: string): RecordState | null {
  const value: unknown = JSON.parse(raw);
  if (!value || typeof value !== "object") {
    return null;
  }
  const stored = value as Record<string, unknown>;
  const parsed = parseCopy({
    kind: COPY_KIND,
    blanked: stored.blanked === true,
    specimenIsLoad: false,
    sources: stored.sources,
    entries: stored.entries,
  });
  if (!parsed.ok) {
    return null;
  }
  const shelf = parseShelf(stored.shelf);
  const talks = parseTalks(stored.talks);
  if (!shelf || !talks) {
    return null;
  }
  return {
    blanked: stored.blanked === true,
    sources: parsed.copy.sources,
    entries: parsed.copy.entries,
    talks,
    keepTalks: stored.keepTalks !== false,
    shelf,
  };
}

export function loadStoredRecord(): StoredLoad {
  if (typeof localStorage === "undefined") {
    return { state: createInitialState(), persist: false, notice: null };
  }
  const raw = localStorage.getItem(RECORD_STORAGE_KEY);
  if (raw === null) {
    return { state: createInitialState(), persist: true, notice: null };
  }
  try {
    const state = parseStoredRecord(raw);
    if (!state) {
      return { state: createInitialState(), persist: false, notice: UNREADABLE };
    }
    return { state, persist: true, notice: null };
  } catch {
    return { state: createInitialState(), persist: false, notice: UNREADABLE };
  }
}

export function saveStoredRecord(state: RecordState): void {
  if (typeof localStorage === "undefined") {
    return;
  }
  localStorage.setItem(RECORD_STORAGE_KEY, JSON.stringify(state));
}
