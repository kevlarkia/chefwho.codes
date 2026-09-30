import { createInitialState } from "./record";
import {
  STORAGE_CONFLICT,
  STORAGE_WRITE_FAILED,
  loadStoredRecord,
  parseStoredRecord,
  saveStoredRecord,
  type StorageCondition,
} from "./storage";
import type { RecordState } from "./types";
import { RECORD_STORAGE_KEY } from "./types";

export type CanonSnapshot = {
  ready: boolean;
  notice: string | null;
  persist: boolean;
  state: RecordState;
  seenRaw: string | null;
  storage: StorageCondition;
};

const closed: CanonSnapshot = {
  ready: false,
  notice: null,
  persist: false,
  state: createInitialState(),
  seenRaw: null,
  storage: "ok",
};

let snapshot: CanonSnapshot | null = null;
let listening = false;
const listeners = new Set<() => void>();

function emit() {
  for (const listener of listeners) {
    listener();
  }
}

function publish(next: CanonSnapshot, force = false) {
  let saved = next;
  if (next.ready && next.persist && typeof window !== "undefined") {
    const result = saveStoredRecord(next.state, next.seenRaw, force);
    if (result.ok) {
      saved = {
        ...next,
        seenRaw: result.raw,
        notice: null,
        storage: "ok",
        persist: true,
      };
    } else if (result.reason === "conflict") {
      saved = {
        ...next,
        persist: false,
        storage: "conflict",
        notice: STORAGE_CONFLICT,
      };
    } else {
      saved = {
        ...next,
        persist: false,
        storage: result.reason === "unavailable" ? "unavailable" : "write-failed",
        notice: STORAGE_WRITE_FAILED,
      };
    }
  }
  snapshot = saved;
  emit();
}

function onStorage(event: StorageEvent) {
  if (event.key !== RECORD_STORAGE_KEY || event.newValue === null) {
    return;
  }
  const current = snapshot;
  if (!current?.persist) {
    return;
  }
  let state: RecordState | null = null;
  try {
    state = parseStoredRecord(event.newValue);
  } catch {
    state = null;
  }
  if (!state) {
    return;
  }
  snapshot = {
    ...current,
    state,
    seenRaw: event.newValue,
    notice: null,
    storage: "ok",
    persist: true,
  };
  emit();
}

function ensureListening() {
  if (listening || typeof window === "undefined") {
    return;
  }
  listening = true;
  window.addEventListener("storage", onStorage);
}

export function subscribeCanon(listener: () => void): () => void {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

export function getCanonSnapshot(): CanonSnapshot {
  if (typeof window === "undefined") {
    return closed;
  }
  ensureListening();
  if (!snapshot) {
    const loaded = loadStoredRecord();
    snapshot = {
      ready: true,
      notice: loaded.notice,
      persist: loaded.persist,
      state: loaded.state,
      seenRaw: loaded.raw,
      storage: loaded.storage,
    };
  }
  return snapshot;
}

export function getCanonServerSnapshot(): CanonSnapshot {
  return closed;
}

export function replaceCanon(
  recipe: (current: CanonSnapshot) => CanonSnapshot,
  options?: { force?: boolean },
): void {
  publish(recipe(getCanonSnapshot()), options?.force === true);
}

export function adoptStoredRecord(): void {
  const loaded = loadStoredRecord();
  snapshot = {
    ready: true,
    notice: loaded.notice,
    persist: loaded.persist,
    state: loaded.state,
    seenRaw: loaded.raw,
    storage: loaded.storage,
  };
  emit();
}
