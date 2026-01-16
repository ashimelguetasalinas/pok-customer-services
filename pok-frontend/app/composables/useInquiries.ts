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

    // 🔹 LISTADO
    const fetchInquiries = async () => {
        loading.value = true
        error.value = null

        try {
            inquiries.value = await $fetch<Inquiry[]>(`${apiBase}/inquiries/`)
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
        loading,
        error,
        fetchInquiries,
        createInquiry,
        getInquiry,
    }
}
