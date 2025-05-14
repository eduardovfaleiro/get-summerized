// src/auth.js
import { reactive } from 'vue';

export const auth = reactive({
    token: localStorage.getItem('access_token') || null,
    login(token) {
        this.token = token;
        localStorage.setItem('access_token', token);
    },
    logout() {
        this.token = null;
        localStorage.removeItem('access_token');
    },
});
