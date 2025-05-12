<template>
  <div class="welcome">
    <h2 class="welcome-title">{{ message }}</h2>

    <div class="summarizer">
      <!-- Left panel -->
      <div class="input-panel">
        <textarea v-model="textToSummarize" placeholder="Digite ou cole seu texto aqui..." rows="6"
          class="text-input"></textarea>

        <div class="actions">
          <button class="paste-btn" @click="pasteFromClipboard">
            <!-- Ícone de prancheta -->
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 3h6a2 2 0 012 2v0a2 2 0 01-2 2H9A2 2 0 017 5V5a2 2 0 012-2z" />
            </svg>
            Colar texto
          </button>

          <label class="upload-label">
            <input type="file" @change="handleFile" accept=".txt,.pdf" hidden />
            <!-- Ícone de upload -->
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1M12 12v6m0-6l-3 3m3-3l3 3M12 3v9" />
            </svg>
            Importar arquivo
          </label>

          <button class="clear-btn" @click="clearInput">
            <!-- Ícone de lixeira -->
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5-4h4a1 1 0 011 1v1H9V4a1 1 0 011-1z" />
            </svg>
            Limpar
          </button>
        </div>

        <button class="summarize-btn" @click="summarizeText" :disabled="loading">
          {{ loading ? 'Resumindo...' : 'Resumir' }}
        </button>
      </div>

      <!-- Right panel -->
      <div class="output-panel">
        <div v-if="summary" class="summary-box">
          <h3>Resumo:</h3>
          <div v-html="summary" class="summary-content"></div>
        </div>
      </div>
    </div>

    <div style="margin: 1em 0;">
      <label for="summaryType">Tipo de resumo:</label>
      <select v-model="summaryType" id="summaryType" style="margin-left: 1em;">
        <option value="short">Pequeno</option>
        <option value="regular">Médio</option>
        <option value="topics">Tópicos</option>
      </select>
    </div>

    <div style="margin-top: 1em;">
      <label for="exportExtension">Exportar como:</label>
      <select v-model="exportExtension" id="exportExtension" style="margin: 0 1em;">
        <option value="txt">TXT</option>
        <option value="pdf">PDF</option>
      </select>
      <button @click="exportSummary">Exportar Resumo</button>
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
      textToSummarize: '',
      summary: '',
      loading: false,
      summaryType: 'regular',
      file: null,
      showFullSummary: false,
      exportExtension: 'txt',
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
    clearInput() {
      this.textToSummarize = '';
      this.file = null;
    },
    pasteFromClipboard() {
      navigator.clipboard.readText().then((text) => {
        this.textToSummarize = text;
      });
    },
    handleFile(event) {
      this.file = event.target.files[0];
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/login');
    },
    exportSummary() {
      const plainText = this.removerTagsHtml(this.summary);
      if (this.exportExtension === 'txt') {
        const blob = new Blob([plainText], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'resumo.txt';
        a.click();
        URL.revokeObjectURL(url);
      } else if (this.exportExtension === 'pdf') {
        const doc = new jsPDF();
        const linhas = doc.splitTextToSize(plainText, 180);
        doc.text(linhas, 10, 10);
        doc.save('resumo.pdf');
      }
    },
    summarizeText() {
      if (!this.textToSummarize.trim() && this.file == null) {
        alert('Por favor, insira um texto para resumir ou selecione um arquivo de texto para leitura.');
        return;
      }

      this.loading = true;
      this.summary = '';

      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('text', this.textToSummarize);
      formData.append('summaryType', this.summaryType);

      axios.post('http://127.0.0.1:5000/summary',
        formData, {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      }
      )
        .then(res => {
          this.summary = marked(res.data.summary);
        })
        .catch((error) => {
          alert(`Erro ao gerar o resumo.\n${error}`);
        })
        .finally(() => {
          this.loading = false;
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

<style scoped>
.welcome-container {
  max-width: 960px;
  margin: 2rem auto;
  font-family: sans-serif;
  display: flex;
  flex-direction: column;
}

.welcome-title {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.75rem;
  color: #2c3e50;
}

.summarizer {
  display: flex;
  gap: 1rem;
}

/* Left panel */
.input-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.text-input {
  flex: 1;
  resize: vertical;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1rem;
  font-family: inherit;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.actions .icon {
  width: 1em;
  height: 1em;
  margin-right: 0.5em;
  vertical-align: middle;
}

/* reaplique os estilos de botão que você já tem */
.paste-btn,
.upload-label,
.clear-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  border: 1px solid;
}

.paste-btn {
  background: white;
  color: #ff964f;
  border-color: #ff964f;
}

.upload-label {
  background: white;
  color: #007bff;
  border-color: #007bff;
}

.clear-btn {
  background: white;
  color: #dc3545;
  border-color: #dc3545;
}

.paste-btn:hover {
  background: #e6f4ea;
}

.upload-label:hover {
  background: #e6f8ff;
}

.clear-btn:hover {
  background: #f8d7da;
}

.summarize-btn {
  padding: 0.75rem;
  background: #ff964f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.summarize-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

/* Right panel */
.output-panel {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fafafa;
  padding: 1rem;
  min-height: 300px;
}

.summary-box h3 {
  margin-top: 0;
  font-size: 1.25rem;
  color: #2c3e50;
}

.summary-content {
  margin-top: 0.5rem;
  line-height: 1.5;
  color: #333;
}

/* Logout */
.logout-btn {
  align-self: center;
  margin-top: 2rem;
  padding: 0.75rem 1.5rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>