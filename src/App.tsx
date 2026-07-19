import { useState, useEffect, useRef, useCallback } from "react";
import { AnimatePresence, motion } from "framer-motion";
import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import TelemetrySidebar from "./components/TelemetrySidebar";
import { streamChat } from "./lib/api";
import { playRadioBleep, playGearShift, setMuted } from "./lib/audio";
import { getTrack } from "./data/tracks";
import type { ChatMessage, ChatMode, Telemetry } from "./types";

const uid = () => Math.random().toString(36).slice(2, 11);

const INITIAL_TELEMETRY: Telemetry = {
  engineTemp: 104,
  responseSpeed: 0,
  ersDeployment: 0,
  drsAvailable: true,
  lap: 1,
};

export default function App() {
  const [mode, setMode] = useState<ChatMode>("paddock");
  const [trackId, setTrackId] = useState("monaco");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [streamingId, setStreamingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [muted, setMutedState] = useState(false);
  const [telemetry, setTelemetry] = useState<Telemetry>(INITIAL_TELEMETRY);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const abortRef = useRef<AbortController | null>(null);
  const track = getTrack(trackId);

  // Telemetry simulation — randomize while thinking to look alive
  useEffect(() => {
    const interval = setInterval(() => {
      setTelemetry((t) => ({
        ...t,
        engineTemp: clamp(
          t.engineTemp + (Math.random() - 0.5) * (isThinking ? 6 : 1.5),
          98,
          125
        ),
        responseSpeed: isThinking
          ? Math.round(180 + Math.random() * 120)
          : Math.round(40 + Math.random() * 30),
      }));
    }, 800);
    return () => clearInterval(interval);
  }, [isThinking]);

  const handleSend = useCallback(async () => {
    const text = input.trim();
    if (!text || isThinking) return;

    setError(null);
    const userMsg: ChatMessage = {
      id: uid(),
      role: "user",
      content: text,
      mode,
      trackId,
    };
    const assistantId = uid();
    const assistantMsg: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      mode,
      trackId,
    };

    setMessages((m) => [...m, userMsg, assistantMsg]);
    setInput("");
    setIsThinking(true);
    setStreamingId(assistantId);
    playRadioBleep();

    // Reset ERS for this session
    setTelemetry((t) => ({ ...t, ersDeployment: 0 }));

    const controller = new AbortController();
    abortRef.current = controller;

    const history = [...messages, userMsg]
      .filter((m) => !m.error)
      .map((m) => ({ role: m.role, content: m.content }));

    await streamChat(
      {
        mode,
        trackId,
        message: text,
        history,
        signal: controller.signal,
      },
      {
        onToken: (tok) => {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId ? { ...m, content: m.content + tok } : m
            )
          );
          setTelemetry((t) => ({
            ...t,
            ersDeployment: t.ersDeployment + Math.round(tok.length / 4),
          }));
        },
        onDone: (full) => {
          setIsThinking(false);
          setStreamingId(null);
          playRadioBleep();
          setTelemetry((t) => ({
            ...t,
            responseSpeed: full.latency_ms,
            ersDeployment: full.tokens_used,
            lap: Math.min(t.lap + 1, track.laps),
          }));
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? {
                    ...m,
                    content: full.reply,
                    tokensUsed: full.tokens_used,
                    latencyMs: full.latency_ms,
                  }
                : m
            )
          );
        },
        onError: (err) => {
          setIsThinking(false);
          setStreamingId(null);
          setError(
            "Telemetry lost. Please check connection and try again."
          );
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? {
                    ...m,
                    content:
                      "PIT LANE ERROR: Telemetry lost. Please check connection and try again.",
                    error: true,
                  }
                : m
            )
          );
          console.error(err);
        },
      }
    );
  }, [input, isThinking, mode, trackId, messages, track.laps]);

  const handleModeChange = (m: ChatMode) => {
    playGearShift();
    setMode(m);
  };

  const handleMuteToggle = () => {
    setMutedState((v) => {
      const next = !v;
      setMuted(next);
      return next;
    });
  };

  const handleTrackChange = (id: string) => {
    setTrackId(id);
    setTelemetry((t) => ({ ...t, lap: 1, ersDeployment: 0 }));
  };

  const dismissError = () => setError(null);

  return (
    <div className="app-bg flex h-screen flex-col text-white">
      <Header
        mode={mode}
        onModeChange={handleModeChange}
        trackId={trackId}
        onTrackChange={handleTrackChange}
        muted={muted}
        onMuteToggle={handleMuteToggle}
      />

      <div className="flex flex-1 overflow-hidden">
        {/* Main chat area (70%) */}
        <main className="flex flex-1 flex-col">
          <ChatWindow
            messages={messages}
            isThinking={isThinking && !streamingId}
            streamingId={streamingId}
            error={error}
            onDismissError={dismissError}
          />
          <ChatInput
            value={input}
            onChange={setInput}
            onSend={handleSend}
            mode={mode}
            disabled={isThinking}
          />
        </main>

        {/* Telemetry sidebar (30%) — desktop */}
        <div className="hidden w-[340px] shrink-0 lg:block">
          <TelemetrySidebar
            telemetry={telemetry}
            track={track}
            mode={mode}
            isThinking={isThinking}
          />
        </div>
      </div>

      {/* Mobile telemetry toggle */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/60 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className="absolute right-0 top-0 h-full w-[300px]"
              onClick={(e) => e.stopPropagation()}
            >
              <TelemetrySidebar
                telemetry={telemetry}
                track={track}
                mode={mode}
                isThinking={isThinking}
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Mobile FAB to open telemetry */}
      {!sidebarOpen && (
        <motion.button
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          onClick={() => setSidebarOpen(true)}
          className="fixed bottom-24 right-4 z-30 flex h-12 w-12 items-center justify-center rounded-full bg-papaya text-carbon-900 shadow-lg lg:hidden"
          aria-label="Open telemetry"
        >
          <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 12h4l3-8 4 16 3-8h4" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </motion.button>
      )}
    </div>
  );
}

function clamp(n: number, min: number, max: number) {
  return Math.round(Math.max(min, Math.min(max, n)));
}
