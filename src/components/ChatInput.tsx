import { motion } from "framer-motion";
import { Send, CornerDownLeft } from "lucide-react";
import { useRef, useEffect } from "react";
import type { ChatMode } from "../types";

interface ChatInputProps {
  value: string;
  onChange: (v: string) => void;
  onSend: () => void;
  mode: ChatMode;
  disabled: boolean;
}

const PLACEHOLDER: Record<ChatMode, string> = {
  paddock: "Ask the paddock...",
  engineer: "Radio check, what's the strategy?...",
};

export default function ChatInput({
  value,
  onChange,
  onSend,
  mode,
  disabled,
}: ChatInputProps) {
  const ref = useRef<HTMLTextAreaElement>(null);
  const isEngineer = mode === "engineer";

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!disabled && value.trim()) onSend();
    }
  };

  return (
    <div className="px-4 pb-4 sm:px-6">
      <div className="mx-auto max-w-3xl">
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className={`relative flex items-end gap-2 rounded-2xl border bg-carbon-700/90 p-2 shadow-2xl backdrop-blur-xl transition-colors ${
            isEngineer
              ? "border-papaya/40 glow-papaya-box"
              : "border-carbon-400"
          }`}
        >
          <textarea
            ref={ref}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            rows={1}
            placeholder={PLACEHOLDER[mode]}
            className="flex-1 resize-none bg-transparent px-3 py-2.5 text-sm text-white placeholder:text-ash focus:outline-none disabled:opacity-50"
          />
          <button
            onClick={onSend}
            disabled={disabled || !value.trim()}
            aria-label="Send message"
            className={`group flex h-10 w-10 shrink-0 items-center justify-center rounded-xl transition-all ${
              isEngineer
                ? "bg-papaya text-carbon-900 hover:shadow-[0_0_20px_rgba(255,135,0,0.6)]"
                : "bg-papaya text-carbon-900 hover:shadow-[0_0_16px_rgba(255,135,0,0.5)]"
            } disabled:cursor-not-allowed disabled:bg-carbon-500 disabled:text-ash disabled:shadow-none`}
          >
            <Send className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
          </button>
        </motion.div>
        <div className="mt-1.5 flex items-center justify-center gap-1.5 font-lcd text-[9px] uppercase tracking-wider text-ash">
          <CornerDownLeft className="h-3 w-3" />
          <span>Enter to send</span>
          <span className="opacity-50">·</span>
          <span>Shift+Enter for newline</span>
        </div>
      </div>
    </div>
  );
}
