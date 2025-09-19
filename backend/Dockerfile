FROM python:3.11-slim

# 2. Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copiar o arquivo de dependências e instalar
# Copiamos primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar o restante do código do backend para o diretório de trabalho
COPY . .

# 5. Expor a porta que o Flask vai rodar (geralmente 5000)
EXPOSE 5000

# 6. Comando para rodar a aplicação com Gunicorn (servidor de produção)
# O comando 'app:app' se refere ao arquivo 'app.py' e à instância 'app' do Flask dentro dele.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]