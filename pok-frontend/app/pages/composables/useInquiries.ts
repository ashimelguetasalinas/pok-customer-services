export function useInquiries() {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  const inquiries = ref([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchInquiries = async () => {
    loading.value = true
    error.value = null

    try {
      const data = await $fetch(
        `${apiBase}/inquiries/`, // SLASH FINAL
        {
          method: 'GET'
        }
      )

      inquiries.value = data as any[]
    } catch (e) {
      console.error(e)
      error.value = 'Error al cargar inquiries'
    } finally {
      loading.value = false
    }
  }

  return {
    inquiries,
    loading,
    error,
    fetchInquiries
  }
}
