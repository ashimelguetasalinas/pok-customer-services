<template>
  <div class="border p-4 rounded shadow mb-2 hover:bg-gray-50 cursor-pointer" @click="$router.push(`/inquiry/${inquiry.id}`)">
    <h3 class="font-bold">{{ inquiry.customer_name }}</h3>
    <p>{{ inquiry.message.substring(0, 100) }}...</p>
    <div class="flex gap-2 mt-2">
      <Badge type="category" :value="inquiry.category" label="Category" />
      <Badge type="sentiment" :value="inquiry.sentiment" label="Sentiment" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Inquiry } from '@/composables/useInquiries'
import Badge from './Badge.vue'

defineProps<{
  inquiry: Inquiry
}>()
</script>
