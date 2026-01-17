import { jwtDecode } from "jwt-decode";

export const useAuth = () => {
    const token = useCookie('auth_token')
    const user = useState<any>('auth_user', () => null)

    const setUserFromToken = (accessToken: string) => {
        try {
            const decoded: any = jwtDecode(accessToken)
            user.value = {
                username: decoded.username,
                groups: decoded.groups || [],
                isSuperuser: decoded.is_superuser
            }
        } catch (e) {
            user.value = null
        }
    }

    // Initialize user if token exists on load
    if (token.value && !user.value) {
        setUserFromToken(token.value)
    }

    const login = async (username, password) => {
        const config = useRuntimeConfig()
        try {
            const { access } = await $fetch<{ access: string }>(`${config.public.apiBase}/token/`, {
                method: 'POST',
                body: { username, password }
            })

            token.value = access
            setUserFromToken(access)
            return true
        } catch (error) {
            console.error('Login failed', error)
            throw error
        }
    }

    const logout = () => {
        token.value = null
        user.value = null
        const router = useRouter()
        router.push('/login')
    }

    const isAdmin = computed(() => {
        return user.value?.isSuperuser || user.value?.groups.includes('Admin')
    })

    const isSupport = computed(() => {
        return user.value?.groups.includes('Support')
    })

    return {
        token,
        user,
        login,
        logout,
        isAdmin,
        isSupport,
        isAuthenticated: computed(() => !!token.value)
    }
}
