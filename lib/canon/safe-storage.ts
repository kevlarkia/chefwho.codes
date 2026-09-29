export type KeyValueStore = {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
};

export type StorageRead =
  | { ok: true; value: string | null }
  | { ok: false };

export function readKey(store: KeyValueStore, key: string): StorageRead {
  try {
    return { ok: true, value: store.getItem(key) };
  } catch {
    return { ok: false };
  }
}

export function writeKey(
  store: KeyValueStore,
  key: string,
  value: string,
): boolean {
  try {
    store.setItem(key, value);
    return true;
  } catch {
    return false;
  }
}

export function openLocalStorage(): {
  store: KeyValueStore | null;
  blocked: boolean;
} {
  try {
    if (typeof localStorage === "undefined") {
      return { store: null, blocked: false };
    }
    return { store: localStorage, blocked: false };
  } catch {
    return { store: null, blocked: true };
  }
}
