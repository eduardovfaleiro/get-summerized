import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' // <- importação do Vuetify
import './axiosConfig'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"
import { auth } from './auth.js'
import { registerToast } from './utils/toast'

// TODO(melhorar isso aqui)
const hash = window.location.hash; // Ex: "#/welcome?token=abc123"
const queryString = hash.split('?')[1]; // "token=abc123"
const urlParams = new URLSearchParams(queryString);
const token = urlParams.get('token');

if (token) {
  auth.login(token)
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
