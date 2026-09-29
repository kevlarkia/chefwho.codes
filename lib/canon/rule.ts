import type { Cite, Source, SourceKind, Weighing } from "./types";
import {
  CAP,
  FLOOR,
  SEASONED_AT,
  WITNESS_CARRY_AT,
  YOUNG_BAR,
} from "./types";

/**
 * A contest is a fight when it is close and strong enough. No separate
 * cutoff for those words was stored. This instrument measures them with
 * the floor and the bar already set:
 * strong means the contesting weight is at least the floor (58);
 * close means the gap between support and contest is at most the bar.
 * A fight is not objective.
 */
export function isFight(
  support: number,
  contest: number,
  bar: number,
): boolean {
  const strong = contest >= FLOOR;
  const close = contest > 0 && Math.abs(support - contest) <= bar;
  return strong && close;
}

export function canCarry(source: Pick<Source, "kind" | "standing">): boolean {
  if (source.kind === "primary" || source.kind === "record") {
    return true;
  }
  if (source.kind === "witness") {
    return source.standing >= WITNESS_CARRY_AT;
  }
  return false;
}

export function barFor(sources: Pick<Source, "standing">[]): number {
  const seasoned = sources
    .map((source) => source.standing)
    .filter((standing) => standing >= SEASONED_AT)
    .sort((left, right) => left - right);
  if (seasoned.length < 3) {
    return YOUNG_BAR;
  }
  const middle =
    seasoned.length % 2 === 1
      ? seasoned[(seasoned.length - 1) / 2]
      : (seasoned[seasoned.length / 2 - 1] + seasoned[seasoned.length / 2]) /
        2;
  return Math.min(CAP, Math.max(FLOOR, middle));
}

export function weigh(
  cites: Cite[],
  sources: Source[],
): Weighing {
  const bar = barFor(sources);
  let support = 0;
  let contest = 0;
  let carriers = 0;
  for (const cite of cites) {
    const source = sources.find((item) => item.id === cite.sourceId);
    if (!source) {
      continue;
    }
    if (cite.role === "support") {
      if (canCarry(source)) {
        support += source.standing;
        carriers += 1;
      } else {
        support += source.standing / 4;
      }
    } else {
      contest += source.standing;
    }
  }
  const net = support - contest;
  const fight = isFight(support, contest, bar);
  const objective = carriers >= 1 && !fight && net >= bar;
  return { support, contest, net, carriers, bar, fight, objective };
}

export function formatWeight(value: number): string {
  if (Number.isInteger(value)) {
    return String(value);
  }
  const quarters = Math.round(value * 4) / 4;
  return String(quarters);
}

export function isSourceKind(value: string): value is SourceKind {
  return (
    value === "primary" ||
    value === "record" ||
    value === "witness" ||
    value === "press" ||
    value === "self" ||
    value === "hearsay"
  );
}
