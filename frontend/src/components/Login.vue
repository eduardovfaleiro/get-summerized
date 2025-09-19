<template>
  <v-container class="fill-height" fluid>
    <v-row  align="center" justify="center">
      <v-card class="pa-6" outlined>
        <v-card-title class="headline" style="word-break: break-word;">Bem-vindo ao GetSummerized!</v-card-title>
        <v-card-subtitle>Entenda mais. Leia menos.</v-card-subtitle>

        <v-text-field v-model="email" label="E-mail" type="email" :error="invalidFields.email"
          :error-messages="invalidFields.email ? 'Preencha o e-mail.' : ''" outlined dense />

        <v-text-field v-model="password" label="Senha" type="password" :error="invalidFields.password"
          :error-messages="invalidFields.password ? 'Preencha a senha.' : ''" outlined dense />

        <v-alert v-if="errorMessage" type="error" dense>
          {{ errorMessage }}
        </v-alert>

        <v-btn color="orange darken-2" block @click="login">
          Entrar
        </v-btn>

        <v-divider class="my-4"></v-divider>

        <v-btn color="red darken-1" block @click="loginWithGoogle">
          <v-icon left>mdi-google</v-icon>
          Entrar com Google
        </v-btn>

        <div class="text-center mt-4">
          <span>Não possui uma conta? <router-link to="/register">Cadastrar</router-link></span>
        </div>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import { auth } from '@/auth'
import { safeRequest } from '@/utils/safeRequest';

export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
      invalidFields: {
        email: false,
        password: false
      }
    };
  },
  methods: {
    async loginWithGoogle() {
      const response = await safeRequest(() => axios.get('/api/login/google/initiate'))

      if (response) {
        window.location.href = '/api/login/google'
      }
    },
    login() {
      this.invalidFields.email = false;
      this.invalidFields.password = false;
      this.errorMessage = '';

      if (!this.email || !this.password) {
        if (!this.email) this.invalidFields.email = true;
        if (!this.password) this.invalidFields.password = true;
        this.errorMessage = 'Preencha e-mail e senha.';
        return;
      }

      axios.post('/api/login', {
        email: this.email,
        password: this.password
      })
        .then(response => {
          auth.login(response.data.access_token);
          this.$router.push('/welcome');
        })
        .catch(error => {
          if (error.response && error.response.status == 401) {
            this.invalidFields.email = true;
            this.invalidFields.password = true;
          }

          this.errorMessage = error.response.data.message;
        });
    }
  }
};
</script>

<style scoped>
</style>