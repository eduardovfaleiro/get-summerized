# frontend/Dockerfile

# --- Estágio 1: Build da aplicação Vue ---
FROM node:18-alpine AS build

# Define o diretório de trabalho
WORKDIR /app

# Copia o package.json e package-lock.json para o cache de dependências
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o resto do código fonte
COPY . .

# Compila a aplicação para produção
RUN npm run build

# --- Estágio 2: Servir os arquivos com Nginx ---
FROM nginx:stable-alpine AS production

# Copia os arquivos compilados do estágio de build para a pasta padrão do Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copia uma configuração customizada do Nginx (opcional, mas recomendado)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expõe a porta 80, que é a porta padrão do Nginx
EXPOSE 80

# O comando para iniciar o Nginx já vem na imagem base