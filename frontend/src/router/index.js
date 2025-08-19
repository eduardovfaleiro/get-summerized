import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Welcome from '@/components/Welcome'
import VerifyEmail from '@/components/VerifyEmail'
import { jwtDecode } from 'jwt-decode';
import { auth } from '@/auth'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  {
    path: '/welcome',
    component: Welcome,
    meta: { requiresAuth: true }  // só acessível com token
  },
  { path: '/verify', component: VerifyEmail, meta: { hideHeader: true }}
]

const router = new VueRouter({
  // modo hash (padrão), sem necessidade de configuração extra
  routes
})

function isTokenExpired(token) {
  if (!token) return true;
  const { exp } = jwtDecode(token);
  if (!exp) return true;
  const now = Date.now() / 1000; // timestamp em segundos
  return exp < now;
}

// Guarda global: bloqueia /welcome sem token
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (isTokenExpired(auth.token)) return next('/login')
  }
  next()
})

export default router