<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: string | null | undefined
}>()

const statusConfig = computed(() => {
  const s = props.status?.toLowerCase()
  switch (s) {
    case 'processed':
      return {
        label: 'Processed',
        classes: 'bg-green-50 text-green-700 border-green-200 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800/50'
      }
    case 'pending':
      return {
        label: 'Pending',
        classes: 'bg-yellow-50 text-yellow-700 border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-300 dark:border-yellow-800/50'
      }
    case 'failed':
      return {
        label: 'Failed',
        classes: 'bg-red-50 text-red-700 border-red-200 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800/50'
      }
    case 'finished':
      return {
        label: 'Finished',
        classes: 'bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900/40 dark:text-blue-200 dark:border-blue-800'
      }
    default:
      return {
        label: props.status || 'Unknown',
        classes: 'bg-gray-50 text-gray-700 border-gray-200 dark:bg-gray-900/20 dark:text-gray-300 dark:border-gray-800/50'
      }
  }
})
</script>

<template>
  <span 
    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border transition-colors"
    :class="statusConfig.classes"
  >
    <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="{
        'bg-green-500': status?.toLowerCase() === 'processed',
        'bg-yellow-500': status?.toLowerCase() === 'pending',
        'bg-red-500': status?.toLowerCase() === 'failed',
        'bg-blue-500': status?.toLowerCase() === 'finished',
        'bg-gray-400': !['processed', 'pending', 'failed', 'finished'].includes(status?.toLowerCase() || '')
    }"></span>
    {{ statusConfig.label }}
  </span>
</template>
