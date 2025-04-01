FROM python:3.9-slim

WORKDIR /app

# Copie e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do projeto
COPY . .

# Exponha a porta da API
EXPOSE 5000

# Comando para iniciar a API e o worker do Celery
# Neste exemplo, usamos um comando shell para iniciar os dois processos em background.
CMD sh -c "celery -A tasks worker --loglevel=info & python api.py"

