<template>
  <div class="max-w-md mx-auto mt-10 p-4 border rounded shadow">
    <h2 class="text-xl font-bold mb-4">New Inquiry</h2>

    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label class="block mb-1">Customer Name</label>
        <input v-model="form.customer_name" type="text" class="w-full border p-2 rounded" required />
      </div>

      <div class="mb-3">
        <label class="block mb-1">Email</label>
        <input v-model="form.email" type="email" class="w-full border p-2 rounded" required />
      </div>

      <div class="mb-3">
        <label class="block mb-1">Mensaje</label>
        <textarea v-model="form.message" class="w-full border p-2 rounded" required></textarea>
      </div>

      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded" :disabled="loading">
        {{ loading ? 'Sending...' : 'Create Inquiry' }}
      </button>
    </form>

    <p v-if="success" class="mt-2 text-green-600">Inquiry created successfully!</p>
    <p v-if="error" class="mt-2 text-red-600">{{ error }}</p>

    <NuxtLink href="/inquiries" class="inline-block mt-4 text-blue-600 underline">
      Back to list
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useInquiries } from '../../composables/useInquiries';

const { loading, error, success, createInquiry, getInquiry } = useInquiries()
const router = useRouter()

const form = reactive({
  customer_name: '',
  email: '',
  message: ''
})

const inquiry = reactive<any>(null)

async function submit() {
  const created = await createInquiry(form)

  inquiry.value = created
  const interval = setInterval(async () => {
    const updated = await getInquiry(created.id)

    if (updated.status === 'processed') {
      Object.assign(inquiry.value, updated)
      clearInterval(interval)
      router.push('/inquiries')
    }
  }, 2000)
}
</script>