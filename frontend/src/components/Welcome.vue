<template>
  <div class="welcome">
    <h2>{{ message }}</h2>

    <!-- Área de texto para inserir o conteúdo a ser resumido -->
    <div style="margin: 2em 0;">
      <textarea v-model="textoParaResumo" placeholder="Cole seu texto aqui para resumir..." rows="6"
        style="width: 100%; padding: 0.5em;"></textarea>
    </div>

    <div style="margin: 1em 0;">
      <label for="arquivo">Ou envie um arquivo:</label>
      <input type="file" @change="handleArquivo" accept=".txt,.pdf" />
    </div>

    <div style="margin: 1em 0;">
      <label for="tipoResumo">Tipo de resumo:</label>
      <select v-model="tipoResumo" id="tipoResumo" style="margin-left: 1em;">
        <option value="pequeno">Pequeno</option>
        <option value="medio">Médio</option>
        <option value="topicos">Em tópicos</option>
      </select>
    </div>

    <button @click="resumirTexto" :disabled="carregando" style="padding: 0.5em 1em;">
      {{ carregando ? 'Resumindo...' : 'Resumir' }}
    </button>

    <div v-if="resumo" style="margin-top: 2em; padding: 1em; border: 1px solid #ccc; background: #f9f9f9;">
      <h3>Resumo:</h3>
      <div v-html="resumo" style="text-align: left;"></div>
      <button @click="mostrarResumoCompleto = !mostrarResumoCompleto">
        {{ mostrarResumoCompleto ? 'Colapsar' : 'Expandir' }}
      </button>

      <div style="margin-top: 1em;">
        <label for="formatoExportacao">Exportar como:</label>
        <select v-model="formatoExportacao" id="formatoExportacao" style="margin: 0 1em;">
          <option value="txt">TXT</option>
          <option value="pdf">PDF</option>
        </select>
        <button @click="exportarResumo">Exportar Resumo</button>
      </div>
    </div>

    <button @click="logout" style="margin-top: 2em; padding: 0.5em 1em;">
      Sair
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import { marked } from 'marked';
import { jsPDF } from 'jspdf';

export default {
  name: 'WelcomePage',
  data() {
    return {
      message: '',
      textoParaResumo: '',
      resumo: '',
      carregando: false,
      tipoResumo: 'medio',
      arquivoSelecionado: null,
      mostrarResumoCompleto: false,
      formatoExportacao: 'txt',
    };
  },
  created() {
    const token = localStorage.getItem('access_token');
    axios.get('http://127.0.0.1:5000/welcome', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
      .then(response => {
        this.message = response.data.message;
      })
      .catch(() => {
        alert('Você precisa fazer login.');
        this.$router.push('/login');
      });
  },
  methods: {
    handleArquivo(event) {
      this.arquivoSelecionado = event.target.files[0];
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/login');
    },
    exportarResumo() {
      const textoPlano = this.removerTagsHtml(this.resumo);
      if (this.formatoExportacao === 'txt') {
        const blob = new Blob([textoPlano], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'resumo.txt';
        a.click();
        URL.revokeObjectURL(url);
      } else if (this.formatoExportacao === 'pdf') {
        const doc = new jsPDF();
        const linhas = doc.splitTextToSize(textoPlano, 180);
        doc.text(linhas, 10, 10);
        doc.save('resumo.pdf');
      }
    },
    resumirTexto() {
      if (!this.textoParaResumo.trim() && this.arquivoSelecionado == null) {
        alert('Por favor, insira um texto para resumir ou selecione um arquivo de texto para leitura.');
        return;
      }

      this.carregando = true;
      this.resumo = '';

      const formData = new FormData();
      formData.append('file', this.arquivoSelecionado);
      formData.append('text', this.textoParaResumo);
      formData.append('summaryType', this.tipoResumo);

      axios.post('http://127.0.0.1:5000/summary',
        formData,
        {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        }
      )
        .then(res => {
          this.resumo = marked(res.data.summary);
        })
        .catch((error) => {
          alert(`Erro ao gerar o resumo.\n${error}`);
        })
        .finally(() => {
          this.carregando = false;
        });
    },
    removerTagsHtml(html) {
      const div = document.createElement('div');
      div.innerHTML = html;
      return div.textContent || div.innerText || '';
    }
  }
};
</script>

<style scoped></style>