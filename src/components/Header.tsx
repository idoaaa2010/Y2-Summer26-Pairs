import { motion, AnimatePresence } from "framer-motion";
import { Volume2, VolumeX, ChevronDown, Check } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import type { ChatMode } from "../types";
import { TRACKS } from "../data/tracks";
import { playGearShift, playTick } from "../lib/audio";

interface HeaderProps {
  mode: ChatMode;
  onModeChange: (mode: ChatMode) => void;
  trackId: string;
  onTrackChange: (id: string) => void;
  muted: boolean;
  onMuteToggle: () => void;
}

export default function Header({
  mode,
  onModeChange,
  trackId,
  onTrackChange,
  muted,
  onMuteToggle,
}: HeaderProps) {
  const [trackOpen, setTrackOpen] = useState(false);
  const trackRef = useRef<HTMLDivElement>(null);
  const isEngineer = mode === "engineer";

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (trackRef.current && !trackRef.current.contains(e.target as Node)) {
        setTrackOpen(false);
      }
    }
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  const handleMode = () => {
    playGearShift();
    onModeChange(isEngineer ? "paddock" : "engineer");
  };

  const activeTrack = TRACKS.find((t) => t.id === trackId) ?? TRACKS[0];

  return (
    <header className="sticky top-0 z-30 border-b border-carbon-500/60 bg-carbon-900/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-[1600px] items-center justify-between gap-4 px-4 py-3 sm:px-6">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="relative h-9 w-9">
            <svg viewBox="0 0 64 64" className="h-full w-full">
              <path
                d="M8 44c10-20 38-20 48 0"
                stroke="#FF8700"
                strokeWidth="4"
                fill="none"
                strokeLinecap="round"
              />
              <circle cx="32" cy="32" r="6" fill="#FF8700" />
            </svg>
          </div>
          <div className="leading-tight">
            <div className="text-sm font-bold tracking-wide text-white">
              McLAREN <span className="text-papaya">PIT WALL</span>
            </div>
            <div className="font-lcd text-[10px] uppercase tracking-[0.3em] text-ash">
              AI Race Engineer
            </div>
          </div>
        </div>

        {/* Center: Mode toggle */}
        <div className="flex items-center gap-3">
          <span
            className={`hidden text-xs font-semibold uppercase tracking-wider transition-colors sm:inline ${
              !isEngineer ? "text-white" : "text-ash"
            }`}
          >
            Paddock
          </span>
          <button
            onClick={handleMode}
            aria-label="Toggle driver mode"
            className="group relative h-9 w-20 rounded-full border border-carbon-400 bg-carbon-700 transition-colors"
          >
            <motion.div
              className="absolute top-1 h-7 w-7 rounded-full shadow-lg"
              animate={{ left: isEngineer ? "3.25rem" : "0.25rem" }}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
              style={{
                background: isEngineer ? "#FF8700" : "#3a3a3a",
                boxShadow: isEngineer
                  ? "0 0 16px rgba(255,135,0,0.6)"
                  : "0 2px 8px rgba(0,0,0,0.4)",
              }}
            />
          </button>
          <span
            className={`hidden text-xs font-semibold uppercase tracking-wider transition-colors sm:inline ${
              isEngineer ? "text-papaya glow-papaya" : "text-ash"
            }`}
          >
            Race Engineer
          </span>
        </div>

        {/* Right: Track selector + mute */}
        <div className="flex items-center gap-2">
          <div ref={trackRef} className="relative">
            <button
              onClick={() => {
                playTick();
                setTrackOpen((o) => !o);
              }}
              className="flex items-center gap-2 rounded-lg border border-carbon-400 bg-carbon-700 px-3 py-2 text-xs font-semibold text-white transition-colors hover:border-papaya/60"
            >
              <span className="h-2 w-2 rounded-full bg-papaya" />
              <span className="hidden sm:inline">{activeTrack.name}</span>
              <ChevronDown className="h-3.5 w-3.5 text-ash" />
            </button>
            <AnimatePresence>
              {trackOpen && (
                <motion.div
                  initial={{ opacity: 0, y: -8, scale: 0.96 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -8, scale: 0.96 }}
                  transition={{ duration: 0.15 }}
                  className="absolute right-0 top-11 z-40 w-52 overflow-hidden rounded-xl border border-carbon-400 bg-carbon-800 shadow-2xl"
                >
                  <div className="px-3 py-2 font-lcd text-[10px] uppercase tracking-[0.25em] text-ash">
                    Select Circuit
                  </div>
                  {TRACKS.map((t) => (
                    <button
                      key={t.id}
                      onClick={() => {
                        playTick();
                        onTrackChange(t.id);
                        setTrackOpen(false);
                      }}
                      className={`flex w-full items-center justify-between px-3 py-2.5 text-left text-sm transition-colors ${
                        t.id === trackId
                          ? "bg-papaya/10 text-papaya"
                          : "text-white hover:bg-carbon-600"
                      }`}
                    >
                      <div>
                        <div className="font-semibold">{t.name}</div>
                        <div className="text-[10px] text-ash">
                          {t.laps} laps · {t.keyCorner}
                        </div>
                      </div>
                      {t.id === trackId && <Check className="h-4 w-4" />}
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <button
            onClick={onMuteToggle}
            aria-label={muted ? "Unmute" : "Mute"}
            className="rounded-lg border border-carbon-400 bg-carbon-700 p-2 text-white transition-colors hover:border-papaya/60"
          >
            {muted ? (
              <VolumeX className="h-4 w-4 text-ash" />
            ) : (
              <Volume2 className="h-4 w-4 text-papaya" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
