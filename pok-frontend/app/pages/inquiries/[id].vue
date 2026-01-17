<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const inquiryId = route.params.id

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const { data: inquiry, pending, error } = await useFetch(
  `${apiBase}/inquiries/${inquiryId}/`,
  { server: false }
)

const responseText = ref('')

watchEffect(() => {
  if (inquiry.value?.suggested_response) {
    responseText.value = inquiry.value.suggested_response
  }
})

const sendResponse = () => {
  alert('Response sent (simulated)')
}
</script>

<template>
  <div class="max-w-5xl mx-auto p-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Inquiry Details</h1>
      <NuxtLink
        to="/inquiries"
        class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 transition"
      >
        ← Back
      </NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="text-gray-500 dark:text-gray-400">
      Loading...
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-red-600 dark:text-red-400">
      Error loading inquiry
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Mensaje del cliente -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
        <h2 class="font-semibold text-lg mb-4 text-gray-900 dark:text-white flex items-center gap-2">
          <span class="w-1 h-6 bg-blue-500 rounded-full"></span>
          Customer Message
        </h2>
        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
          <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed">
            {{ inquiry?.message }}
          </p>
        </div>
      </div>

      <!-- Respuesta sugerida -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
        <h2 class="font-semibold text-lg mb-4 text-gray-900 dark:text-white flex items-center gap-2">
          <span class="w-1 h-6 bg-purple-500 rounded-full"></span>
          AI Suggested Response
        </h2>

        <textarea
          v-model="responseText"
          rows="6"
          class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition bg-white dark:bg-gray-700 border-gray-200 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 resize-none"
        />

        <div class="flex justify-end mt-4">
          <button
            @click="sendResponse"
            class="bg-blue-600 text-white px-6 py-2.5 rounded-xl hover:bg-blue-700 transition shadow-lg shadow-blue-500/25 font-medium flex items-center gap-2"
          >
            <span>Send Response</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
