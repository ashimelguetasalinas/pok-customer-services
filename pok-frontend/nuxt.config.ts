import tsconfigPaths from 'vite-tsconfig-paths'

export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/color-mode',
  ],

  css: ['~/assets/css/tailwind.css'],

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000/api'
    }
  },

  srcDir: 'app',

  colorMode: {
    classSuffix: '',
    preference: 'system',
    fallback: 'light',
  },
  vite: {
    plugins: [tsconfigPaths()]
  }
})
