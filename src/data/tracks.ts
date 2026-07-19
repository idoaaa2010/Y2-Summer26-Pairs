import type { Track } from "../types";

/**
 * Iconic F1 circuits. `mapPath` is a simplified SVG silhouette used for the
 * mini-map in the telemetry dashboard.
 */
export const TRACKS: Track[] = [
  {
    id: "monaco",
    name: "Monaco",
    country: "Monaco",
    laps: 78,
    sectors: 3,
    keyCorner: "Grand Hotel Hairpin",
    climate: "Mediterranean, 24°C, light sea breeze",
    mapPath:
      "M30 60 C 50 30, 90 25, 110 45 S 150 70, 150 90 S 120 120, 90 110 S 40 100, 30 60 Z",
  },
  {
    id: "silverstone",
    name: "Silverstone",
    country: "UK",
    laps: 52,
    sectors: 3,
    keyCorner: "Copse",
    climate: "Overcast, 16°C, gusty crosswinds",
    mapPath:
      "M20 80 C 30 40, 80 30, 120 50 C 160 70, 160 110, 120 120 C 70 130, 20 120, 20 80 Z",
  },
  {
    id: "monza",
    name: "Monza",
    country: "Italy",
    laps: 53,
    sectors: 3,
    keyCorner: "Parabolica",
    climate: "Dry, 28°C, low downforce, high top speed",
    mapPath:
      "M40 30 L 140 30 L 160 80 L 140 130 L 40 130 L 20 80 Z",
  },
  {
    id: "spa",
    name: "Spa",
    country: "Belgium",
    laps: 44,
    sectors: 3,
    keyCorner: "Eau Rouge",
    climate: "Changeable, 18°C, rain likely in sector 3",
    mapPath:
      "M20 120 C 40 60, 80 40, 100 70 C 120 100, 140 50, 160 30",
  },
  {
    id: "austria",
    name: "Austria",
    country: "Austria",
    laps: 71,
    sectors: 3,
    keyCorner: "Turn 3",
    climate: "Sunny, 26°C, high altitude, thin air",
    mapPath:
      "M80 25 L 140 70 L 120 130 L 40 130 L 20 70 Z",
  },
];

export const DEFAULT_TRACK = TRACKS[0];

export function getTrack(id: string): Track {
  return TRACKS.find((t) => t.id === id) ?? DEFAULT_TRACK;
}
