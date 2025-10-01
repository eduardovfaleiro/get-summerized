# ☀️ GetSummerized

[![Status do Projeto](https://img.shields.io/badge/status-ativo-brightgreen.svg)](https://get-summerized.web.app/)
[![Licença](https://img.shields.io/badge/licença-MIT-blue.svg)](/LICENSE)
[![Vue.js](https://img.shields.io/badge/Vue.js-2.x-green)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)](https://flask.palletsprojects.com/)

Plataforma inteligente para sumarização instantânea de textos e documentos (PDF/TXT), utilizando o poder da API de Inteligência Artificial do Google.

### ✨ **[Acesse a versão live do projeto!](https://get-summerized.web.app/)** ✨

## 🎬 Demonstração

<img src="https://github.com/user-attachments/assets/ec2073cb-98bc-4c20-b9f3-b7ea1f66714f" width="90%" alt="Demonstração do GetSummerized (LOGIN)">
<img width="90%" alt="Demonstração do GetSummerized (TELA INICIAL)" src="https://github.com/user-attachments/assets/94ffe2ee-d5b0-410b-bc43-ed1eef58616b" /> 

## 🎯 Sobre o Projeto

O GetSummerized foi criado para resolver um problema comum: o excesso de informação. Em um mundo onde somos bombardeados por artigos, documentos e relatórios longos, esta ferramenta oferece uma solução rápida e eficiente para extrair as ideias principais de qualquer texto.

Utilizando a API do Google, o GetSummerized processa o conteúdo fornecido pelo usuário e gera resumos coesos em diferentes formatos, otimizando o tempo de estudo e trabalho. O projeto conta com autenticação de usuários para garantir a privacidade dos seus documentos.

## ✨ Funcionalidades Principais

* **✍️ Múltiplos Formatos de Entrada:** Faça upload de arquivos `.pdf` e `.txt` ou simplesmente cole o texto diretamente na plataforma.
* **🧠 Resumos Inteligentes:** Escolha o tipo de resumo que melhor se adapta à sua necessidade:
    * **Tópicos:** Ideal para captar os pontos-chave de forma estruturada.
    * **Curto:** Um parágrafo conciso com a ideia central do texto.
    * **Médio:** Um resumo mais detalhado, mas ainda assim direto.
* **📄 Exportação Fácil:** Baixe os resumos gerados nos formatos `.pdf` ou `.txt` com um único clique.
* **🔐 Autenticação Segura:** Sistema de login e cadastro.
* **📱 Interface Responsiva:** Experiência de uso otimizada para desktops, tablets e smartphones.

## 🛠️ Arquitetura e Tecnologias Utilizadas

Este projeto foi construído com uma arquitetura desacoplada, separando o frontend do backend para maior escalabilidade e manutenção.

```
[Usuário] -> [Frontend (Vue.js no Firebase Hosting)] <-> [API Backend (Flask no Cloud Run)] <-> [Google AI API]
```

#### **Frontend (Vue.js 2)**

* **Vue 2:** Framework progressivo para a construção da interface.
* **Vue Router:** Para gerenciamento das rotas da aplicação.
* **Axios:** Para realizar as chamadas HTTP para o backend.
* **Firebase Hosting:** Para uma hospedagem rápida, segura e com deploy contínuo.

#### **Backend (Python & Flask)**

* **Flask:** Microframework para a criação da API REST.
* **GenAI API:** API utilizada para a inteligência artificial generativa que cria os resumos.
* **PyPDF2:** Biblioteca para extração de texto de arquivos PDF.
* **Cloud Run:** Plataforma serverless do Google Cloud para hospedar o backend, garantindo escalabilidade automática.
* **Docker:** Para containerizar a aplicação backend, garantindo um ambiente de execução consistente do desenvolvimento à produção.
* **Google Secret Manager:** Para armazenamento e gerenciamento seguro de chaves de API e outras variáveis de ambiente sensíveis.
