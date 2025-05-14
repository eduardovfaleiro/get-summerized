import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' // <- importação do Vuetify

Vue.config.productionTip = false

new Vue({
  router,
  vuetify, // <- aqui você adiciona o Vuetify à instância
  render: h => h(App)
}).$mount('#app')
