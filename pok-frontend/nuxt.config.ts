import tsconfigPaths from 'vite-tsconfig-paths'

export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss'],

  css: ['~/assets/css/tailwind.css'],

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000/api'
    }
  },

  vite: {
    plugins: [tsconfigPaths()] // <--- esto permite que ~ funcione
  }
})
