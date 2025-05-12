<template>
  <div class="register-container">
    <div class="register">
      <h2>Crie sua conta no GetSummerized</h2>
      <p>Entenda mais. Leia menos.</p>


      <input v-model="email" type="email" placeholder="E-mail" :class="{ 'input-error': invalidFields.email }" />
      <input v-model="password" type="password" placeholder="Senha"
        :class="{ 'input-error': invalidFields.password }" />
      <input v-model="confirmPassword" type="password" placeholder="Confirme a senha"
        :class="{ 'input-error': invalidFields.confirmPassword }" />

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

      <button class="register-btn" @click="register" :disabled="isSubmitting">
        {{ isSubmitting ? 'Cadastrando...' : 'Cadastrar' }}
      </button>

      <p class="login-link">
        Já possui uma conta?
        <router-link to="/login">Entrar</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
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
    };
  },
  methods: {
    async register() {
      this.errorMessage = '';
      this.successMessage = '';
      this.invalidFields = { email: false, password: false, confirmPassword: false };

      if (!this.email || !this.password || !this.confirmPassword) {
        this.errorMessage = 'Preencha todos os campos.';
        if (!this.email) this.invalidFields.email = true;
        if (!this.password) this.invalidFields.password = true;
        if (!this.confirmPassword) this.invalidFields.confirmPassword = true;
        return;
      }

      if (!isValidEmail(this.email)) {
        this.errorMessage = 'E-mail inválido.';
        this.invalidFields.email = true;
        return;
      }

      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'As senhas não coincidem.';
        this.invalidFields.password = true;
        this.invalidFields.confirmPassword = true;
        return;
      }

      this.isSubmitting = true;
      try {
        const response = await axios.post('http://127.0.0.1:5000/register', {
          email: this.email,
          password: this.password
        });

        if (response.status === 201) {
          this.successMessage = 'Usuário criado com sucesso!';
          setTimeout(() => {
            this.$router.push('/login');
          }, 1500);
        }
      } catch (error) {
        if (error.response && error.response.status === 409) {
          this.errorMessage = 'Usuário já existe.';
          this.invalidFields.email = true;
        } else if (error.response && error.response.status === 400) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = 'Erro ao cadastrar. Tente novamente.';
        }
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.register-container {
  display: flex;
  height: 100vh;
  font-family: sans-serif;
}

.register {
  flex: 1;
  padding: 4rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: white;
  max-width: 500px;
  width: 100%;
  margin: auto;
}

.register h2 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.register p:not(.error-message) {
  margin-bottom: 1.5rem;
  color: #666;
}

.register input {
  margin-bottom: 1rem;
  padding: 0.75rem;
  font-size: 1rem;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 6px;
  transition: border-color 0.3s;
  box-sizing: inherit;
}

.input-error {
  border-color: red !important;
}

.register-btn {
  background-color: #6c63ff;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1rem;
  cursor: pointer;
  width: 100%;
  box-sizing: inherit;
}

.login-link {
  margin-top: 1rem;
  font-size: 0.9rem;
}

.error-message {
  color: red;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.success-message {
  color: green;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
</style>
