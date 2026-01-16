<script setup lang="ts">
import { onMounted } from 'vue'
import { useInquiries } from '../composables/useInquiries'
import CategoryBadge from '../components/CategoryBadge.vue'
import SentimentBadge from '../components/SentimentBadge.vue'


const { inquiries, loading, error, fetchInquiries } = useInquiries()

onMounted(() => {
  fetchInquiries()
})
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-semibold mb-4">Inquiries</h1>

    <!-- Loading -->
    <div v-if="loading" class="text-gray-500">
      Cargando consultas...
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-red-600">
      {{ error }}
    </div>

    <!-- Empty -->
    <div v-else-if="inquiries.length === 0" class="text-gray-500">
      No hay consultas aún.
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto">
      <table class="min-w-full border border-gray-200 rounded-lg">
        <thead class="bg-gray-50">
          <tr>
            <th class="th">Client</th>
            <th class="th">Email</th>
            <th class="th">Category</th>
            <th class="th">Sentimient</th>
            <th class="th">Status</th>
            <th class="th">Date</th>
            <th class="th">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="inquiry in inquiries"
            :key="inquiry.id"
            class="border-t hover:bg-gray-50 cursor-pointer"
          >
            <td class="td font-medium">{{ inquiry.customer_name }}</td>
            <td class="td text-sm text-gray-600">{{ inquiry.email }}</td>

            <td class="td">
              <CategoryBadge :category="inquiry.category" />
            </td>

            <td class="td">
              <SentimentBadge :sentiment="inquiry.sentiment" />
            </td>

            <td class="td capitalize">{{ inquiry.status }}</td>

            <td class="td text-sm text-gray-500">
              {{ new Date(inquiry.created_at).toLocaleDateString() }}
            </td>

          <td class="p-3">
            <NuxtLink
              :to="`/inquiries/${inquiry.id}`"
              class="
                inline-flex items-center gap-2
                px-3 py-1.5
                rounded-md
                bg-blue-600
                text-white text-sm font-medium
                hover:bg-blue-700
                transition
              "
            >
              Ver detalle
              <span class="text-xs">→</span>
            </NuxtLink>
          </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.th {
  @apply px-4 py-2 text-left text-sm font-semibold text-gray-700;
}
.td {
  @apply px-4 py-2 text-sm;
}
</style>
