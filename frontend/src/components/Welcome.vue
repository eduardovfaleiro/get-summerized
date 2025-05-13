<template>
  <v-container fluid class="fill-height pa-0">
      <v-col cols="12" class="p-0">
        <!-- Summarizer Panels -->
        <v-row dense no-gutters>
          <v-col cols="6">
            <v-card outlined class="px-4 pt-2 no-bottom-border no-top-right-radius">
              <v-row align="center" style="height: 100px">
                <v-col cols="6">
                  <v-btn @click="triggerFileInput" color="primary" text>
                    <v-icon left>mdi-upload</v-icon>
                    Importar arquivo
                  </v-btn>
                  <input
                    ref="uploader"
                    type="file"
                    @change="uploadFile"
                    class="d-none"
                  />
                </v-col>
                <v-col cols="6">
                  <div class="text-caption">Tipo de resumo</div>
                  <v-chip-group
                    v-model="summaryType"
                    row
                    active-class="primary--text"
                    mandatory
                  >
                    <v-chip
                      v-for="opt in summaryOptions"
                      :key="opt.value"
                      :value="opt.value"
                      outlined
                    >
                      {{ opt.text }}
                    </v-chip>
                  </v-chip-group>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card outlined class="px-4 pt-2 no-bottom-border no-top-left-border">
              <v-row align="center" style="height: 100px">
                <v-btn @click="downloadSummaryPdf" color="primary" text>
                  <v-icon left>mdi-download</v-icon>
                  Baixar como PDF
                </v-btn>
                <v-btn @click="downloadSummaryTxt" color="primary" text>
                  <v-icon left>mdi-download</v-icon>
                  Baixar como TXT
                </v-btn>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
        <v-card outlined class="pa-4 no-top-radius">
          <v-row dense>
            <!-- Input Panel -->
            <v-col cols="12" md="6">
              <v-textarea
                v-model="textToSummarize"
                placeholder="Digite ou cole seu texto aqui..."
                rows="12"
                outlined
                no-resize
              />
              <v-row dense class="justify-end">
                <v-col cols="6">
                  <v-btn block outlined color="orange" @click="pasteFromClipboard">
                    <v-icon left>mdi-clipboard-text</v-icon> Colar
                  </v-btn>
                </v-col>
                <v-col cols="6">
                  <v-btn block outlined color="red" @click="clearInput">
                    <v-icon left>mdi-trash-can</v-icon> Limpar
                  </v-btn>
                </v-col>
              </v-row>
              <v-btn
                class="mt-4"
                block
                color="orange darken-2"
                :loading="loading"
                @click="summarizeText"
              >
                {{ loading ? 'Resumindo...' : 'Resumir' }}
              </v-btn>
            </v-col>

            <!-- Output Panel -->
            <v-col cols="12" md="6" outine>
              <v-sheet
                outlined
                rounded
                style="height: 346px; overflow-y: auto; padding: 8px;"
              >
                <div v-html="summary"></div>
              </v-sheet>
              <v-row dense class="justify-end mt-5">
                <v-col cols="6">
                  <v-btn block outlined color="orange" @click="copySummary">
                    <v-icon left>mdi-clipboard-text</v-icon>
                    <transition name="fade">
                      <span :key="copied">{{ copied ? 'Copiado!' : 'Copiar' }}</span>
                    </transition>
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
  </v-container>
</template>


<script>
import axios from 'axios'
import { marked } from 'marked'
import { jsPDF } from 'jspdf'
import { auth } from '@/auth'

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
      exportExtension: 'txt',
      summaryOptions: [
        { text: 'Pequeno',  value: 'short'   },
        { text: 'Médio',    value: 'regular' },
        { text: 'Tópicos',  value: 'topics'  }
      ],
      copied: false,
    }
  },
  created() {
    // const token = localStorage.getItem('access_token')
    const token = auth.token;
    axios
      .get('http://127.0.0.1:5000/welcome', {
        headers: { Authorization: 'Bearer ' + token },
      })
      .then(res => {
        this.message = res.data.message
      })
      .catch(() => {
        this.$router.push('/login')
      })
  },
  methods: {
    triggerFileInput() {
      this.$refs.uploader.click(); // Simula o clique no input de arquivo
    },
    clearInput() {
      this.textToSummarize = ''
      this.file = null
    },
    pasteFromClipboard() {
      navigator.clipboard.readText().then(txt => {
        this.textToSummarize = txt
      })
    },
    copySummary() {
      if (!this.summary) return;
      
      // extrai só o texto puro (sem tags) do summary
      const text = this.summary.replace(/<[^>]+>/g, '\n').trim();
      navigator.clipboard.writeText(text)
        .then(() => {
          this.copied = true;
          // volta ao normal após 1.5s
          setTimeout(() => this.copied = false, 1500);
        })
        .catch(() => {
          // se falhar, você pode manter copiado=false ou mostrar erro
          this.copied = false;
        });
    },
    async uploadFile(e) {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:5000/extract-text', {
        method: 'POST',
        headers: {
          // Authorization: 'Bearer ' + localStorage.getItem('access_token'), // use seu token JWT
          Authorization: 'Bearer ' + auth.token, // use seu token JWT
        },
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        this.textToSummarize = data.text; // preencher seu v-model do textarea
      } else {
        alert('Erro ao extrair texto: ' + data.message);
      }
    },
    summarizeText() {
      if (!this.textToSummarize.trim() && !this.file) {
        return this.$toast.error('Insira texto ou selecione um arquivo.')
      }
      this.loading = true
      this.summary = ''

      const form = new FormData()
      form.append('file', this.file)
      form.append('text', this.textToSummarize)
      form.append('summaryType', this.summaryType)

      axios
        .post('http://127.0.0.1:5000/summary', form, {
          // headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          headers: { Authorization: 'Bearer ' + auth.token }
        })
        .then(res => {
          this.summary = marked(res.data.summary)
        })
        .catch(() => {
          this.$toast.error('Erro ao gerar o resumo.')
        })
        .finally(() => {
          this.loading = false
        })
    },
    downloadSummaryPdf() {
      const text = this.summary.replace(/<[^>]+>/g, '\n')
      const doc = new jsPDF()
      const lines = doc.splitTextToSize(text, 180)
      doc.text(lines, 10, 10)
      doc.save('resumo.pdf')
    },
    downloadSummaryTxt() {
      const text = this.summary.replace(/<[^>]+>/g, '\n')
      const blob = new Blob([text], { type: 'text/plain' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = 'resumo.txt'
      link.click()
      URL.revokeObjectURL(link.href)
    },
  },
}
</script>

<style scoped>
.no-top-right-radius {
  border-top-right-radius: 0 !important;
}

.no-top-left-border {
  border-top-left-radius: 0 !important;
  border-left: none;
}

.no-bottom-border {
  border-bottom: none;
}

.no-top-radius {
  border-top-left-radius: 0 !important;
  border-top-right-radius: 0 !important;
}
</style>
