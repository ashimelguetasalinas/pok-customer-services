<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useInquiries } from '../../composables/useInquiries'
import CategoryBadge from '../../components/CategoryBadge.vue'
import SentimentBadge from '../../components/SentimentBadge.vue'

const { inquiries, totalCount, currentPage, loading, error, fetchInquiries } = useInquiries()

const search = ref('')
const category = ref('')
const sentiment = ref('')
let pollingInterval: any = null

// Debounce search could be better, but simple watch is fine for now
watch([category, sentiment], () => {
  fetchInquiries({ page: 1, search: search.value, category: category.value, sentiment: sentiment.value })
})

let searchTimeout: any
const onSearchInput = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchInquiries({ page: 1, search: search.value, category: category.value, sentiment: sentiment.value })
  }, 500)
}

const changePage = (newPage: number) => {
  fetchInquiries({ page: newPage, search: search.value, category: category.value, sentiment: sentiment.value })
}

const getInitials = (name: string) => {
  return name
    ? name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    : '?'
}

const checkPendingStatus = () => {
  const hasPending = inquiries.value.some(i => i.status === 'pending')
  
  if (hasPending) {
    // Silent refresh - preserve loading state if possible or just fetch
    fetchInquiries({ 
      page: currentPage.value, 
      search: search.value, 
      category: category.value, 
      sentiment: sentiment.value 
    })
  }
}

onMounted(() => {
  fetchInquiries()
  
  // Poll every 5 seconds
  pollingInterval = setInterval(checkPendingStatus, 5000)
})

onUnmounted(() => {
  if (pollingInterval) clearInterval(pollingInterval)
})
</script>

<template>
  <div class="p-6 max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Inquiries</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Manage and respond to customer questions</p>
      </div>
      <NuxtLink 
        to="/inquiries/create"
        class="bg-blue-600 text-white px-5 py-2.5 rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/25 flex items-center gap-2 font-medium"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        New Inquiry
      </NuxtLink>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 mb-6 flex flex-wrap gap-4 items-center">
      <div class="flex-1 min-w-[240px] relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input 
          v-model="search"
          @input="onSearchInput"
          placeholder="Search items..."
          class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400"
        />
      </div>
      
      <select v-model="category" class="px-4 py-2 border border-gray-200 rounded-lg text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none cursor-pointer">
        <option value="">All Categories</option>
        <option value="sales">Sales</option>
        <option value="technical_support">Technical Support</option>
        <option value="billing">Billing</option>
        <option value="complaint">Complaint</option>
        <option value="general_inquiry">General Inquiry</option>
        <option value="spam">Spam</option>
      </select>

      <select v-model="sentiment" class="px-4 py-2 border border-gray-200 rounded-lg text-sm bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none cursor-pointer">
        <option value="">All Sentiments</option>
        <option value="positive">Positive</option>
        <option value="neutral">Neutral</option>
        <option value="negative">Negative</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 flex items-center gap-3">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      {{ error }}
    </div>

    <!-- Empty -->
    <div v-else-if="inquiries.length === 0" class="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-dashed border-gray-200 dark:border-gray-700">
      <div class="mx-auto h-12 w-12 text-gray-400 mb-3">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white">No inquiries found</h3>
      <p class="mt-1 text-gray-500">Get started by creating a new inquiry.</p>
    </div>

    <!-- Table -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700/50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Customer</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Message Preview</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Category</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Sentiment</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Date</th>
              <th scope="col" class="relative px-6 py-3">
                <span class="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr
              v-for="item in inquiries"
              :key="item?.id"
              class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors group cursor-pointer"
              @click="$router.push(`/inquiries/${item?.id}`)"
            >
              <!-- Customer -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold text-sm shadow-sm">
                      {{ getInitials(item?.customer_name) }}
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ item?.customer_name || 'Unknown' }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">{{ item?.email || 'No email' }}</div>
                  </div>
                </div>
              </td>

              <!-- Message Preview -->
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900 dark:text-white max-w-xs truncate">
                  {{ item?.message || 'No message content' }}
                </div>
              </td>

              <!-- Status -->
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full capitalize"
                  :class="{
                    'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300': item?.status === 'processed',
                    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300': item?.status === 'pending',
                    'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300': item?.status === 'failed'
                  }"
                >
                  <span class="w-1.5 h-1.5 rounded-full mr-1.5 self-center" 
                    :class="{
                      'bg-green-400': item?.status === 'processed',
                      'bg-yellow-400': item?.status === 'pending',
                      'bg-red-400': item?.status === 'failed'
                    }"
                  ></span>
                  {{ item?.status }}
                </span>
              </td>

              <!-- Category -->
              <td class="px-6 py-4 whitespace-nowrap">
                <CategoryBadge :category="item?.category ?? null" />
              </td>

              <!-- Sentiment -->
              <td class="px-6 py-4 whitespace-nowrap">
                <SentimentBadge :sentiment="item?.sentiment ?? null" />
              </td>

              <!-- Date -->
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ item?.created_at ? new Date(item.created_at).toLocaleDateString() : '-' }}
              </td>

              <!-- Actions -->
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <span class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300 opacity-0 group-hover:opacity-100 transition-opacity">
                  View Details →
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div class="bg-white dark:bg-gray-800 px-4 py-3 flex items-center justify-between border-t border-gray-200 dark:border-gray-700 sm:px-6">
        <div class="flex-1 flex justify-between sm:hidden">
          <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">Previous</button>
          <button @click="changePage(currentPage + 1)" :disabled="currentPage * 10 >= totalCount" class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">Next</button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700 dark:text-gray-400">
              Showing page
              <span class="font-medium">{{ currentPage }}</span>
              of
              <span class="font-medium">{{ Math.ceil(totalCount / 10) || 1 }}</span>
              results ({{ totalCount }} total)
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button 
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50"
              >
                <span class="sr-only">Previous</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
              <button 
                @click="changePage(currentPage + 1)"
                :disabled="currentPage * 10 >= totalCount"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50"
              >
                <span class="sr-only">Next</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>
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
