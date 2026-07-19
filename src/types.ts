export type ChatMode = "paddock" | "engineer";

export type Role = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: Role;
  content: string;
  mode: ChatMode;
  trackId: string;
  tokensUsed?: number;
  latencyMs?: number;
  error?: boolean;
}

export interface Track {
  id: string;
  name: string;
  country: string;
  laps: number;
  sectors: number;
  keyCorner: string;
  climate: string;
  /** SVG path data for the mini-map silhouette */
  mapPath: string;
}

export interface ChatApiResponse {
  reply: string;
  tokens_used: number;
  latency_ms: number;
}

export interface Telemetry {
  engineTemp: number; // °C  — "AI Load"
  responseSpeed: number; // ms
  ersDeployment: number; // "Tokens Used"
  drsAvailable: boolean;
  lap: number;
}
