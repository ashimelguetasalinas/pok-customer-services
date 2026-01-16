<script setup lang="ts">
defineProps<{
  category: string | null
}>()




const map: Record<string, string> = {
  'sales': 'bg-blue-100 text-blue-800',
  'technical_support': 'bg-purple-100 text-purple-800',
  'complaint': 'bg-red-100 text-red-800',
  'spam': 'bg-gray-200 text-gray-700',
  "billing": 'bg-green-100 text-green-800',
  "general_inquiry": 'bg-yellow-100 text-yellow-800',
}
</script>

<template>
  <span
    class="px-2 py-1 rounded-full text-xs font-medium"
    :class="map[category ?? ''] || 'bg-gray-100 text-gray-600'"
  >
    {{ category ?? 'Sin clasificar' }}
  </span>
</template>
