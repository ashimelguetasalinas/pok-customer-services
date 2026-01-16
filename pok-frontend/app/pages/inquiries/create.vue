<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useInquiries } from '../composables/useInquiries'

const router = useRouter()
const { createInquiry, getInquiry } = useInquiries()

const processing = ref(false)

const form = ref({
  customer_name: '',
  email: '',
  message: '',
})

const loading = ref(false)
const error = ref<string | null>(null)

const submitForm = async () => {
  loading.value = true
  error.value = null

  try {
    const inquiry = await createInquiry(form.value)

    processing.value = true
    loading.value = false

    const interval = setInterval(async () => {
      const updated = await getInquiry(inquiry.id)

      if (updated.status === 'processed') {
        clearInterval(interval)
        router.push('/inquiries')
      }
    }, 2000)

  } catch (err: any) {
    console.error(err)
    error.value =
      err.data?.detail ||
      'Error al enviar la consulta. Por favor intente nuevamente.'
  } finally {
    loading.value = false
  }
}
</script>

<template>

    <div v-if="processing" class="fixed inset-0 bg-white/80 backdrop-blur-sm flex flex-col items-center justify-center z-50">
        <svg class="animate-spin h-12 w-12 text-blue-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
        >
            <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
            />
            <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
        </svg>

        <p class="text-gray-700 text-sm font-medium">
            Analyzing inquiry with AI…
        </p>
    </div>


  <div class="max-w-2xl mx-auto p-6">
    <!-- Header -->
    <div class="flex items-center gap-4 mb-8">
      <NuxtLink 
        to="/inquiries"
        class="text-gray-500 hover:text-gray-700 transition"
      >
        ← Back
      </NuxtLink>
      <h1 class="text-2xl font-bold text-gray-800">New Inquiry</h1>
    </div>

    <!-- Form Card -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
      <form @submit.prevent="submitForm" class="space-y-6">
        
        <!-- Customer Name -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700 mb-2">Customer Name</label>
          <input
            id="name"
            v-model="form.customer_name"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            placeholder="Ej: Juan Pérez"
          />
        </div>

        <!-- Email -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            placeholder="juan@ejemplo.com"
          />
        </div>

        <!-- Message -->
        <div>
          <label for="message" class="block text-sm font-medium text-gray-700 mb-2">Message</label>
          <textarea
            id="message"
            v-model="form.message"
            required
            rows="5"
            class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition resize-none"
            placeholder="Escriba aquí la consulta del cliente..."
          ></textarea>
        </div>

        <!-- Error Alert -->
        <div v-if="error" class="p-4 bg-red-50 text-red-700 rounded-lg text-sm">
          {{ error }}
        </div>

        <!-- Submit Button -->
        <div class="pt-4">
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-500/30"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Processing...' : 'Create Inquiry' }}
          </button>
        </div>

      </form>
    </div>
  </div>
</template>
