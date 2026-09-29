import assert from "node:assert/strict";
import test from "node:test";
import { exportCopy, parseCopy } from "./copy";
import { HELD_WORDS, lookupHeld } from "./held-words";
import {
  NOT_IN_RECORD,
  answerQuestion,
  guardRephrase,
} from "./pipe";
import { mapDictionaryPayload, presentReader } from "./reader";
import {
  ask,
  blankRecord,
  createInitialState,
  disproveEntry,
  loadSpecimen,
  placeBook,
  rejectEntry,
  setKeepTalks,
  setStanding,
  verifyEntry,
} from "./record";
import { barFor, canCarry, weigh } from "./rule";
import { booksIn, seedShelf } from "./shelf";
import { specimenEntries, specimenSources } from "./specimen";
import type { Source } from "./types";

function source(
  id: string,
  kind: Source["kind"],
  standing: number,
): Source {
  return {
    id,
    name: id,
    kind,
    standing,
    history: [],
  };
}

test("the bar uses the young bar, then the middle, held between 58 and 80", () => {
  assert.equal(barFor([]), 64);
  assert.equal(barFor([source("a", "record", 90), source("b", "record", 90)]), 64);
  assert.equal(
    barFor([
      source("a", "record", 90),
      source("b", "record", 90),
      source("c", "record", 90),
    ]),
    80,
  );
  assert.equal(
    barFor([
      source("a", "record", 52),
      source("b", "record", 52),
      source("c", "record", 52),
    ]),
    58,
  );
  assert.equal(
    barFor([
      source("a", "record", 50),
      source("b", "record", 60),
      source("c", "record", 70),
      source("d", "record", 80),
    ]),
    65,
  );
});

test("primary and record carry, a witness carries only at 70, and the rest inform", () => {
  assert.equal(canCarry(source("p", "primary", 10)), true);
  assert.equal(canCarry(source("r", "record", 10)), true);
  assert.equal(canCarry(source("w", "witness", 70)), true);
  assert.equal(canCarry(source("w", "witness", 69)), false);
  assert.equal(canCarry(source("press", "press", 90)), false);
  assert.equal(canCarry(source("self", "self", 90)), false);
  assert.equal(canCarry(source("hear", "hearsay", 90)), false);
});

test("support from a carrier adds full standing, inform adds a quarter, and a contest subtracts full standing", () => {
  const sources = [
    source("record", "record", 80),
    source("press", "press", 58),
    source("hear", "hearsay", 40),
    source("seasoned-a", "primary", 60),
    source("seasoned-b", "primary", 60),
  ];
  const weighing = weigh(
    [
      { sourceId: "record", role: "support" },
      { sourceId: "press", role: "support" },
      { sourceId: "hear", role: "contest" },
    ],
    sources,
  );
  assert.equal(weighing.support, 80 + 14.5);
  assert.equal(weighing.contest, 40);
  assert.equal(weighing.carriers, 1);
  assert.equal(weighing.net, 80 + 14.5 - 40);
});

test("a close, strong contest is a fight and is not objective", () => {
  const sources = [
    source("support", "primary", 140),
    source("contest", "primary", 80),
    source("a", "record", 60),
    source("b", "record", 60),
    source("c", "record", 60),
  ];
  const blocked = weigh(
    [
      { sourceId: "support", role: "support" },
      { sourceId: "contest", role: "contest" },
    ],
    sources,
  );
  assert.equal(blocked.bar, 60);
  assert.equal(blocked.net, 60);
  assert.equal(blocked.fight, true);
  assert.equal(blocked.objective, false);

  const clear = weigh([{ sourceId: "support", role: "support" }], sources);
  assert.equal(clear.fight, false);
  assert.equal(clear.objective, true);
});

test("a contest below the floor does not become a fight", () => {
  const sources = [
    source("support", "primary", 114),
    source("contest", "hearsay", 50),
    source("b", "record", 64),
    source("c", "record", 64),
  ];
  const weighing = weigh(
    [
      { sourceId: "support", role: "support" },
      { sourceId: "contest", role: "contest" },
    ],
    sources,
  );
  assert.equal(weighing.bar, 64);
  assert.equal(weighing.net, 64);
  assert.equal(weighing.fight, false);
  assert.equal(weighing.objective, true);
});

test("the specimen rulings match the handoff", () => {
  const sources = specimenSources();
  const entries = specimenEntries();
  const byId = Object.fromEntries(entries.map((item) => [item.id, item]));
  const bodleian = weigh(byId["ent-bodleian"].cites, sources);
  assert.equal(bodleian.objective, true);
  assert.equal(bodleian.carriers, 1);
  assert.equal(byId["ent-bodleian"].disposition, "objective");

  const roots = weigh(byId["ent-canon-cannon"].cites, sources);
  assert.equal(roots.objective, false);
  assert.equal(roots.fight, false);
  assert.equal(byId["ent-canon-cannon"].disposition, "desk");

  const scroll = weigh(byId["ent-long-scroll"].cites, sources);
  assert.equal(scroll.carriers, 0);
  assert.equal(scroll.objective, false);
  assert.equal(byId["ent-long-scroll"].humanHold, true);
  assert.equal(byId["ent-long-scroll"].disposition, "subjective");

  const narrow = weigh(byId["ent-colophon-narrow"].cites, sources);
  assert.equal(narrow.objective, false);
  assert.equal(byId["ent-colophon-narrow"].disposition, "fallen");

  assert.equal(byId["ent-colophon-always"].disposition, "disproved");
  assert.equal(byId["ent-q-spelling"].disposition, "rejected");
  assert.equal(
    sources.find((item) => item.id === "src-colophon-index")?.standing,
    57,
  );
});

test("a disproof stays when standing rises, and a human hold stays when standing falls", () => {
  const state = createInitialState();
  const raised = setStanding(state, "src-colophon-index", 81, "Raised.", "2026-09-29T00:00:00.000Z");
  const always = raised.entries.find((item) => item.id === "ent-colophon-always");
  assert.equal(always?.disposition, "disproved");
  const narrow = raised.entries.find((item) => item.id === "ent-colophon-narrow");
  assert.equal(narrow?.disposition, "objective");
  assert.ok(narrow?.journey.some((event) => event.kind === "fell"));
  assert.ok(narrow?.journey.some((event) => event.kind === "held"));

  const dropped = setStanding(
    state,
    "src-reading-journal",
    10,
    "Lowered.",
    "2026-09-29T00:00:00.000Z",
  );
  const scroll = dropped.entries.find((item) => item.id === "ent-long-scroll");
  assert.equal(scroll?.disposition, "subjective");
  assert.equal(scroll?.humanHold, true);
});

test("reject does not uncanonize a rule hold", () => {
  const state = createInitialState();
  const rejected = rejectEntry(state, "ent-bodleian", "2026-09-29T00:00:00.000Z");
  assert.equal(
    rejected.entries.find((item) => item.id === "ent-bodleian")?.disposition,
    "objective",
  );
  const disproved = disproveEntry(
    state,
    "ent-bodleian",
    "A later document contests the day.",
    "2026-09-29T00:00:00.000Z",
  );
  const bodleian = disproved.entries.find((item) => item.id === "ent-bodleian");
  assert.equal(bodleian?.disposition, "disproved");
  assert.ok(bodleian?.journey.some((event) => event.note.includes("8 November 1602") || event.kind === "disproved"));
});

test("verify on a desk item stays subjective", () => {
  const state = createInitialState();
  const next = verifyEntry(state, "ent-canon-cannon", "2026-09-29T00:00:00.000Z");
  const roots = next.entries.find((item) => item.id === "ent-canon-cannon");
  assert.equal(roots?.disposition, "subjective");
  assert.equal(roots?.humanHold, true);
});

test("ask closes on the specimen and does not answer an empty question", () => {
  const state = createInitialState();
  assert.deepEqual(answerQuestion("", state.entries, state.sources), []);
  assert.deepEqual(answerQuestion("   ", state.entries, state.sources), []);
  const bodleian = answerQuestion(
    "When did the Bodleian open to readers?",
    state.entries,
    state.sources,
  );
  assert.equal(bodleian.length, 1);
  assert.match(bodleian[0], /8 November 1602/);
  assert.match(bodleian[0], /Held by the rule/);
  const roots = answerQuestion(
    "Do canon and cannon share a root?",
    state.entries,
    state.sources,
  );
  assert.equal(roots.length, 1);
  assert.match(roots[0], /Not canon/);
  assert.deepEqual(
    answerQuestion("What is the capital of France?", state.entries, state.sources),
    [NOT_IN_RECORD],
  );
});

test("a model phrase that adds a content word is dropped", () => {
  const lines = [
    "The Bodleian Library opened to readers on 8 November 1602. Held by the rule.",
  ];
  const question = "When did the Bodleian open to readers?";
  assert.deepEqual(
    guardRephrase(
      "The Bodleian Library opened to readers on 8 November 1602 in France. Held by the rule.",
      lines,
      question,
      "",
    ),
    lines,
  );
  const kept = guardRephrase(
    "The Bodleian Library opened to readers on 8 November 1602. Held by the rule about that.",
    lines,
    question,
    "",
  );
  assert.equal(kept.length, 1);
  assert.match(kept[0], /about/);
});

test("held words are not overwritten by the wider base", () => {
  const wider = {
    answered: true as const,
    definitions: ["A different definition."],
    origin: "A different origin.",
    audioUrl: "https://example.com/canon.mp3",
  };
  const view = presentReader("Canon", wider);
  assert.equal(view.status, "held");
  assert.equal(view.marker, "Held here.");
  assert.deepEqual(view.definitions, [HELD_WORDS.canon.definition]);
  assert.equal(view.origin, HELD_WORDS.canon.origin);
  assert.equal(view.audioUrl, null);
  assert.equal(lookupHeld("readers")?.definition, HELD_WORDS.reader.definition);
});

test("a wider base that does not answer is unreachable, and a missing origin is said", () => {
  const missed = presentReader("serendipity", { answered: false });
  assert.equal(missed.status, "unreachable");
  assert.match(missed.marker, /unreachable/);
  assert.doesNotMatch(missed.marker, /unknown/i);

  const noOrigin = presentReader("serendipity", {
    answered: true,
    definitions: ["A happy accident."],
  });
  assert.equal(noOrigin.status, "wider");
  assert.equal(noOrigin.marker, "From the wider base.");
  assert.equal(noOrigin.originMissing, true);

  const withAudio = presentReader("serendipity", {
    answered: true,
    definitions: ["A happy accident."],
    origin: "https://example.com/serendipity",
    audioUrl: "http://example.com/nope.mp3",
  });
  assert.equal(withAudio.audioUrl, null);
  assert.equal(withAudio.origin, "https://example.com/serendipity");

  const secure = presentReader("serendipity", {
    answered: true,
    definitions: ["A happy accident."],
    audioUrl: "https://example.com/yes.mp3",
  });
  assert.equal(secure.audioUrl, "https://example.com/yes.mp3");
});

test("a long selection is not sent to the wider base", () => {
  const view = presentReader("one two three four five", {
    answered: true,
    definitions: ["Should not be used."],
  });
  assert.equal(view.status, "too-long");
  assert.equal(view.definitions.length, 0);
});

test("dictionary payload keeps returned definitions and drops a non-https recording", () => {
  const mapped = mapDictionaryPayload([
    {
      meanings: [{ definitions: [{ definition: "A kept sentence." }] }],
      sourceUrls: ["https://example.com/word"],
      phonetics: [{ audio: "http://example.com/word.mp3" }, { audio: "https://example.com/word.mp3" }],
    },
  ]);
  assert.equal(mapped.answered, true);
  if (mapped.answered) {
    assert.deepEqual(mapped.definitions, ["A kept sentence."]);
    assert.match(mapped.origin ?? "", /https:\/\/example.com\/word/);
    assert.equal(mapped.audioUrl, "https://example.com/word.mp3");
  }
  assert.deepEqual(mapDictionaryPayload({ title: "No Definitions Found" }), {
    answered: false,
  });
});

test("a copy holds sources and entries, not the shelf or the talks", () => {
  const state = createInitialState();
  const asked = ask(state, "When did the Bodleian open to readers?", "2026-09-29T00:00:00.000Z");
  assert.equal(asked.stored, true);
  const copy = exportCopy(state.sources, state.entries, state.blanked);
  assert.equal(copy.kind, "kanon-copy");
  assert.equal(copy.specimenIsLoad, true);
  assert.equal("talks" in copy, false);
  assert.equal("shelf" in copy, false);
  assert.equal("voice" in copy, false);
  const parsed = parseCopy(JSON.parse(JSON.stringify(copy)));
  assert.equal(parsed.ok, true);
  if (parsed.ok) {
    assert.equal(parsed.copy.entries.length, state.entries.length);
  }
  assert.equal(parseCopy({ kind: "other" }).ok, false);
});

test("blanking clears the record and leaves the shelf and the talks", () => {
  const state = ask(
    createInitialState(),
    "When did the Bodleian open to readers?",
    "2026-09-29T00:00:00.000Z",
  ).state;
  const blanked = blankRecord(state);
  assert.equal(blanked.sources.length, 0);
  assert.equal(blanked.entries.length, 0);
  assert.equal(blanked.blanked, true);
  assert.equal(blanked.talks.length, state.talks.length);
  assert.equal(blanked.shelf.length, state.shelf.length);
  const restored = loadSpecimen(blanked);
  assert.equal(restored.entries.length > 0, true);
  assert.equal(restored.talks.length, state.talks.length);
});

test("turning talks off does not erase what is kept", () => {
  const state = ask(
    createInitialState(),
    "When did the Bodleian open to readers?",
    "2026-09-29T00:00:00.000Z",
  ).state;
  const off = setKeepTalks(state, false);
  assert.equal(off.talks.length, 1);
  const again = ask(off, "Do canon and cannon share a root?", "2026-09-29T00:01:00.000Z");
  assert.equal(again.stored, false);
  assert.equal(again.state.talks.length, 1);
  assert.match(again.lines[0], /Not canon/);
});

test("moving a book does not remove it from the shelf", () => {
  const shelf = seedShelf();
  const before = shelf.length;
  const moved = placeBook(
    { ...createInitialState(), shelf },
    "book-meditations",
    "read",
  ).shelf;
  assert.equal(moved.length, before);
  assert.equal(moved.find((book) => book.id === "book-meditations")?.place, "read");
  assert.equal(booksIn(moved, "read").some((book) => book.title === "Meditations"), true);
  assert.equal(
    shelf.some((book) => book.title === "HBR Guide to Your Personal Growth"),
    false,
  );
  assert.equal(
    shelf.find((book) => book.id === "book-bitcoin-starting")?.title,
    "A starting book on Bitcoin",
  );
  const greene = shelf.filter((book) => book.author === "Robert Greene");
  assert.deepEqual(
    greene.map((book) => book.title).sort(),
    [
      "The 33 Strategies of War",
      "The 48 Laws of Power",
      "The Art of Seduction",
    ],
  );
});

test("an empty record can load the specimen, and a filled record is not replaced", () => {
  const empty = blankRecord(createInitialState());
  const loaded = loadSpecimen(empty);
  assert.equal(loaded.sources.length > 0, true);
  const filled = createInitialState();
  assert.equal(loadSpecimen(filled), filled);
});
