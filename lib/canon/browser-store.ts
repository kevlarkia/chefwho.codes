import { loadStoredRecord, saveStoredRecord } from "./storage";
import { createInitialState } from "./record";
import type { RecordState } from "./types";

export type CanonSnapshot = {
  ready: boolean;
  notice: string | null;
  persist: boolean;
  state: RecordState;
};

const closed: CanonSnapshot = {
  ready: false,
  notice: null,
  persist: false,
  state: createInitialState(),
};

let snapshot: CanonSnapshot | null = null;
const listeners = new Set<() => void>();

function publish(next: CanonSnapshot) {
  snapshot = next;
  if (next.ready && next.persist && typeof window !== "undefined") {
    saveStoredRecord(next.state);
  }
  for (const listener of listeners) {
    listener();
  }
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
  if (!snapshot) {
    const loaded = loadStoredRecord();
    snapshot = {
      ready: true,
      notice: loaded.notice,
      persist: loaded.persist,
      state: loaded.state,
    };
  }
  return snapshot;
}

export function getCanonServerSnapshot(): CanonSnapshot {
  return closed;
}

export function replaceCanon(
  recipe: (current: CanonSnapshot) => CanonSnapshot,
): void {
  publish(recipe(getCanonSnapshot()));
}
