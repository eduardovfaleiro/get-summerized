<template>
  <div class="login-container">
    <div class="login">
      <h2>Bem-vindo ao GetSummerized!</h2>
      <p>Entenda mais. Leia menos.</p>

      <input v-model="email" type="email" placeholder="E-mail" :class="{ 'input-error': invalidFields.email }" />
      <input v-model="password" type="password" placeholder="Senha"
        :class="{ 'input-error': invalidFields.password }" />

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <button class="login-btn" @click="login">Entrar</button>

      <p class="signup-link">
        Não possui uma conta?
        <router-link to="/register">Cadastrar</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

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
    login() {
      // reseta flags
      this.invalidFields.email = false;
      this.invalidFields.password = false;

      if (!this.email || !this.password) {
        if (!this.email) this.invalidFields.email = true;
        if (!this.password) this.invalidFields.password = true;
        this.errorMessage = 'Preencha e-mail e senha.';
        return;
      }

      axios.post('http://127.0.0.1:5000/login', {
        email: this.email,
        password: this.password
      })
        .then(response => {
          localStorage.setItem('access_token', response.data.access_token);
          this.$router.push('/welcome');
        })
        .catch(() => {
          // marca ambos em erro para garantir feedback
          this.invalidFields.email = true;
          this.invalidFields.password = true;
          this.errorMessage = 'E-mail ou senha incorretos.';
        });
    }
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.login-container {
  display: flex;
  height: 100vh;
  font-family: sans-serif;
}

.login {
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

.login h2 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.login p:not(.error-message) {
  margin-bottom: 1.5rem;
  color: #666;
}

.login input {
  margin-bottom: 1rem;
  padding: 0.75rem;
  font-size: 1rem;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 6px;
  transition: border-color 0.3s;
}

.input-error {
  border-color: red !important;
}

.login-btn {
  background-color: #6c63ff;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1rem;
  cursor: pointer;
  width: 100%;
}

.signup-link {
  margin-top: 1rem;
  font-size: 0.9rem;
}

.error-message {
  color: red;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
</style>
