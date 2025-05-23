FROM python:3.10-slim

# Criar usuário não-root
RUN useradd -m dimdimuser

# Definir diretório de trabalho
WORKDIR /home/dimdimuser/app

# Copiar a aplicação
COPY app/ .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir variáveis apenas genéricas (sem segredo)
ENV DB_HOST=db
ENV DB_PORT=5432
ENV POSTGRES_DB=dimdimdb
ENV POSTGRES_USER=admin

# Trocar para usuário não-root
USER dimdimuser

# Rodar aplicação
CMD ["python", "main.py"]
