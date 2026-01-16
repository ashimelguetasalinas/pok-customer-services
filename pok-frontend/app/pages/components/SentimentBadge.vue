<script setup lang="ts">
const props = defineProps<{ sentiment: string | null }>()

const normalized = computed(() =>
  props.sentiment?.toLowerCase()
)

const map: Record<string, string> = {
  positive: 'bg-green-100 text-green-800',
  neutral: 'bg-yellow-100 text-yellow-800',
  negative: 'bg-red-100 text-red-800',
}
</script>

<template>
  <span
    class="px-2 py-1 rounded-full text-xs font-medium"
    :class="map[normalized ?? ''] || 'bg-gray-100 text-gray-600'"
  >
    {{ sentiment ?? 'Sin clasificar' }}
  </span>
</template>
