import { motion, AnimatePresence } from "framer-motion";
import { User, Radio } from "lucide-react";
import type { ChatMessage } from "../types";
import F1Loader from "./F1Loader";

interface ChatBubbleProps {
  message: ChatMessage;
  isStreaming?: boolean;
}

/** Parse the [Summary]/[Response]/[Next Step] format into styled blocks. */
function parseBlocks(text: string) {
  const blocks: { label: string; text: string }[] = [];
  const regex = /\[(Summary|Response|Next Step)\]:\s*([^\[]*)/g;
  let m;
  while ((m = regex.exec(text)) !== null) {
    blocks.push({ label: m[1], text: m[2].trim() });
  }
  return blocks;
}

export default function ChatBubble({ message, isStreaming }: ChatBubbleProps) {
  const isUser = message.role === "user";
  const isEngineer = message.mode === "engineer";

  if (isUser) {
    return (
      <motion.div
        layout
        initial={{ opacity: 0, y: 12, x: 8 }}
        animate={{ opacity: 1, y: 0, x: 0 }}
        transition={{ duration: 0.25 }}
        className="flex justify-end"
      >
        <div className="flex max-w-[85%] items-start gap-2.5 sm:max-w-[75%]">
          <div className="rounded-2xl rounded-tr-sm border border-carbon-400 bg-carbon-600 px-4 py-2.5 text-sm text-white">
            {message.content}
          </div>
          <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-carbon-500 text-ash">
            <User className="h-4 w-4" />
          </div>
        </div>
      </motion.div>
    );
  }

  const blocks = parseBlocks(message.content);
  const hasBlocks = blocks.length > 0;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 12, x: -8 }}
      animate={{ opacity: 1, y: 0, x: 0 }}
      transition={{ duration: 0.25 }}
      className="flex justify-start"
    >
      <div className="flex max-w-[88%] items-start gap-2.5 sm:max-w-[80%]">
        <div
          className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
            isEngineer
              ? "bg-papaya text-carbon-900"
              : "bg-carbon-500 text-white"
          }`}
        >
          <Radio className="h-4 w-4" />
        </div>
        <div
          className={`rounded-2xl rounded-tl-sm border px-4 py-3 text-sm ${
            message.error
              ? "border-red-500/60 bg-red-500/15 text-white"
              : isEngineer
              ? "border-papaya/30 bg-carbon-700 text-white"
              : "border-carbon-400 bg-carbon-700 text-white"
          }`}
        >
          {hasBlocks ? (
            <div className="space-y-2">
              {blocks.map((b, i) => (
                <div key={i}>
                  <div
                    className={`font-lcd text-[10px] uppercase tracking-[0.2em] ${
                      b.label === "Next Step"
                        ? "text-papaya glow-papaya"
                        : b.label === "Summary"
                        ? "text-ash"
                        : "text-white"
                    }`}
                  >
                    {b.label}
                  </div>
                  <div className="mt-0.5 leading-relaxed">{b.text}</div>
                </div>
              ))}
            </div>
          ) : (
            <div className="leading-relaxed whitespace-pre-wrap">{message.content}</div>
          )}

          {isStreaming && (
            <div className="mt-3 border-t border-carbon-500 pt-2">
              <F1Loader label="Receiving telemetry" />
            </div>
          )}

          {!isStreaming && !message.error && (message.tokensUsed || message.latencyMs) && (
            <div className="mt-2 flex items-center gap-3 border-t border-carbon-500/60 pt-1.5 font-lcd text-[9px] uppercase tracking-wider text-ash">
              {message.latencyMs ? <span>{message.latencyMs}ms</span> : null}
              {message.tokensUsed ? (
                <>
                  <span>·</span>
                  <span>{message.tokensUsed} tok</span>
                </>
              ) : null}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
