import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// The PWA console. Proxies /v1 to the core API in dev so the WS stream and REST share an origin.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/v1": {
        target: process.env.VITE_API_BASE || "http://localhost:8000",
        changeOrigin: true,
        ws: true,
      },
    },
  },
});
