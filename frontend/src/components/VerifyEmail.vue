<template>
    <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="6" lg="4">
                <v-card class="pa-6 text-center" outlined>
                    <div v-if="isLoading">
                        <v-progress-circular
                        indeterminate
                        color="orange"
                        size="64"
                        ></v-progress-circular>
                        <h2 class="mt-4 grey--text text--darken-2">Verificando seu e-mail...</h2>
                        <p class="body-1 grey--text">Por favor, aguarde um momento.</p>
                    </div>

                    <div v-else-if="successMessage">
                        <v-icon size="80" color="success">mdi-check-circle-outline</v-icon>
                        <h1 class="mt-4 success--text">E-mail verificado!</h1>
                        <p class="body-1 mt-2">{{ successMessage }}</p>
                        <v-btn
                        color="orange darken-2"
                        class="mt-4"
                        large
                        to="/login"
                        >
                        Ir para o login
                        </v-btn>
                    </div>

                    <div v-else-if="errorMessage">
                        <v-icon size="80" color="error">mdi-alert-circle-outline</v-icon>
                        <h1 class="mt-4 error--text">Ocorreu um erro</h1>
                        <p class="body-1 mt-2">{{ errorMessage }}</p>
                        <v-btn
                        color="grey darken-1"
                        class="mt-4"
                        text
                        to="/register"
                        >
                        Tentar novamente o cadastro
                        </v-btn>
                    </div>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    name: 'VerifyEmailPage',
    data() {
        return {
            isLoading: true,
            successMessage: '',
            errorMessage: '',
        };
    },
    async created() {
        await this.verifyToken();
    },
    methods: {
        async verifyToken() {
            const token = this.$route.query.token

            if (!token) {
                this.isLoading = false
                this.errorMessage = 'Nenhum token de verificação encontrado. O link pode estar quebrado.';
                return;
            }

            try {
                const response = await axios.get(`/api/verify/${token}`);
                
                this.successMessage = response.data.message || 'Seu e-mail foi verificado com sucesso.';
            } catch (error) {
                if (error.response && error.response.data && error.response.data.message) {
                this.errorMessage = error.response.data.message;
                } else {
                this.errorMessage = 'Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.';
                }
            } finally {
                this.isLoading = false;
            }
        }
    }
}
</script>