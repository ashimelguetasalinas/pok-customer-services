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
  alert('Respuesta enviada (simulado)')
}
</script>

<template>
  <div class="max-w-5xl mx-auto p-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Detalle del Inquiry</h1>
      <NuxtLink
        to="/inquiries"
        class="text-blue-600 hover:underline"
      >
        ← Volver
      </NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="text-gray-500">
      Cargando...
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-red-600">
      Error al cargar el inquiry
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Mensaje del cliente -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="font-semibold mb-2">Mensaje del Cliente</h2>
        <p class="text-gray-700 whitespace-pre-line">
          {{ inquiry?.message }}

        </p>
      </div>

      <!-- Respuesta sugerida -->
      <div class="bg-white rounded-xl shadow p-6">
        <h2 class="font-semibold mb-2">
          Respuesta sugerida por IA
        </h2>

        <textarea
          v-model="responseText"
          rows="6"
          class="w-full border rounded-lg p-3 focus:outline-none focus:ring focus:ring-blue-200"
        />

        <div class="flex justify-end mt-4">
          <button
            @click="sendResponse"
            class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Enviar respuesta
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
