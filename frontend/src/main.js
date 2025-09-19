import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' // <- importação do Vuetify
import './axiosConfig'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"
import { auth } from './auth.js'
import { registerToast } from './utils/toast'

const hash = window.location.hash; // Ex: "#/welcome?token=abc123"

// Verificação para garantir que a URL tem uma query string
if (hash.includes('?')) {
    const queryString = hash.split('?')[1];
    const urlParams = new URLSearchParams(queryString);
    const token = urlParams.get('token');

    if (token) {
        // 1. Loga o usuário
        auth.login(token);

        // 2. Remove o token da URL
        const newHash = hash.split('?')[0]; // Pega a parte antes do '?' (ex: "#/welcome")
        window.history.replaceState({}, document.title, newHash);
    }
}


Vue.use(Toast)
Vue.config.productionTip = false

const app = new Vue({
  router,
  vuetify, // <- aqui você adiciona o Vuetify à instância
  render: h => h(App)
})

registerToast(app.$toast)

app.$mount('#app')
