import assert from "node:assert/strict";
import test from "node:test";
import type { KeyValueStore } from "./safe-storage";
import { readKey, writeKey } from "./safe-storage";
import { createInitialState } from "./record";
import { loadFromStore, planSave, saveToStore } from "./storage";

function memoryStore(initial: string | null = null): KeyValueStore & { raw: string | null; writes: number } {
  return {
    raw: initial,
    writes: 0,
    getItem() {
      return this.raw;
    },
    setItem(_key: string, value: string) {
      this.writes += 1;
      this.raw = value;
    },
  };
}

test("a storage read or write that throws does not escape", () => {
  const store: KeyValueStore = {
    getItem() {
      throw new Error("SecurityError");
    },
    setItem() {
      throw new Error("QuotaExceededError");
    },
  };
  assert.deepEqual(readKey(store, "kanon-v1"), { ok: false });
  assert.equal(writeKey(store, "kanon-v1", "{}"), false);
  const loaded = loadFromStore(store);
  assert.equal(loaded.persist, false);
  assert.equal(loaded.storage, "unavailable");
  assert.match(loaded.notice ?? "", /did not open its storage/);
  const saved = saveToStore(store, createInitialState(), null, true);
  assert.deepEqual(saved, { ok: false, reason: "failed" });
});

test("a save does not overwrite a record another writer changed", () => {
  const store = memoryStore("{\"earlier\":true}");
  const blocked = saveToStore(store, createInitialState(), null);
  assert.equal(blocked.ok, false);
  if (!blocked.ok) {
    assert.equal(blocked.reason, "conflict");
  }
  assert.equal(store.writes, 0);
  assert.equal(store.raw, "{\"earlier\":true}");
  const forced = saveToStore(store, createInitialState(), null, true);
  assert.equal(forced.ok, true);
  assert.equal(store.writes, 1);
});

test("the first save writes, and a matching save does not write again", () => {
  const store = memoryStore(null);
  const first = saveToStore(store, createInitialState(), null);
  assert.equal(first.ok, true);
  assert.equal(store.writes, 1);
  const raw = first.ok ? first.raw : null;
  const second = saveToStore(store, createInitialState(), raw);
  assert.equal(second.ok, true);
  assert.equal(store.writes, 1);
  assert.equal(planSave("a", "b", "c"), "conflict");
  assert.equal(planSave("a", "a", "a"), "same");
  assert.equal(planSave(null, null, "{}"), "write");
});

test("malformed stored text is kept and is not overwritten by the load", () => {
  const store = memoryStore("{");
  const loaded = loadFromStore(store);
  assert.equal(loaded.storage, "unreadable");
  assert.equal(loaded.persist, false);
  assert.equal(loaded.raw, "{");
  assert.equal(store.raw, "{");
});
