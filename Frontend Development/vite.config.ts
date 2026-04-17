import { fileURLToPath, URL } from "node:url";

import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";
import { viteMockServe } from "vite-plugin-mock";

export default defineConfig({
  plugins: [
    vue(),
    viteMockServe({
      mockPath: "mock",
      enable: true,
      localEnabled: true,
      prodEnabled: false,
      watchFiles: true,
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    port: 5173,
  },
});

