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
