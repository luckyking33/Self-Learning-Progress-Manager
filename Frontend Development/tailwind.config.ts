import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{vue,ts,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        soft: "0 20px 60px rgba(15, 23, 42, 0.08)",
      },
      transitionTimingFunction: {
        fluid: "cubic-bezier(0.4, 0, 0.2, 1)",
      },
    },
  },
  plugins: [],
} satisfies Config;
