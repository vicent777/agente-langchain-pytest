# 1. Escolhe a imagem base (O sistema operacional com Python)
FROM python:3.11-slim

# 2. Define onde as coisas vão acontecer dentro do container
WORKDIR /app

# 3. Copia o arquivo de bibliotecas e instala elas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia todo o seu código (main.py, app.py, etc) para dentro
COPY . .

# 5. Avisa que a API vai rodar na porta 8000
EXPOSE 8000

# 6. O comando que liga a sua API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]