# RT-01/04: imagem Python mínima para a aplicação.
FROM python:3.12-slim
# Diretório interno para o código.
WORKDIR /code
# Evitar bytecode e atrasos nos logs.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
# RT-08: copiar dependências primeiro aproveita a cache de construção.
COPY requirements.txt .
# Instalar as versões fixadas sem guardar cache pip.
RUN pip install --no-cache-dir -r requirements.txt
# Copiar apenas a aplicação; testes não são necessários no contentor.
COPY app/ ./app/
# Porta HTTP interna, distinta da porta publicada no host.
EXPOSE 8000
# RT-02/09: iniciar FastAPI com Uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
