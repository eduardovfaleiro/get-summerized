// src/auth.js
import { reactive } from 'vue';
import { jwtDecode } from 'jwt-decode';

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

export function isTokenExpired(token) {
  if (!token) return true;
  const { exp } = jwtDecode(token);
  if (!exp) return true;
  const now = Date.now() / 1000; // timestamp em segundos
  return exp < now;
}