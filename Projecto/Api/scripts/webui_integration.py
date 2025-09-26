import requests
import json
import os

def save_to_rag(conversation):
    """
    Salva uma conversa no sistema RAG
    """
    rag_url = "http://localhost:8000/ingest"
    
    # Formata a conversa para armazenamento
    conversation_text = json.dumps(conversation, ensure_ascii=False, indent=2)
    
    payload = {
        "text": conversation_text,
        "metadata": {
            "source": "open-webui",
            "type": "conversation",
            "model": conversation.get("model", "unknown"),
            "timestamp": conversation.get("timestamp", "")
        }
    }
    
    try:
        response = requests.post(rag_url, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao salvar no RAG: {e}")
        return False

def query_rag(question):
    """
    Consulta o sistema RAG para obter contexto relevante
    """
    rag_url = f"http://localhost:8000/ask"
    
    try:
        response = requests.get(rag_url, params={"q": question})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar RAG: {e}")
        return None

# Substitua a senha do Postgres pela variável de ambiente
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Confirmar que estas entradas estão presentes:
# .env
# pgdata/
# webui_data/
# ollama/
# backups_security/
# **/id_ed25519*