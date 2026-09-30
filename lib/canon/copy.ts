import { dedupeCites, isSourceKind, isUsableStanding } from "./rule";
import { specimenEntries, specimenSources } from "./specimen";
import type { Cite, Disposition, Entry, JourneyEvent, Source } from "./types";
import { COPY_KIND, DISPOSITIONS, JOURNEY_KINDS } from "./types";
import type { JourneyKind, SourceKind } from "./types";

export type CanonCopy = {
  kind: typeof COPY_KIND;
  blanked: boolean;
  specimenIsLoad: boolean;
  sources: Source[];
  entries: Entry[];
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isStoredSourceKind(value: unknown): value is SourceKind {
  return typeof value === "string" && isSourceKind(value);
}

function isDisposition(value: unknown): value is Disposition {
  return (
    typeof value === "string" &&
    (DISPOSITIONS as readonly string[]).includes(value)
  );
}

function isJourneyKind(value: unknown): value is JourneyKind {
  return (
    typeof value === "string" &&
    (JOURNEY_KINDS as readonly string[]).includes(value)
  );
}

function canonical(value: unknown): string {
  return JSON.stringify(value);
}

export function specimenIsLoad(sources: Source[], entries: Entry[]): boolean {
  return (
    canonical(sources) === canonical(specimenSources()) &&
    canonical(entries) === canonical(specimenEntries())
  );
}

function parseSource(value: unknown): Source | null {
  if (!isRecord(value)) {
    return null;
  }
  if (typeof value.id !== "string" || typeof value.name !== "string") {
    return null;
  }
  if (value.name.trim().length === 0 || !isStoredSourceKind(value.kind)) {
    return null;
  }
  if (!isUsableStanding(value.standing) || !Array.isArray(value.history)) {
    return null;
  }
  const history = [];
  for (const item of value.history) {
    if (!isRecord(item)) {
      return null;
    }
    if (typeof item.at !== "string" || typeof item.note !== "string") {
      return null;
    }
    if (!isUsableStanding(item.standing)) {
      return null;
    }
    history.push({
      at: item.at,
      standing: item.standing,
      note: item.note,
    });
  }
  return {
    id: value.id,
    name: value.name,
    kind: value.kind,
    standing: value.standing,
    history,
  };
}

function parseCite(value: unknown): Cite | null {
  if (!isRecord(value)) {
    return null;
  }
  if (typeof value.sourceId !== "string") {
    return null;
  }
  if (value.role !== "support" && value.role !== "contest") {
    return null;
  }
  return { sourceId: value.sourceId, role: value.role };
}

function parseJourney(value: unknown): JourneyEvent | null {
  if (!isRecord(value)) {
    return null;
  }
  if (typeof value.id !== "string" || typeof value.at !== "string") {
    return null;
  }
  if (typeof value.note !== "string" || !isJourneyKind(value.kind)) {
    return null;
  }
  return {
    id: value.id,
    at: value.at,
    kind: value.kind,
    note: value.note,
  };
}

function parseEntry(value: unknown): Entry | null {
  if (!isRecord(value)) {
    return null;
  }
  if (typeof value.id !== "string" || typeof value.text !== "string") {
    return null;
  }
  if (!isDisposition(value.disposition) || typeof value.humanHold !== "boolean") {
    return null;
  }
  if (!Array.isArray(value.cites) || !Array.isArray(value.journey)) {
    return null;
  }
  const cites: Cite[] = [];
  for (const cite of value.cites) {
    const parsed = parseCite(cite);
    if (!parsed) {
      return null;
    }
    cites.push(parsed);
  }
  const uniqueCites = dedupeCites(cites);
  const journey: JourneyEvent[] = [];
  for (const event of value.journey) {
    const parsed = parseJourney(event);
    if (!parsed) {
      return null;
    }
    journey.push(parsed);
  }
  return {
    id: value.id,
    text: value.text,
    cites: uniqueCites,
    disposition: value.disposition,
    humanHold: value.humanHold,
    journey,
  };
}

export function exportCopy(
  sources: Source[],
  entries: Entry[],
  blanked: boolean,
): CanonCopy {
  return {
    kind: COPY_KIND,
    blanked,
    specimenIsLoad: specimenIsLoad(sources, entries),
    sources,
    entries,
  };
}

export function parseCopy(
  value: unknown,
): { ok: true; copy: CanonCopy } | { ok: false; reason: string } {
  if (!isRecord(value) || value.kind !== COPY_KIND) {
    return { ok: false, reason: "That file is not a canon copy." };
  }
  if (!Array.isArray(value.sources) || !Array.isArray(value.entries)) {
    return {
      ok: false,
      reason: "That file does not hold sources and entries.",
    };
  }
  if (typeof value.blanked !== "boolean") {
    return {
      ok: false,
      reason: "That file does not say whether this browser was blanked.",
    };
  }
  const sources: Source[] = [];
  for (const source of value.sources) {
    const parsed = parseSource(source);
    if (!parsed) {
      return { ok: false, reason: "A source in that file could not be read." };
    }
    sources.push(parsed);
  }
  const entries: Entry[] = [];
  for (const entry of value.entries) {
    const parsed = parseEntry(entry);
    if (!parsed) {
      return { ok: false, reason: "An entry in that file could not be read." };
    }
    entries.push(parsed);
  }
  const sourceIds = new Set(sources.map((source) => source.id));
  const entryIds = new Set(entries.map((entry) => entry.id));
  if (sourceIds.size !== sources.length || entryIds.size !== entries.length) {
    return { ok: false, reason: "That file repeats an id." };
  }
  return {
    ok: true,
    copy: {
      kind: COPY_KIND,
      blanked: value.blanked,
      specimenIsLoad:
        typeof value.specimenIsLoad === "boolean"
          ? value.specimenIsLoad
          : specimenIsLoad(sources, entries),
      sources,
      entries,
    },
  };
}
