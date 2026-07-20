/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        carbon: {
          900: "#0a0a0a",
          800: "#111111",
          700: "#1a1a1a",
          600: "#222222",
          500: "#2a2a2a",
          400: "#3a3a3a",
        },
        papaya: {
          DEFAULT: "#FF8700",
          50: "#FFF4E6",
          100: "#FFE3BF",
          200: "#FFCB80",
          300: "#FFB04D",
          400: "#FF9A1F",
          500: "#FF8700",
          600: "#E67300",
          700: "#B85A00",
          800: "#7a3d00",
        },
        cream: "#F5F5F5",
        ash: "#A3A3A3",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
        lcd: ["DSEG7 Classic", "Share Tech Mono", "ui-monospace", "monospace"],
      },
      backgroundImage: {
        "carbon-fiber":
          "radial-gradient(circle at 20% 20%, rgba(255,135,0,0.04) 0%, transparent 40%), radial-gradient(circle at 80% 70%, rgba(255,135,0,0.03) 0%, transparent 45%), repeating-linear-gradient(45deg, #0e0e0e 0px, #0e0e0e 2px, #131313 2px, #131313 4px)",
      },
      keyframes: {
        "pulse-glow": {
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(255,135,0,0.5)" },
          "50%": { boxShadow: "0 0 24px 4px rgba(255,135,0,0.35)" },
        },
        "spin-fast": {
          to: { transform: "rotate(360deg)" },
        },
        "flicker": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.85" },
        },
      },
      animation: {
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "spin-fast": "spin-fast 0.6s linear infinite",
        "flicker": "flicker 3s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
