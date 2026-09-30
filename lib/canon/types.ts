export const SOURCE_KINDS = [
  "primary",
  "record",
  "witness",
  "press",
  "self",
  "hearsay",
] as const;

export type SourceKind = (typeof SOURCE_KINDS)[number];

export type StandingChange = {
  at: string;
  standing: number;
  note: string;
};

export type Source = {
  id: string;
  name: string;
  kind: SourceKind;
  standing: number;
  history: StandingChange[];
};

export type CiteRole = "support" | "contest";

export type Cite = {
  sourceId: string;
  role: CiteRole;
};

export const DISPOSITIONS = [
  "objective",
  "desk",
  "subjective",
  "fallen",
  "disproved",
  "rejected",
] as const;

export type Disposition = (typeof DISPOSITIONS)[number];

export const JOURNEY_KINDS = [
  "entered",
  "revised",
  "doubt",
  "held",
  "fell",
  "verified",
  "rejected",
  "disproved",
  "note",
] as const;

export type JourneyKind = (typeof JOURNEY_KINDS)[number];

export type JourneyEvent = {
  id: string;
  at: string;
  kind: JourneyKind;
  note: string;
};

export type Entry = {
  id: string;
  text: string;
  cites: Cite[];
  disposition: Disposition;
  humanHold: boolean;
  journey: JourneyEvent[];
};

export type Weighing = {
  support: number;
  contest: number;
  net: number;
  carriers: number;
  bar: number;
  fight: boolean;
  objective: boolean;
};

export type BookPlace = "read" | "to-get";

export type Book = {
  id: string;
  title: string;
  author: string;
  note?: string;
  place: BookPlace;
};

export type Talk = {
  id: string;
  at: string;
  question: string;
  lines: string[];
  synopsis: string;
};

export type RecordState = {
  blanked: boolean;
  sources: Source[];
  entries: Entry[];
  talks: Talk[];
  keepTalks: boolean;
  shelf: Book[];
};

export const RECORD_STORAGE_KEY = "kanon-v1";
export const VOICE_STORAGE_KEY = "kanon-voice";
export const COPY_KIND = "kanon-copy";

export const FLOOR = 58;
export const CAP = 80;
export const YOUNG_BAR = 64;
export const SEASONED_AT = 50;
export const WITNESS_CARRY_AT = 70;

export const CALM_RATE = 0.85;
export const CALM_PITCH = 1;

export const SHORT_PHRASE_WORD_LIMIT = 4;
