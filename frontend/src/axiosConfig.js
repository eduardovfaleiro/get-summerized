import axios from 'axios'
import { auth } from './auth.js'
import router from './router/index.js'
import { showToast } from './utils/toast.js'

axios.interceptors.request.use(config => {
    if (auth.token) {
        config.headers.Authorization = `Bearer ${auth.token}`
    }
    return config
})

axios.interceptors.response.use(response => response, error => {
    const status = error.response?.status

    switch(status) {
        case 401:
            auth.logout()
            router.push('/login');
            break
        case 429:
            showToast('Você atingiu o limite de uso. Tente novamente mais tarde.')
            break
        default:
            showToast('Ocorreu um erro inesperado.')
            break
    }

    return Promise.reject(error)
})