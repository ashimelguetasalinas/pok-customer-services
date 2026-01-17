<script setup lang="ts">
definePageMeta({
  middleware: [
    function (to, from) {
      return navigateTo('/inquiries')
    }
  ]
})
</script>

<template>
  <div>Redirecting...</div>
</template>
