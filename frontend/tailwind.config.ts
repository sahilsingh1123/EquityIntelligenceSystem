import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17212b",
        panel: "#f7f9fb",
        line: "#d9e2ec",
        gain: "#0e8f64",
        loss: "#c43d3d",
        caution: "#b7791f",
        info: "#2563a9"
      },
      boxShadow: {
        soft: "0 8px 24px rgba(23, 33, 43, 0.08)"
      }
    }
  },
  plugins: []
};

export default config;
