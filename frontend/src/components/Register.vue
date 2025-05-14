<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-card class="pa-6" outlined>
        <v-card-title class="headline" style="word-break: break-word;">Crie sua conta no GetSummerized</v-card-title>
        <v-card-subtitle>Entenda mais. Leia menos.</v-card-subtitle>

        <v-text-field
          v-model="email"
          label="E-mail"
          type="email"
          :error="invalidFields.email"
          :error-messages="invalidFields.email ? 'Preencha o e-mail.' : ''"
          outlined
          dense
        />

        <v-text-field
          v-model="password"
          label="Senha"
          type="password"
          :error="invalidFields.password"
          :error-messages="invalidFields.password ? 'Preencha a senha.' : ''"
          outlined
          dense
        />

        <v-text-field
          v-model="confirmPassword"
          label="Confirme a senha"
          type="password"
          :error="invalidFields.confirmPassword"
          :error-messages="invalidFields.confirmPassword ? 'As senhas não coincidem.' : ''"
          outlined
          dense
        />

        <v-alert v-if="errorMessage" type="error" dense>
          {{ errorMessage }}
        </v-alert>
        <v-alert v-if="successMessage" type="success" dense>
          {{ successMessage }}
        </v-alert>

        <v-btn
          color="orange darken-2"
          block
          :loading="isSubmitting"
          @click="register"
        >
          {{ isSubmitting ? 'Cadastrando...' : 'Cadastrar' }}
        </v-btn>

        <div class="text-center mt-4">
          Já possui uma conta?
          <router-link to="/login">Entrar</router-link>
        </div>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import { isValidEmail } from '@/utils/validation.js'

export default {
  name: 'RegisterPage',
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
      errorMessage: '',
      successMessage: '',
      isSubmitting: false,
      invalidFields: {
        email: false,
        password: false,
        confirmPassword: false
      }
    }
  },
  methods: {
    async register() {
      // reset flags & messages
      this.errorMessage = ''
      this.successMessage = ''
      this.invalidFields = {
        email: false,
        password: false,
        confirmPassword: false
      }

      // required fields
      if (!this.email || !this.password || !this.confirmPassword) {
        this.errorMessage = 'Preencha todos os campos.'
        if (!this.email) this.invalidFields.email = true
        if (!this.password) this.invalidFields.password = true
        if (!this.confirmPassword) this.invalidFields.confirmPassword = true
        return
      }

      // email format
      if (!isValidEmail(this.email)) {
        this.errorMessage = 'E-mail inválido.'
        this.invalidFields.email = true
        return
      }

      // password match
      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'As senhas não coincidem.'
        this.invalidFields.password = true
        this.invalidFields.confirmPassword = true
        return
      }

      this.isSubmitting = true
      try {
        const res = await axios.post('/api/register', {
          email: this.email,
          password: this.password
        })
        if (res.status === 201) {
          this.successMessage = 'Usuário criado com sucesso!'
          setTimeout(() => this.$router.push('/login'), 1500)
        }
      } catch (err) {
        if (err.response && err.response.status === 409) {
          this.errorMessage = 'Usuário já existe.'
          this.invalidFields.email = true
        } else if (err.response && err.response.status === 400) {
          this.errorMessage = err.response.data.message
        } else {
          this.errorMessage = 'Erro ao cadastrar. Tente novamente.'
        }
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
</style>
