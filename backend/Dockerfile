# Usa uma imagem oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8080 (que o Cloud Run usa)
EXPOSE 8080

# Comando para iniciar o servidor (ajuste se estiver usando Flask/FastAPI/etc.)
CMD ["python", "app.py"]
