<template>
  <div>
    <v-container fluid class="fill-height pa-0">
        <v-col cols="12" class="p-0">
          <v-card outlined class="pa-2 no-top-radius">
            <v-row dense>
              <v-col cols="12" md="6" class="pr-2">
                <v-textarea
                  v-model="textToSummarize"
                  placeholder="Digite ou cole seu texto aqui..."
                  rows="10"
                  outlined
                  no-resize
                  :maxlength="maxLength"
                  :rules="[v => v.length <= maxLength || `Máximo de ${maxLength} caracteres`]"
                />
                <v-row align="center" class="ml-2 mt-2 mb-1">
                  <div class="text-caption mr-4">Tipo de resumo</div>
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
                </v-row>
                <v-row dense>
                  <v-col cols="12" lg="4">
                    <v-btn block outlined color="red" @click="clearInput">
                      <v-icon left>mdi-trash-can</v-icon> Limpar
                    </v-btn>
                  </v-col>
                  <v-col cols="12" lg="4">
                    <v-btn @click="triggerFileInput" color="primary" block outlined >
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
                  <v-col cols="12" lg="4">
                    <v-btn block outlined color="orange" @click="pasteFromClipboard">
                      <v-icon left>mdi-clipboard-text</v-icon> Colar
                    </v-btn>
                  </v-col>
                </v-row>
                <v-btn
                  block
                  color="orange darken-2"
                  :disabled="isSubmitDisabled"
                  :loading="loading"
                  @click="summarizeText"
                  class="my-2"
                >
                  {{ loading ? 'Resumindo...' : 'Resumir' }}
                </v-btn>
              </v-col>

              <v-divider vertical></v-divider>

              <v-col cols="12" md="6" class="pl-2">
                <v-sheet
                  outlined
                  rounded
                  style="height: 290px; overflow-y: auto; padding: 8px;"
                >
                  <div v-html="summary"></div>
                </v-sheet>
                <v-btn block text @click="toggleFullScreen" class="my-3">
                  <v-icon left>mdi-fullscreen</v-icon>
                  Exibir em tela cheia
                </v-btn>
                <v-row dense class="justify-end mt-2">
                  <v-col cols="12" lg="4">
                    <v-btn @click="downloadSummaryPdf" color="primary" block outlined>
                      <v-icon left>mdi-download</v-icon>
                      Baixar como PDF
                    </v-btn>
                  </v-col>
                  <v-col cols="12" lg="4">
                    <v-btn @click="downloadSummaryTxt" color="primary" block outlined>
                      <v-icon left>mdi-download</v-icon>
                      Baixar como TXT
                    </v-btn>
                  </v-col>
                  <v-col cols="12" lg="4">
                    <v-btn block outlined color="orange" @click="copySummary" class="mb-2">
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

    <v-dialog
      v-model="fullScreen"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dense flat>
          <v-btn icon @click="toggleFullScreen">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Resumo</v-toolbar-title>
        </v-toolbar>
        <v-card-text style="overflow-y:auto; height: calc(100vh - 56px);">
          <div v-html="summary"></div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
import axios from 'axios'
import { marked } from 'marked'
import { jsPDF } from 'jspdf'

export default {
  name: 'WelcomePage',
  data() {
    return {
      message: '',
      fullScreen: false,
      textToSummarize: '',
      summary: '',
      loading: false,
      summaryType: 'regular',
      exportExtension: 'txt',
      maxLength: 10,
      summaryOptions: [
        { text: 'Pequeno',  value: 'short'   },
        { text: 'Médio',    value: 'regular' },
        { text: 'Tópicos',  value: 'topics'  }
      ],
      copied: false,
    }
  },
  created() {
    // axios
    //   .get('/api/welcome')
    //   .then(res => {
    //     this.message = res.data.message
    //   })
    //   .catch(() => {
    //     this.$router.push('/login')
    //   })

    axios.get('/api/config').then(res => {
      this.maxLength = res.data.MAX_LENGTH
    })
  },
  computed: {
    isSubmitDisabled() {
      return (
        this.textToSummarize.length === 0 ||
        this.textToSummarize.length > this.maxLength ||
        this.loading
      )
    }
  },
  methods: {
    toggleFullScreen() {
      this.fullScreen = !this.fullScreen
    },
    triggerFileInput() {
      this.$refs.uploader.click(); // Simula o clique no input de arquivo
    },
    clearInput() {
      this.textToSummarize = ''
    },
    pasteFromClipboard() {
      navigator.clipboard.readText().then(txt => {
        this.textToSummarize = txt
      })
    },
    copySummary() {
      if (!this.summary) return;

      // Decodifica entidades HTML
      const temp = document.createElement('div')
      temp.innerHTML = this.summary
      const decodedText = temp.textContent || temp.innerText || ''

      // (Opcional) Remove tags HTML se houver risco de sobrar alguma
      const cleanText = decodedText.replace(/<[^>]+>/g, '').trim()

      navigator.clipboard.writeText(cleanText)
        .then(() => {
          this.copied = true
          setTimeout(() => this.copied = false, 1500)
        })
        .catch(() => {
          this.copied = false
        })
    },
    async uploadFile(e) {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);

      axios
        .post('/api/extract-text', formData)
        .then(res => {
          this.textToSummarize = res.data.text
        })
    },
    summarizeText() {
      if (!this.textToSummarize.trim() && !this.file) {
        return this.$toast.error('Insira texto ou selecione um arquivo.')
      }
      this.loading = true
      this.summary = ''

      const form = new FormData()
      form.append('text', this.textToSummarize)
      form.append('summaryType', this.summaryType)

      axios
        .post('/api/summary', form)
        .then(res => {
          this.summary = marked(res.data.summary)
        }).catch(() => {
          // Deixar assim p/ não exibir erro
        }).finally(() => {
          this.loading = false
        })
    },
    downloadSummaryPdf() {
      // Decodifica as entidades HTML
      const temp = document.createElement('div')
      temp.innerHTML = this.summary
      const decodedText = temp.textContent || temp.innerText || ''

      // Remove tags HTML, se necessário
      const cleanText = decodedText.replace(/<[^>]+>/g, '')

      // Gera o PDF
      const doc = new jsPDF()
      const lines = doc.splitTextToSize(cleanText, 180)
      doc.text(lines, 10, 10)
      doc.save('resumo.pdf')
    },
    downloadSummaryTxt() {
      // Cria um elemento temporário para decodificar HTML
      const temp = document.createElement('div')
      temp.innerHTML = this.summary
      const decodedText = temp.textContent || temp.innerText || ''

      // Remove as tags (se ainda necessário) e salva como texto
      const cleanText = decodedText.replace(/<[^>]+>/g, '\n')
      const blob = new Blob([cleanText], { type: 'text/plain' })
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
