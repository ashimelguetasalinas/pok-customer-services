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

    // State sharing across components/pages
    const inquiries = useState<Inquiry[]>('inquiries_list', () => [])
    const totalCount = useState<number>('inquiries_total', () => 0)
    const currentPage = useState<number>('inquiries_current_page', () => 1)

    const loading = ref(false)
    const error = ref<string | null>(null)

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

            if (Array.isArray(data)) {
                inquiries.value = data.filter(i => i !== null)
                totalCount.value = inquiries.value.length
            } else if (data && data.results) {
                inquiries.value = data.results.filter((i: any) => i !== null)
                totalCount.value = data.count
            } else {
                inquiries.value = []
                totalCount.value = 0
            }

            currentPage.value = query.page

        } catch (e) {
            console.error(e)
            error.value = 'Error loading inquiries'
        } finally {
            loading.value = false
        }
    }

    const createInquiry = async (payload: any) => {
        const item = await $fetch<Inquiry>(`${apiBase}/inquiries/create/`, {
            method: 'POST',
            body: payload,
        })
        // Optimized: Add to state locally to avoid full refresh if simple
        inquiries.value = [item, ...inquiries.value].slice(0, 10)
        return item
    }

    const getInquiry = async (id: number) => {
        // Optimized: Check shared state first
        const cached = inquiries.value.find(i => i.id === Number(id))
        if (cached) return cached

        return await $fetch<Inquiry>(`${apiBase}/inquiries/${id}/`)
    }

    const updateInquiry = async (id: number, payload: Partial<Inquiry>) => {
        const auth = useAuth()
        const token = auth.token.value

        const updated = await $fetch<Inquiry>(`${apiBase}/inquiries/${id}/`, {
            method: 'PATCH',
            body: payload,
            headers: token ? { Authorization: `Bearer ${token}` } : {}
        })

        // Optimized: Update shared state
        const index = inquiries.value.findIndex(i => i.id === Number(id))
        if (index !== -1) {
            inquiries.value[index] = { ...inquiries.value[index], ...updated }
        }

        return updated
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
        updateInquiry
    }
}
