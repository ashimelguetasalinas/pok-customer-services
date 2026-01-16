<script setup lang="ts">
const colorMode = useColorMode()

const toggleTheme = () => {
  colorMode.preference =
    colorMode.value === 'dark' ? 'light' : 'dark'
}
</script>

<template>
  <button
    @click="toggleTheme"
    class="px-3 py-2 rounded-lg text-sm border
           bg-gray-100 dark:bg-gray-800
           text-gray-800 dark:text-gray-100
           transition"
  >
    <span v-if="colorMode.value === 'dark'">🌙 Dark</span>
    <span v-else>☀️ Light</span>
  </button>
</template>
