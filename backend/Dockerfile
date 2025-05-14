# Use imagem base com Python
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Expõe a porta
EXPOSE 8080

# Comando para iniciar o app
CMD ["python", "app.py"]
