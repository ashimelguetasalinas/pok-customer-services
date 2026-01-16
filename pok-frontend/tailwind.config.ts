/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    content: [
        './components/**/*.{vue,js,ts}',
        './layouts/**/*.{vue,js,ts}',
        './pages/**/*.{vue,js,ts}',
        './app.vue',
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}