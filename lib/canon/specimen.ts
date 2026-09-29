import type { Entry, JourneyEvent, Source } from "./types";

const DAY = "2026-09-27T12:00:00.000Z";

function at(minutes: number): string {
  return new Date(Date.parse(DAY) + minutes * 60_000).toISOString();
}

function event(
  id: string,
  minutes: number,
  kind: JourneyEvent["kind"],
  note: string,
): JourneyEvent {
  return { id, at: at(minutes), kind, note };
}

export function specimenSources(): Source[] {
  return [
    {
      id: "src-bodleian-catalogue",
      name: "Bodleian Catalogue",
      kind: "record",
      standing: 86,
      history: [
        {
          at: at(0),
          standing: 86,
          note: "Standing as loaded with the specimen.",
        },
      ],
    },
    {
      id: "src-oxford-history-note",
      name: "Oxford History Note",
      kind: "press",
      standing: 58,
      history: [
        {
          at: at(0),
          standing: 58,
          note: "Standing as loaded with the specimen.",
        },
      ],
    },
    {
      id: "src-forum-thread",
      name: "Forum Thread",
      kind: "hearsay",
      standing: 28,
      history: [
        {
          at: at(0),
          standing: 28,
          note: "Standing as loaded with the specimen.",
        },
      ],
    },
    {
      id: "src-etymology-desk",
      name: "Etymology Desk",
      kind: "record",
      standing: 76,
      history: [
        {
          at: at(0),
          standing: 76,
          note: "Standing as loaded with the specimen.",
        },
      ],
    },
    {
      id: "src-personal-margin",
      name: "Personal Margin",
      kind: "self",
      standing: 44,
      history: [
        {
          at: at(0),
          standing: 44,
          note: "Standing as loaded with the specimen.",
        },
      ],
    },
    {
      id: "src-reading-journal",
      name: "Reading Journal",
      kind: "witness",
      standing: 63,
      history: [
        {
          at: at(0),
          standing: 63,
          note: "Standing as loaded with the specimen. Under 70, so not a carrier.",
        },
      ],
    },
    {
      id: "src-colophon-index",
      name: "Colophon Index",
      kind: "primary",
      standing: 57,
      history: [
        {
          at: at(1),
          standing: 81,
          note: "Standing when the colophon claims were entered.",
        },
        {
          at: at(4),
          standing: 57,
          note: "Lowered from 81 to 57 because the overclaim was certainty beyond the document.",
        },
      ],
    },
    {
      id: "src-naming-scratch",
      name: "Naming Scratch",
      kind: "self",
      standing: 34,
      history: [
        {
          at: at(0),
          standing: 34,
          note: "Standing as loaded with the specimen.",
        },
      ],
    },
  ];
}

export function specimenEntries(): Entry[] {
  const bodleian: Entry = {
    id: "ent-bodleian",
    text: "The Bodleian Library opened to readers on 8 November 1602.",
    cites: [
      { sourceId: "src-bodleian-catalogue", role: "support" },
      { sourceId: "src-oxford-history-note", role: "support" },
    ],
    disposition: "objective",
    humanHold: false,
    journey: [
      event(
        "j-bodleian-entered",
        1,
        "entered",
        "The Bodleian Library opened to readers in 1602.",
      ),
      event(
        "j-bodleian-doubt",
        2,
        "doubt",
        "Some notices put a reading room in 1598 and the public opening in 1602.",
      ),
      event(
        "j-bodleian-revised",
        3,
        "revised",
        "Wording revised to: The Bodleian Library opened to readers on 8 November 1602.",
      ),
      event("j-bodleian-held", 3, "held", "Held by the rule."),
    ],
  };
  const roots: Entry = {
    id: "ent-canon-cannon",
    text: "Canon and cannon share a root.",
    cites: [
      { sourceId: "src-forum-thread", role: "support" },
      { sourceId: "src-etymology-desk", role: "contest" },
    ],
    disposition: "desk",
    humanHold: false,
    journey: [
      event("j-roots-entered", 1, "entered", "Entered on the desk."),
      event(
        "j-roots-note",
        2,
        "note",
        "They do not. One is a rule, the other a tube.",
      ),
    ],
  };
  const scroll: Entry = {
    id: "ent-long-scroll",
    text: "A long-scroll brief is more trustworthy than a slide deck.",
    cites: [
      { sourceId: "src-personal-margin", role: "support" },
      { sourceId: "src-reading-journal", role: "support" },
    ],
    disposition: "subjective",
    humanHold: true,
    journey: [
      event("j-scroll-entered", 1, "entered", "Entered."),
      event(
        "j-scroll-verified",
        2,
        "verified",
        "Verified by the person. It stays subjective. Verification is not proof.",
      ),
    ],
  };
  const narrow: Entry = {
    id: "ent-colophon-narrow",
    text: "A printed colophon can carry a publication date.",
    cites: [{ sourceId: "src-colophon-index", role: "support" }],
    disposition: "fallen",
    humanHold: false,
    journey: [
      event(
        "j-narrow-entered",
        1,
        "entered",
        "Entered on a primary index.",
      ),
      event(
        "j-narrow-held",
        2,
        "held",
        "Held by the rule while Colophon Index stood at 81.",
      ),
      event(
        "j-narrow-fell",
        4,
        "fell",
        "It fell when Colophon Index was lowered to 57. It was not revived by that fall.",
      ),
    ],
  };
  const always: Entry = {
    id: "ent-colophon-always",
    text: "A colophon date is always the true first publication.",
    cites: [{ sourceId: "src-colophon-index", role: "support" }],
    disposition: "disproved",
    humanHold: false,
    journey: [
      event("j-always-entered", 2, "entered", "Entered."),
      event(
        "j-always-disproved",
        4,
        "disproved",
        "Disproved and kept. A colophon can be added after the edition, or reprinted with a later date.",
      ),
    ],
  };
  const spelling: Entry = {
    id: "ent-q-spelling",
    text: "A Q-spelling is a safe name for this system.",
    cites: [{ sourceId: "src-naming-scratch", role: "support" }],
    disposition: "rejected",
    humanHold: false,
    journey: [
      event("j-q-entered", 1, "entered", "Entered."),
      event(
        "j-q-rejected",
        2,
        "rejected",
        "Rejected and kept. Naming Scratch.",
      ),
    ],
  };
  return [bodleian, roots, scroll, narrow, always, spelling];
}
