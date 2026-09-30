"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { mapDictionaryPayload, presentReader, type WiderAnswer } from "@/lib/canon/reader";
import type { ReaderView } from "@/lib/canon/reader";
import { CanonProvider, useCanon } from "./CanonProvider";
import { ReaderSidebar } from "./ReaderSidebar";
import { VoiceProvider } from "./use-voice";

const ROOMS = [
  { href: "/canon", label: "Canon" },
  { href: "/canon/desk", label: "Desk" },
  { href: "/canon/sources", label: "Sources" },
  { href: "/canon/enter", label: "Enter" },
  { href: "/canon/ask", label: "Ask" },
  { href: "/canon/books", label: "Books" },
];

function elementOf(node: Node | null): Element | null {
  if (!node) {
    return null;
  }
  return node instanceof Element ? node : node.parentElement;
}

function CanonFrame({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const { ready, notice, storage, acceptStoredReplacement, loadOtherTab } = useCanon();
  const rootRef = useRef<HTMLDivElement>(null);
  const [phrase, setPhrase] = useState<string | null>(null);
  const [view, setView] = useState<ReaderView | null>(null);
  const [asking, setAsking] = useState(false);
  const request = useRef(0);

  useEffect(() => {
    const root = rootRef.current;
    if (!root) {
      return;
    }

    async function openPhrase(raw: string) {
      const cleaned = raw.trim().replace(/\s+/g, " ");
      if (!cleaned) {
        return;
      }
      const id = request.current + 1;
      request.current = id;
      const local = presentReader(cleaned, null);
      if (local.status === "held" || local.status === "too-long") {
        setPhrase(cleaned);
        setView(local);
        setAsking(false);
        return;
      }
      setPhrase(cleaned);
      setView(null);
      setAsking(true);
      let wider: WiderAnswer = { answered: false };
      try {
        const response = await fetch(
          `https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(cleaned)}`,
        );
        if (response.ok) {
          wider = mapDictionaryPayload(await response.json());
        }
      } catch {
        wider = { answered: false };
      }
      if (request.current !== id) {
        return;
      }
      setView(presentReader(cleaned, wider));
      setAsking(false);
    }

    function onSelect() {
      const selection = window.getSelection();
      if (!selection || selection.isCollapsed) {
        return;
      }
      const anchor = elementOf(selection.anchorNode);
      if (!anchor || !root || !root.contains(anchor)) {
        return;
      }
      if (anchor.closest("input, textarea, select, button, a, summary, label")) {
        return;
      }
      const text = selection.toString();
      if (text.trim().length === 0) {
        return;
      }
      void openPhrase(text);
    }

    document.addEventListener("mouseup", onSelect);
    document.addEventListener("keyup", onSelect);
    return () => {
      document.removeEventListener("mouseup", onSelect);
      document.removeEventListener("keyup", onSelect);
    };
  }, []);

  return (
    <div className="canon-app" ref={rootRef}>
      <header className="canon-header">
        <p className="eyebrow">Two tracks</p>
        <h1>Canon</h1>
        <p className="lede">
          Pronounced canon. Spelled Canon. The record kept under the earlier
          spelling stays in this browser. The words behind the letters stay
          open. canon.observer is owned. Stated 30 September 2026. No registrar
          and no price were given.
        </p>
      </header>
      <nav className="canon-rooms" aria-label="Rooms">
        {ROOMS.map((room) => {
          const current =
            room.href === "/canon"
              ? pathname === "/canon"
              : pathname === room.href || pathname.startsWith(`${room.href}/`);
          return (
            <Link
              key={room.href}
              href={room.href}
              aria-current={current ? "page" : undefined}
            >
              {room.label}
            </Link>
          );
        })}
      </nav>
      {notice ? (
        <div className="canon-notice" role="status">
          <p>{notice}</p>
          <div className="canon-actions">
            <button
              type="button"
              className="secondary-button"
              onClick={acceptStoredReplacement}
            >
              {storage === "conflict"
                ? "Keep this tab's record"
                : "Write what is on screen over the stored text"}
            </button>
            {storage === "conflict" ? (
              <button type="button" className="secondary-button" onClick={loadOtherTab}>
                Load the other tab&apos;s record
              </button>
            ) : null}
          </div>
        </div>
      ) : null}
      <div className="canon-layout">
        <div className="canon-room">
          {ready ? children : <p>Opening the record in this browser.</p>}
        </div>
        <ReaderSidebar
          phrase={phrase}
          view={view}
          asking={asking}
          onClose={() => {
            request.current += 1;
            setPhrase(null);
            setView(null);
            setAsking(false);
            window.speechSynthesis?.cancel();
          }}
        />
      </div>
    </div>
  );
}

export function CanonShell({ children }: { children: ReactNode }) {
  return (
    <CanonProvider>
      <VoiceProvider>
        <CanonFrame>{children}</CanonFrame>
      </VoiceProvider>
    </CanonProvider>
  );
}
