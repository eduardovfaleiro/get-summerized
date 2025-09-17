<template>
  <v-app>
    <v-app-bar
      app
      color="white"
      dark
      style="position: fixed;"
      v-if="!$route.meta.hideHeader"
    >
      <div 
        class="d-flex align-center"
        style="position: absolute; left: 50%; transform: translateX(-50%)"
      >
        <v-img
          alt="GetSummerized Logo"
          contain
          src="@/assets/get-summerized-logo.svg"
          transition="scale-transition"
          :width="$vuetify.breakpoint.xs ? 28 : 40"
        />
        <v-img
          alt="GetSummerized Text"
          contain
          min-width="100"
          src="@/assets/get-summerized-text.svg"
          :width="$vuetify.breakpoint.xs ? 130 : 175"
        />
      </div>

      <!-- Right-aligned Logout -->
      <v-spacer/>
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        text
        @click="logout"
      >
        Sair
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import { auth, isTokenExpired } from '@/auth.js'

export default {
  name: 'App',
  computed: {
    isLoggedIn() {
      return !isTokenExpired(auth.token)
    }
  },
  methods: {
    logout() {
      auth.logout()
      this.$router.push('/login')
    }
  }

};
</script>
