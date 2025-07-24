import axios from 'axios'
import { auth } from './auth.js'
import router from './router/index.js'

axios.interceptors.request.use(config => {
    if (auth.token) {
        config.headers.Authorization = `Bearer ${auth.token}`
    }
    return config
})

axios.interceptors.response.use(response => response, error => {
    if (error.response?.status == 401) {
        auth.logout()
        router.push('/login');
    }
    return Promise.reject(error)
})