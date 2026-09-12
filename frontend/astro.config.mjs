import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

const API_URL = process.env.PUBLIC_API_URL || 'http://localhost:8000';

export default defineConfig({
  output: 'static',
  integrations: [react(), tailwind()],
  server: { port: 4321 },
  vite: {
    server: {
      proxy: {
        '/api': {
          target: API_URL,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  },
});
