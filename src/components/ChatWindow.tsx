import { motion, AnimatePresence } from "framer-motion";
import { AlertTriangle, X } from "lucide-react";
import type { ChatMessage } from "../types";
import ChatBubble from "./ChatBubble";
import F1Loader from "./F1Loader";

interface ChatWindowProps {
  messages: ChatMessage[];
  isThinking: boolean;
  streamingId: string | null;
  error: string | null;
  onDismissError: () => void;
}

export default function ChatWindow({
  messages,
  isThinking,
  streamingId,
  error,
  onDismissError,
}: ChatWindowProps) {
  return (
    <div className="relative flex h-full flex-col">
      {/* Error banner */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -20, height: 0 }}
            animate={{ opacity: 1, y: 0, height: "auto" }}
            exit={{ opacity: 0, y: -20, height: 0 }}
            className="z-10"
          >
            <div className="mx-4 mt-3 flex items-center gap-3 rounded-lg border border-red-500/50 bg-gradient-to-r from-red-600/90 to-papaya/80 px-4 py-3 shadow-lg">
              <AlertTriangle className="h-5 w-5 shrink-0 text-white" />
              <div className="flex-1">
                <div className="text-sm font-bold uppercase tracking-wide text-white">
                  Pit Lane Error
                </div>
                <div className="text-xs text-white/90">{error}</div>
              </div>
              <button
                onClick={onDismissError}
                className="rounded p-1 text-white/80 transition-colors hover:bg-white/10 hover:text-white"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 sm:px-6">
        <div className="mx-auto flex max-w-3xl flex-col gap-4">
          <AnimatePresence initial={false}>
            {messages.map((m) => (
              <ChatBubble
                key={m.id}
                message={m}
                isStreaming={streamingId === m.id}
              />
            ))}
          </AnimatePresence>

          {isThinking && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="flex justify-start"
            >
              <div className="flex items-center gap-2.5">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-papaya text-carbon-900">
                  <F1Loader compact />
                </div>
                <div className="rounded-2xl rounded-tl-sm border border-papaya/30 bg-carbon-700 px-4 py-3">
                  <F1Loader label="Syncing telemetry" />
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
