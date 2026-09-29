export type HeldWord = {
  definition: string;
  origin: string;
};

const reader: HeldWord = {
  definition: "A person who reads.",
  origin: "Old English rǣdere, from rǣdan, to read or to advise.",
};

export const HELD_WORDS: Record<string, HeldWord> = {
  canon: {
    definition: "A rule, or a body of work accepted as holding.",
    origin: "Greek kanōn, a rod or a rule, through Latin canon.",
  },
  kanon: {
    definition: "The name of this instrument. This spelling of canon.",
    origin: "The same Greek root.",
  },
  cannon: {
    definition: "A large gun. Not the same word as canon.",
    origin: "Italian cannone, from Latin canna, a reed or a tube.",
  },
  preservation: {
    definition: "Keeping something, including what later fails.",
    origin: "Latin praeservare, to guard in advance.",
  },
  objective: {
    definition: "Settled by the rule from sources that can carry it.",
    origin: "Medieval Latin objectivus, from objectum.",
  },
  subjective: {
    definition: "Not yet provable. It waits for a person.",
    origin: "Latin subjectivus, from subicere, to place under.",
  },
  standing: {
    definition: "The weight a source currently has.",
    origin: "Old English standan, with -ing.",
  },
  source: {
    definition: "What a claim rests on.",
    origin: "Old French sourse, from Latin surgere, to rise.",
  },
  reader,
  readers: reader,
  library: {
    definition: "A kept collection.",
    origin: "Latin librarium, from liber, a book.",
  },
  claim: {
    definition: "A sentence entered to be judged.",
    origin: "Old French clamer, from Latin clamare, to cry out.",
  },
  desk: {
    definition: "Where a claim waits because the rule will not decide it.",
    origin: "Medieval Latin desca, from Latin discus.",
  },
  journey: {
    definition: "The kept history of a claim, including doubt and disproof.",
    origin: "Old French jornee, a day's travel.",
  },
  knowledge: {
    definition: "What is held, and the path by which it came to be held.",
    origin: "Middle English, from know and -ledge.",
  },
  skeptical: {
    definition: "Unwilling to treat a wish, or a single source, as proof.",
    origin: "Greek skeptikos, given to inquiry.",
  },
  memory: {
    definition: "What is kept of earlier talks.",
    origin: "Latin memoria, from memor, mindful.",
  },
  book: {
    definition:
      "A written work. On the shelf it is a list item, not a canonized claim.",
    origin: "Old English bōc.",
  },
  colophon: {
    definition: "A note, often at the end of a book, that can carry a date.",
    origin: "Greek kolophōn, a summit or a finishing stroke.",
  },
  bodleian: {
    definition: "The Bodleian Library at Oxford.",
    origin: "Named for Thomas Bodley, who refounded it.",
  },
};

export function normalizePhrase(phrase: string): string {
  return phrase
    .trim()
    .replace(/\s+/g, " ")
    .replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, "")
    .toLowerCase();
}

export function lookupHeld(phrase: string): HeldWord | null {
  const key = normalizePhrase(phrase);
  return HELD_WORDS[key] ?? null;
}
