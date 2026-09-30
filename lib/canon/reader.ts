import { lookupHeld } from "./held-words";
import { SHORT_PHRASE_WORD_LIMIT } from "./types";

export type WiderAnswer =
  | { answered: false }
  | {
      answered: true;
      definitions: string[];
      origin?: string;
      audioUrl?: string;
    };

export type ReaderView = {
  phrase: string;
  status: "held" | "wider" | "unreachable" | "too-long";
  marker: string;
  definitions: string[];
  origin: string | null;
  originMissing: boolean;
  audioUrl: string | null;
};

export function isShortPhrase(phrase: string): boolean {
  const words = phrase.trim().split(/\s+/).filter(Boolean);
  return words.length > 0 && words.length <= SHORT_PHRASE_WORD_LIMIT;
}

export function presentReader(
  phrase: string,
  wider: WiderAnswer | null,
): ReaderView {
  const cleaned = phrase.trim().replace(/\s+/g, " ");
  if (!isShortPhrase(cleaned)) {
    return {
      phrase: cleaned,
      status: "too-long",
      marker: "Mark a word or a short phrase.",
      definitions: [],
      origin: null,
      originMissing: false,
      audioUrl: null,
    };
  }
  const held = lookupHeld(cleaned);
  if (held) {
    return {
      phrase: cleaned,
      status: "held",
      marker: "Held here.",
      definitions: [held.definition],
      origin: held.origin,
      originMissing: held.origin.length === 0,
      audioUrl: null,
    };
  }
  if (!wider || !wider.answered || wider.definitions.length === 0) {
    return {
      phrase: cleaned,
      status: "unreachable",
      marker: "The wider base did not answer. It is unreachable.",
      definitions: [],
      origin: null,
      originMissing: false,
      audioUrl: null,
    };
  }
  const origin = wider.origin?.trim() ? wider.origin.trim() : null;
  const audioUrl =
    wider.audioUrl && wider.audioUrl.startsWith("https://")
      ? wider.audioUrl
      : null;
  return {
    phrase: cleaned,
    status: "wider",
    marker: "From the wider base.",
    definitions: wider.definitions,
    origin,
    originMissing: origin === null,
    audioUrl,
  };
}

type DictionaryEntry = {
  meanings?: {
    definitions?: { definition?: string }[];
  }[];
  sourceUrls?: string[];
  etymology?: string;
  origin?: string;
  phonetics?: { audio?: string }[];
};

export function mapDictionaryPayload(payload: unknown): WiderAnswer {
  if (!Array.isArray(payload) || payload.length === 0) {
    return { answered: false };
  }
  const definitions: string[] = [];
  const origins: string[] = [];
  let audioUrl: string | undefined;
  for (const item of payload) {
    if (!item || typeof item !== "object") {
      continue;
    }
    const entry = item as DictionaryEntry;
    for (const meaning of entry.meanings ?? []) {
      for (const definition of meaning.definitions ?? []) {
        if (definition.definition && definition.definition.trim()) {
          definitions.push(definition.definition.trim());
        }
      }
    }
    if (entry.etymology?.trim()) {
      origins.push(entry.etymology.trim());
    }
    if (entry.origin?.trim()) {
      origins.push(entry.origin.trim());
    }
    for (const url of entry.sourceUrls ?? []) {
      if (url.trim()) {
        origins.push(url.trim());
      }
    }
    if (!audioUrl) {
      for (const phonetic of entry.phonetics ?? []) {
        if (phonetic.audio && phonetic.audio.startsWith("https://")) {
          audioUrl = phonetic.audio;
          break;
        }
      }
    }
  }
  if (definitions.length === 0) {
    return { answered: false };
  }
  return {
    answered: true,
    definitions,
    origin: origins.length > 0 ? origins.join(" ") : undefined,
    audioUrl,
  };
}
