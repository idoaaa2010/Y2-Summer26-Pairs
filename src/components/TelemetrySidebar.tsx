import { motion, AnimatePresence } from "framer-motion";
import { Gauge, Activity, Zap, Flag, Radio, MapPin } from "lucide-react";
import type { Telemetry, Track, ChatMode } from "../types";

interface TelemetrySidebarProps {
  telemetry: Telemetry;
  track: Track;
  mode: ChatMode;
  isThinking: boolean;
}

function Metric({
  icon,
  label,
  value,
  unit,
  color = "papaya",
  pulse = false,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  unit: string;
  color?: "papaya" | "white" | "ash";
  pulse?: boolean;
}) {
  const colorClass =
    color === "papaya"
      ? "text-papaya glow-papaya"
      : color === "white"
      ? "text-white"
      : "text-ash";
  return (
    <div className="relative overflow-hidden rounded-lg border border-carbon-500 bg-carbon-900/80 p-3 scanlines">
      <div className="flex items-center gap-1.5 font-lcd text-[9px] uppercase tracking-[0.2em] text-ash">
        {icon}
        <span>{label}</span>
      </div>
      <div className="mt-1.5 flex items-baseline gap-1">
        <AnimatePresence mode="popLayout">
          <motion.span
            key={String(value)}
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 6 }}
            transition={{ duration: 0.15 }}
            className={`font-lcd text-2xl font-bold tabular-nums ${colorClass} ${
              pulse ? "animate-flicker" : ""
            }`}
          >
            {value}
          </motion.span>
        </AnimatePresence>
        <span className="font-lcd text-xs text-ash">{unit}</span>
      </div>
    </div>
  );
}

export default function TelemetrySidebar({
  telemetry,
  track,
  mode,
  isThinking,
}: TelemetrySidebarProps) {
  const isEngineer = mode === "engineer";

  return (
    <aside className="flex h-full flex-col gap-3 overflow-y-auto border-l border-carbon-500/60 bg-carbon-900/60 p-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity className="h-4 w-4 text-papaya" />
          <span className="font-lcd text-xs uppercase tracking-[0.25em] text-white">
            Live Telemetry
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <motion.span
            className="h-2 w-2 rounded-full bg-papaya"
            animate={{ opacity: [1, 0.3, 1] }}
            transition={{ duration: 1.2, repeat: Infinity }}
          />
          <span className="font-lcd text-[9px] uppercase tracking-wider text-ash">
            {isThinking ? "Live" : "Idle"}
          </span>
        </div>
      </div>

      {/* Mode badge */}
      <div
        className={`rounded-lg border px-3 py-2 text-center font-lcd text-[10px] uppercase tracking-[0.2em] ${
          isEngineer
            ? "border-papaya/50 bg-papaya/10 text-papaya"
            : "border-carbon-400 bg-carbon-700 text-ash"
        }`}
      >
        {isEngineer ? "Race Engineer Mode" : "Paddock Mode"}
      </div>

      {/* Mini-map */}
      <div className="relative overflow-hidden rounded-xl border border-carbon-500 bg-carbon-900 p-3 scanlines">
        <div className="flex items-center gap-1.5 font-lcd text-[9px] uppercase tracking-[0.2em] text-ash">
          <MapPin className="h-3 w-3" />
          <span>{track.name} Circuit</span>
        </div>
        <div className="mt-2 flex items-center justify-center">
          <svg viewBox="0 0 180 160" className="h-32 w-full">
            <motion.path
              key={track.id}
              d={track.mapPath}
              fill="none"
              stroke="#FF8700"
              strokeWidth="3"
              strokeLinecap="round"
              strokeLinejoin="round"
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{ pathLength: 1, opacity: 1 }}
              transition={{ duration: 0.8, ease: "easeInOut" }}
              style={{ filter: "drop-shadow(0 0 4px rgba(255,135,0,0.6))" }}
            />
            {/* Start/finish dot */}
            <motion.circle
              cx="30"
              cy="60"
              r="4"
              fill="#FF8700"
              animate={{ scale: [1, 1.4, 1], opacity: [1, 0.6, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            />
          </svg>
        </div>
        <div className="mt-1 flex justify-between font-lcd text-[9px] uppercase tracking-wider text-ash">
          <span>{track.laps} Laps</span>
          <span>{track.sectors} Sectors</span>
        </div>
      </div>

      {/* Metrics grid */}
      <div className="grid grid-cols-2 gap-2">
        <Metric
          icon={<Gauge className="h-3 w-3" />}
          label="Engine Temp"
          value={telemetry.engineTemp}
          unit="°C"
          pulse={isThinking}
        />
        <Metric
          icon={<Zap className="h-3 w-3" />}
          label="Response"
          value={telemetry.responseSpeed}
          unit="ms"
          color="white"
          pulse={isThinking}
        />
      </div>

      {/* ERS Deployment (full width) */}
      <div className="relative overflow-hidden rounded-lg border border-carbon-500 bg-carbon-900/80 p-3 scanlines">
        <div className="flex items-center justify-between font-lcd text-[9px] uppercase tracking-[0.2em] text-ash">
          <div className="flex items-center gap-1.5">
            <Zap className="h-3 w-3" />
            <span>ERS Deployment</span>
          </div>
          <span className="text-papaya">Tokens</span>
        </div>
        <div className="mt-1.5 flex items-baseline gap-1">
          <AnimatePresence mode="popLayout">
            <motion.span
              key={telemetry.ersDeployment}
              initial={{ opacity: 0, y: -6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 6 }}
              transition={{ duration: 0.15 }}
              className="font-lcd text-2xl font-bold tabular-nums text-papaya glow-papaya"
            >
              {telemetry.ersDeployment}
            </motion.span>
          </AnimatePresence>
          <span className="font-lcd text-xs text-ash">used</span>
        </div>
        {/* Bar */}
        <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-carbon-500">
          <motion.div
            className="h-full rounded-full bg-papaya"
            animate={{
              width: `${Math.min(100, telemetry.ersDeployment / 8)}%`,
            }}
            transition={{ duration: 0.4 }}
          />
        </div>
      </div>

      {/* Race status */}
      <div className="rounded-lg border border-carbon-500 bg-carbon-900/80 p-3 scanlines">
        <div className="flex items-center gap-1.5 font-lcd text-[9px] uppercase tracking-[0.2em] text-ash">
          <Flag className="h-3 w-3" />
          <span>Race Status</span>
        </div>
        <div className="mt-2 space-y-1.5 text-xs">
          <div className="flex justify-between">
            <span className="text-ash">Lap</span>
            <span className="font-lcd text-white">
              {telemetry.lap} / {track.laps}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-ash">DRS</span>
            <span
              className={`font-lcd ${
                telemetry.drsAvailable ? "text-papaya glow-papaya" : "text-ash"
              }`}
            >
              {telemetry.drsAvailable ? "AVAILABLE" : "DISABLED"}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-ash">Key Corner</span>
            <span className="font-lcd text-white">{track.keyCorner}</span>
          </div>
        </div>
      </div>

      {/* Radio link indicator */}
      <div className="mt-auto flex items-center justify-center gap-2 rounded-lg border border-carbon-500 bg-carbon-900/60 py-2">
        <Radio className="h-3.5 w-3.5 text-papaya" />
        <span className="font-lcd text-[9px] uppercase tracking-[0.25em] text-ash">
          Pit Wall Link · Encrypted
        </span>
      </div>
    </aside>
  );
}
