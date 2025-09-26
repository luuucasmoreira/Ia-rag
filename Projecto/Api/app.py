from fastapi import FastAPI
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import os
import json
import time
from functools import lru_cache

app = FastAPI()

DB_URL = os.getenv("DB_URL", "postgresql://rag_user:SENSITIVE_PASSWORD_HERE@postgres:5432/ragdb")

# Pool de conexões otimizado
engine = create_engine(
    DB_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")  # MODELO ULTRA RÁPIDO

from pydantic import BaseModel
from typing import Optional, Dict, Any

class IngestRequest(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.on_event("startup")
def startup():
    """Garante a extensão e tabela necessárias."""
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.execute(text(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    metadata JSONB,
                    embedding vector(384)
                )
                """
            ))
            conn.commit()
    except Exception as e:
        # Log simples em stdout
        print(f"Erro no startup: {e}")

@app.post("/ingest")
def ingest(request: IngestRequest):
    try:
        with engine.connect() as conn:
            # Inserir o documento na tabela
            metadata_json = json.dumps(request.metadata) if request.metadata else '{}'
            result = conn.execute(
                text("INSERT INTO documents (content, metadata) VALUES (:content, :metadata::jsonb) RETURNING id"),
                {"content": request.text, "metadata": metadata_json}
            )
            conn.commit()
            doc_id = result.scalar_one()
            return {"message": "Documento inserido com sucesso", "id": doc_id}
    except Exception as e:
        return {"error": f"Erro ao inserir documento: {str(e)}"}

def get_context_optimized(query: str):
    """Busca contexto de forma otimizada"""
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS documents (id SERIAL PRIMARY KEY, content TEXT, metadata JSONB, embedding vector(384))"))
            conn.commit()
            rows = conn.execute(text("SELECT content FROM documents ORDER BY id DESC LIMIT 3")).fetchall()
            return [row[0] for row in rows]
    except Exception as e:
        print(f"Erro ao buscar contexto: {e}")
        return []

@app.get("/ask") 
def ask(q: str):
    start_time = time.time()
    
    # APPROACH DRASTICAMENTE DIFERENTE - SIMPLIFICADO MÁXIMO
    try:
        # Requisição MEGA OTIMIZADA com modelo menor
        payload = {
            "model": OLLAMA_MODEL, 
            "prompt": f"Questão: {q}\nResposta:",
            "stream": False,  # IMPORTANTE: sem stream para resposta instantânea
            "options": {
                "temperature": 0.1,    # ULTRA BAIXA criatividade = máxima velocidade
                "top_p": 0.1,         # DIVERSIDADE MÍNIMA = resposta imediata
                "num_predict": 100,   # APENAS 100 tokens = resposta ultrarrápida
                "num_ctx": 256,       # CONTEXTO MÍNIMO = processamento instantâneo
                "repeat_penalty": 1.0,
                "stop": ["\n\n"]
            }
        }
        
        r = requests.post(OLLAMA_URL, json=payload, timeout=10)  # TIMEOUT ULTRA BAIXO
        
        if r.status_code == 200:
            data = r.json()
            response = data.get("response", "Sem resposta").strip()
            processing_time = time.time() - start_time
            
            return {
                "answer": response[:500],  # Resposta limitada ao essencial
                "processing_time": round(processing_time, 2),
                "model": OLLAMA_MODEL,
                "status": "ultra_fast" if processing_time < 5 else "fast"
            }
        else:
            return {"error": f"Status HTTP: {r.status_code}", "processing_time": round(time.time() - start_time, 2)}
            
    except requests.Timeout:
        return {"error": "Timeout - muito lento", "processing_time": round(time.time() - start_time, 2)}
    except Exception as e:
        return {"error": f"Erro: {str(e)}", "processing_time": round(time.time() - start_time, 2)}