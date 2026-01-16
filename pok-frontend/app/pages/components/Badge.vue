<template>
  <span
    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
    :class="colorClass"
  >
    {{ label }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{
  label: string
  type?: 'status' | 'sentiment' | 'category'
}>()

const colorClass = computed(() => {
  if (props.type === 'status') {
    if (props.label === 'pending')
      return 'bg-yellow-100 text-yellow-800'
    if (props.label === 'responded')
      return 'bg-green-100 text-green-800'
  }

  if (props.type === 'sentiment') {
    if (props.label === 'positive')
      return 'bg-green-100 text-green-800'
    if (props.label === 'negative')
      return 'bg-red-100 text-red-800'
    return 'bg-gray-100 text-gray-700'
  }

  return 'bg-blue-100 text-blue-800'
})
</script>
