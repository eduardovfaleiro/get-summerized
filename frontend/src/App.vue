<template>
  <v-app>
    <v-app-bar
      app
      color="white"
      dark
      style="position: fixed;"
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
          width="40"
        />
        <v-img
          alt="GetSummerized Text"
          contain
          min-width="100"
          src="@/assets/get-summerized-text.svg"
          width="200"
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
import { auth } from '@/auth.js'

export default {
  name: 'App',
  computed: {
    isLoggedIn() {
      return !!auth.token
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
