import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Projektgerüst (EP-16). Inhalte unter content/ bindet später der Browser-Adapter per import.meta.glob ein.
export default defineConfig({
  plugins: [react()],
});
