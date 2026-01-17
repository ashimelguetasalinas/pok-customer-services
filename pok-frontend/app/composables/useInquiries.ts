import { ref } from 'vue'

export interface Inquiry {
    id: number;
    customer_name: string;
    email: string;
    message: string;
    category: string | null;
    sentiment: string | null;
    suggested_response: string | null;
    status: string;
    created_at: string;
}

export function useInquiries() {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const inquiries = ref<Inquiry[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    // 🔹 LISTADO (con filtros y paginación)
    const totalCount = ref(0)
    const currentPage = ref(1)

    const fetchInquiries = async (params: { page?: number, search?: string, category?: string, sentiment?: string } = {}) => {
        loading.value = true
        error.value = null

        const query: any = {
            page: params.page || 1,
        }

        if (params.search) query.search = params.search
        if (params.category) query.category = params.category
        if (params.sentiment) query.sentiment = params.sentiment

        try {
            const data: any = await $fetch(`${apiBase}/inquiries/`, {
                params: query
            })

            console.log("API Response:", data) // DEBUG

            if (Array.isArray(data)) {
                // Backend sent a plain list
                inquiries.value = data.filter(i => i !== null && i !== undefined)
                totalCount.value = inquiries.value.length
            } else if (data && data.results && Array.isArray(data.results)) {
                // Backend sent paginated response
                inquiries.value = data.results.filter((i: any) => i !== null && i !== undefined)
                totalCount.value = data.count
            } else {
                console.warn("Unexpected response format:", data)
                inquiries.value = []
                totalCount.value = 0
            }

            currentPage.value = query.page

        } catch (e) {
            console.error(e)
            error.value = 'Error al cargar inquiries'
        } finally {
            loading.value = false
        }
    }

    const createInquiry = async (payload: any) => {
        return await $fetch<Inquiry>(`${apiBase}/inquiries/create/`, {
            method: 'POST',
            body: payload,
        })
    }

    const getInquiry = async (id: number) => {
        return await $fetch<Inquiry>(`${apiBase}/inquiries/${id}/`)
    }

    return {
        inquiries,
        totalCount,
        currentPage,
        loading,
        error,
        fetchInquiries,
        createInquiry,
        getInquiry,
    }
}
