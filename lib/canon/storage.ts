import { parseCopy } from "./copy";
import { createInitialState } from "./record";
import { openLocalStorage, readKey, writeKey, type KeyValueStore } from "./safe-storage";
import type { Book, BookPlace, RecordState, Talk } from "./types";
import { COPY_KIND, RECORD_STORAGE_KEY } from "./types";

export type StorageCondition = "ok" | "unreadable" | "unavailable" | "write-failed" | "conflict";

export type StoredLoad = {
  state: RecordState;
  persist: boolean;
  notice: string | null;
  raw: string | null;
  storage: StorageCondition;
};

export type SaveResult =
  | { ok: true; raw: string }
  | { ok: false; reason: "conflict" | "failed" | "unavailable" };

const UNREADABLE =
  "The record stored in this browser could not be read. Nothing has been written over it.";

export const STORAGE_UNAVAILABLE =
  "This browser did not open its storage. The record on screen stays in this tab.";

export const STORAGE_WRITE_FAILED =
  "The record could not be written in this browser. What is on screen stays here. The stored text was left as it was.";

export const STORAGE_CONFLICT =
  "Another tab wrote the record. This tab did not overwrite it.";

export function planSave(
  expectedRaw: string | null,
  currentRaw: string | null,
  nextRaw: string,
): "write" | "conflict" | "same" {
  if (currentRaw === nextRaw) {
    return "same";
  }
  if (currentRaw !== expectedRaw) {
    return "conflict";
  }
  return "write";
}

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

function emptyLoad(
  notice: string | null,
  storage: StorageCondition,
  persist: boolean,
): StoredLoad {
  return {
    state: createInitialState(),
    persist,
    notice,
    raw: null,
    storage,
  };
}

export function loadFromStore(store: KeyValueStore): StoredLoad {
  const read = readKey(store, RECORD_STORAGE_KEY);
  if (!read.ok) {
    return emptyLoad(STORAGE_UNAVAILABLE, "unavailable", false);
  }
  if (read.value === null) {
    return {
      state: createInitialState(),
      persist: true,
      notice: null,
      raw: null,
      storage: "ok",
    };
  }
  try {
    const state = parseStoredRecord(read.value);
    if (!state) {
      return {
        state: createInitialState(),
        persist: false,
        notice: UNREADABLE,
        raw: read.value,
        storage: "unreadable",
      };
    }
    return {
      state,
      persist: true,
      notice: null,
      raw: read.value,
      storage: "ok",
    };
  } catch {
    return {
      state: createInitialState(),
      persist: false,
      notice: UNREADABLE,
      raw: read.value,
      storage: "unreadable",
    };
  }
}

export function loadStoredRecord(): StoredLoad {
  const opened = openLocalStorage();
  if (!opened.store) {
    return emptyLoad(opened.blocked ? STORAGE_UNAVAILABLE : null, opened.blocked ? "unavailable" : "ok", false);
  }
  return loadFromStore(opened.store);
}

export function saveToStore(
  store: KeyValueStore,
  state: RecordState,
  expectedRaw: string | null,
  force = false,
): SaveResult {
  let nextRaw: string;
  try {
    nextRaw = JSON.stringify(state);
  } catch {
    return { ok: false, reason: "failed" };
  }
  const current = readKey(store, RECORD_STORAGE_KEY);
  if (!current.ok) {
    return { ok: false, reason: "failed" };
  }
  const plan = planSave(expectedRaw, current.value, nextRaw);
  if (plan === "same") {
    return { ok: true, raw: current.value ?? nextRaw };
  }
  if (plan === "conflict" && !force) {
    return { ok: false, reason: "conflict" };
  }
  if (!writeKey(store, RECORD_STORAGE_KEY, nextRaw)) {
    return { ok: false, reason: "failed" };
  }
  return { ok: true, raw: nextRaw };
}

export function saveStoredRecord(
  state: RecordState,
  expectedRaw: string | null,
  force = false,
): SaveResult {
  const opened = openLocalStorage();
  if (!opened.store) {
    return { ok: false, reason: "unavailable" };
  }
  return saveToStore(opened.store, state, expectedRaw, force);
}
