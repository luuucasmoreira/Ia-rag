# Ambiente RAG com Ollama + 
    depends_on:
      - ollama
      - postgres
    ports:
      - "8000:8000"
```

---

API

api/Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

api/requirements.txt

fastapi
uvicorn
psycopg2-binary
sqlalchemy
langchain
requests

api/app.py

from fastapi import FastAPI
import requests
from sqlalchemy import create_engine, text

app = FastAPI()

DB_URL = "postgresql://rag_user:rag_pass@postgres:5432/ragdb"
engine = create_engine(DB_URL)

OLLAMA_URL = "http://ollama:11434/api/generate"

@app.get("/ask")
def ask(q: str):
    # Busca documentos mais próximos (mockado simplificado)
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT content FROM documents LIMIT 1")).fetchall()
        context = rows[0][0] if rows else "Nada no contexto"

    prompt = f"Contexto: {context}\nPergunta: {q}"

    r = requests.post(OLLAMA_URL, json={"model": "mistral", "prompt": prompt}, stream=True)
    response = ""
    for chunk in r.iter_lines():
        if chunk:
            response += chunk.decode() + "\n"

    return {"answer": response}


---

Como Rodar

1. Clonar repositório

git clone https://github.com/seuusuario/seurepo.git
cd seurepo


2. Subir containers

docker-compose up -d


3. Baixar modelos no Ollama

docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull codellama
docker exec -it ollama ollama pull starcoder


4. Testar API

curl "http://localhost:8000/ask?q=como criar um dockerfile?"




---

Modelos recomendados (gratuitos)

CodeLlama → ótimo para programação.

Mistral 7B → rápido e generalista.

StarCoder / DeepSeek-Coder → especializados em código.

Llama 3 Instruct → generalista, mas bom para devs.



---

Próximos Passos

Implementar /ingest para adicionar textos/documentos ao banco com embeddings.

Usar pgvector de verdade na busca vetorial (em vez de mock).

Integrar com n8n para orquestração de fluxos automáticos.

Criar pipelines de avaliação para “treinar” o fluxo de RAG.



---

Licença

MIT

---

Quer que eu já adicione no README a **rota `/ingest`** pronta, com geração de embeddings no Postgres via `langchain`?

