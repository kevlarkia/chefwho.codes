"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useSyncExternalStore,
  type ReactNode,
} from "react";
import { CALM_PITCH, CALM_RATE, VOICE_STORAGE_KEY } from "@/lib/canon/types";

type VoiceChoice = {
  voiceURI: string | null;
};

const voiceListeners = new Set<() => void>();
let storedVoice: string | null | undefined;

function readStoredVoice(): string | null {
  const raw = window.localStorage.getItem(VOICE_STORAGE_KEY);
  if (!raw) {
    return null;
  }
  try {
    const parsed = JSON.parse(raw) as VoiceChoice;
    if (parsed && (parsed.voiceURI === null || typeof parsed.voiceURI === "string")) {
      return parsed.voiceURI;
    }
  } catch {
    return null;
  }
  return null;
}

function subscribeVoice(listener: () => void): () => void {
  voiceListeners.add(listener);
  return () => {
    voiceListeners.delete(listener);
  };
}

function getVoiceSnapshot(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  if (storedVoice === undefined) {
    storedVoice = readStoredVoice();
  }
  return storedVoice;
}

function getVoiceServerSnapshot(): string | null {
  return null;
}

function writeVoice(next: string | null) {
  storedVoice = next;
  window.localStorage.setItem(
    VOICE_STORAGE_KEY,
    JSON.stringify({ voiceURI: next } satisfies VoiceChoice),
  );
  for (const listener of voiceListeners) {
    listener();
  }
}

function useVoice() {
  const voiceURI = useSyncExternalStore(
    subscribeVoice,
    getVoiceSnapshot,
    getVoiceServerSnapshot,
  );
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);

  useEffect(() => {
    const synthesis = window.speechSynthesis;
    if (!synthesis) {
      return;
    }
    const loadVoices = () => {
      setVoices(
        synthesis
          .getVoices()
          .filter((voice) => voice.lang.toLowerCase().startsWith("en")),
      );
    };
    const timer = window.setTimeout(loadVoices, 0);
    synthesis.addEventListener("voiceschanged", loadVoices);
    return () => {
      window.clearTimeout(timer);
      synthesis.removeEventListener("voiceschanged", loadVoices);
      synthesis.cancel();
    };
  }, []);

  function speak(text: string) {
    const synthesis = window.speechSynthesis;
    if (!synthesis || text.trim().length === 0) {
      return;
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = CALM_RATE;
    utterance.pitch = CALM_PITCH;
    const match = synthesis.getVoices().find((voice) => voice.voiceURI === voiceURI);
    if (match) {
      utterance.voice = match;
    }
    synthesis.cancel();
    synthesis.speak(utterance);
  }

  return {
    voiceURI,
    setVoiceURI: writeVoice,
    voices,
    speak,
  };
}

type VoiceValue = ReturnType<typeof useVoice>;

const VoiceContext = createContext<VoiceValue | null>(null);

export function VoiceProvider({ children }: { children: ReactNode }) {
  const value = useVoice();
  return <VoiceContext.Provider value={value}>{children}</VoiceContext.Provider>;
}

export function useCanonVoice(): VoiceValue {
  const value = useContext(VoiceContext);
  if (!value) {
    throw new Error("Voice is only available inside Canon.");
  }
  return value;
}
