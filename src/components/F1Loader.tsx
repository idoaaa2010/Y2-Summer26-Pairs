import { motion } from "framer-motion";

/**
 * F1-inspired loader: a high-speed spinning Pirelli-style tire ring with
 * a pulsating telemetry radar ring in Papaya Orange.
 */
export default function F1Loader({
  label = "Telemetry sync",
  compact = false,
}: {
  label?: string;
  compact?: boolean;
}) {
  return (
    <div className="flex items-center gap-4">
      <div className={`relative ${compact ? "h-4 w-4" : "h-10 w-10"}`}>
        {/* Outer radar pulse ring */}
        <motion.span
          className="absolute inset-0 rounded-full border-2 border-papaya/40"
          animate={{ scale: [1, 1.35, 1], opacity: [0.6, 0, 0.6] }}
          transition={{ duration: 1.4, repeat: Infinity, ease: "easeOut" }}
        />
        {/* Spinning tire tread */}
        <motion.div
          className="absolute inset-0 rounded-full border-[3px] border-transparent border-t-papaya border-r-papaya/70 border-l-papaya/30"
          animate={{ rotate: 360 }}
          transition={{ duration: 0.7, repeat: Infinity, ease: "linear" }}
        />
        {/* Inner hub */}
        <motion.div
          className="absolute inset-[35%] rounded-full bg-papaya"
          animate={{ opacity: [1, 0.4, 1] }}
          transition={{ duration: 0.9, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>
      {!compact && (
        <span className="font-lcd text-xs uppercase tracking-[0.25em] text-ash">
          {label}
          <motion.span
            className="inline-block w-6"
            animate={{ opacity: [0, 1, 0] }}
            transition={{ duration: 1, repeat: Infinity }}
          >
            …
          </motion.span>
        </span>
      )}
    </div>
  );
}
