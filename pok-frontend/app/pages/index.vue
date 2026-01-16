<script setup lang="ts">
const { inquiries, loading, fetchInquiries } = useInquiries()

onMounted(() => {
  fetchInquiries()
})
</script>

<template>
  <div>
    <h1>Inquiries</h1>

    <div v-if="loading">Loading...</div>

    <ul>
      <li v-for="i in inquiries" :key="i.id">
        {{ i.customer_name }} - {{ i.email }}
      </li>
    </ul>
  </div>
</template>
