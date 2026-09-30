import { weigh } from "./rule";
import type { Entry, Source } from "./types";

const STOP_WORDS = new Set([
  "a",
  "an",
  "the",
  "of",
  "to",
  "and",
  "or",
  "is",
  "are",
  "was",
  "were",
  "be",
  "been",
  "being",
  "in",
  "on",
  "for",
  "with",
  "from",
  "that",
  "this",
  "it",
  "by",
  "as",
  "at",
  "do",
  "did",
  "does",
  "not",
  "no",
  "if",
  "so",
  "than",
  "then",
  "into",
  "over",
  "under",
  "about",
  "when",
  "what",
  "which",
  "who",
  "whom",
  "whose",
  "why",
  "how",
  "can",
  "may",
  "has",
  "have",
  "had",
  "but",
  "its",
  "his",
  "her",
  "their",
  "you",
  "your",
]);

export const GLUE_WORDS = [
  "about",
  "there",
  "their",
  "which",
  "would",
  "could",
  "these",
  "those",
  "under",
  "after",
  "before",
  "while",
  "where",
  "because",
  "through",
  "without",
  "within",
] as const;

export const NOT_IN_RECORD =
  "That is not in the record. I will not supply it from anywhere else.";

function stem(word: string): string {
  if (!/^[a-z]+$/.test(word)) {
    return word;
  }
  if (word.endsWith("ing") && word.length > 6) {
    return word.slice(0, -3);
  }
  if (word.endsWith("ed") && word.length > 5) {
    return word.slice(0, -2);
  }
  if (word.endsWith("s") && word.length > 4 && !word.endsWith("ss")) {
    return word.slice(0, -1);
  }
  return word;
}

function wordsOf(text: string): string[] {
  return text.toLowerCase().match(/[\p{L}\p{N}]+/gu) ?? [];
}

function tokens(text: string): string[] {
  return wordsOf(text).filter(
    (word) => word.length >= 4 && !STOP_WORDS.has(word),
  );
}

function sharesStem(left: string, right: string): boolean {
  return stem(left) === stem(right);
}

export function claimsForQuestion(question: string, entries: Entry[]): Entry[] {
  const asked = tokens(question);
  if (asked.length === 0) {
    return [];
  }
  return entries.filter((entry) => {
    const claim = tokens(entry.text);
    let hits = 0;
    for (const word of asked) {
      if (claim.some((part) => sharesStem(word, part))) {
        hits += 1;
      }
    }
    if (hits >= 2 && hits * 2 >= asked.length) {
      return true;
    }
    return (
      hits === 1 &&
      asked.some(
        (word) =>
          word.length >= 8 && claim.some((part) => sharesStem(word, part)),
      )
    );
  });
}

export function closedLine(entry: Entry, sources: Source[]): string {
  const text = entry.text.trim();
  const weighing = weigh(entry.cites, sources);
  if (entry.disposition === "objective") {
    return `${text} Held by the rule.`;
  }
  if (entry.disposition === "subjective") {
    return `${text} Not canon. Held by you, and still subjective.`;
  }
  if (entry.disposition === "fallen") {
    return `${text} Not canon. It fell, and it stays visible.`;
  }
  if (entry.disposition === "disproved") {
    return `${text} Disproved, and kept.`;
  }
  if (entry.disposition === "rejected") {
    return `${text} Rejected, and kept.`;
  }
  if (weighing.fight) {
    return `${text} Not canon. It is a fight.`;
  }
  return `${text} Not canon.`;
}

export function answerQuestion(
  question: string,
  entries: Entry[],
  sources: Source[],
): string[] {
  if (question.trim().length === 0) {
    return [];
  }
  const matched = claimsForQuestion(question, entries);
  if (matched.length === 0) {
    return [NOT_IN_RECORD];
  }
  return matched.map((entry) => closedLine(entry, sources));
}

export function contentWords(text: string): string[] {
  return wordsOf(text).filter((word) => word.length >= 5);
}

export function rephraseKeepsLines(
  candidate: string,
  lines: string[],
  question: string,
  context: string,
): boolean {
  const allowed = new Set<string>(GLUE_WORDS);
  for (const word of contentWords(`${lines.join(" ")} ${question} ${context}`)) {
    allowed.add(word);
  }
  return contentWords(candidate).every((word) => allowed.has(word));
}

export function guardRephrase(
  candidate: string,
  lines: string[],
  question: string,
  context: string,
): string[] {
  if (rephraseKeepsLines(candidate, lines, question, context)) {
    return [candidate];
  }
  return lines;
}
