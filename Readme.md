# Projeto: Ambiente RAG Local com Ollama + Postgres (pgvector) + FastAPI

Este projeto cria um **ambiente local em Docker** para testar **RAG (Retrieval-Augmented Generation)** utilizando:

- **Ollama** → roda modelos LLM open-source (Mistral, CodeLlama, StarCoder etc.).
- **Postgres com pgvector** → banco de dados vetorial para armazenar embeddings.
- **API em FastAPI** → ponto de entrada para indexar (`/ingest`) e consultar (`/ask`) documentos.

O objetivo é fornecer uma base prática para desenvolvedores que desejam treinar e testar um fluxo de IA com foco em **programação**.

---

## Arquitetura

- **Ollama**: responsável por carregar e executar modelos de linguagem localmente.
- **Postgres + pgvector**: armazena embeddings vetoriais dos documentos indexados.
- **API RAG (FastAPI)**: cria embeddings, salva no banco e realiza consultas usando similaridade antes de chamar o Ollama.

Fluxo simplificado:

1. O usuário envia documentos via `/ingest`.
2. O texto é convertido em embeddings e armazenado no banco.
3. O usuário faz uma pergunta em `/ask`.
4. A API busca documentos mais relevantes no banco.
5. A API monta um prompt com contexto e chama o Ollama para gerar a resposta.

---

## Estrutura de Pastas

```
project/
 ├─ docker-compose.yml     # Orquestra containers
 ├─ ollama/                # Persistência dos modelos do Ollama
 ├─ pgdata/                # Dados persistidos do Postgres
 └─ api/                   # API FastAPI para ingestão e consulta
     ├─ Dockerfile
     ├─ requirements.txt
     └─ app.py
```

---

## Componentes do Projeto

### 1. **docker-compose.yml**

Define três serviços:

- **ollama**: expõe a API do Ollama na porta `11434`.
- **postgres**: banco Postgres com extensão pgvector habilitada.
- **api**: serviço FastAPI que conecta Ollama e Postgres.

### 2. **API FastAPI**

Endpoints principais:

- `POST /ingest` → recebe texto + metadados, gera embeddings e armazena no banco.
- `GET /ask` → recebe pergunta, busca contexto no banco e consulta o Ollama.
- `GET /health` → retorna status simples do serviço.

### 3. **Dependências**

- **FastAPI / Uvicorn** → framework web da API.
- **psycopg2 + pgvector** → comunicação com Postgres + suporte vetorial.
- **sentence-transformers** → geração de embeddings.
- **requests** → integração com a API do Ollama.

---

## Modelos recomendados

Os seguintes modelos gratuitos funcionam bem para programação:

- **CodeLlama** → especializado em código.
- **Mistral 7B** → rápido e eficiente.
- **StarCoder / DeepSeek-Coder** → focados em geração de código.
- **Llama 3 Instruct** → mais generalista, mas útil para programação.

Para baixar modelos dentro do container do Ollama:

```bash
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull codellama
docker exec -it ollama ollama pull starcoder
```

---

## Como rodar

1. **Clonar repositório**

   ```bash
   git clone https://github.com/seuusuario/seurepo.git
   cd seurepo
   ```

2. **Subir containers**

   ```bash
   docker-compose up -d --build
   ```

3. **Verificar status**

   ```bash
   docker-compose logs -f api
   ```

4. **Testar ingestão**

   ```bash
   curl -X POST "http://localhost:8000/ingest" -H "Content-Type: application/json" -d '{"text":"Exemplo de documento para IA de programadores"}'
   ```

5. **Testar consulta**

   ```bash
   curl "http://localhost:8000/ask?q=Como criar um Dockerfile em Python?"
   ```

---

## Próximos passos

- Criar índice vetorial em Postgres para buscas mais rápidas:

  ```sql
  CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists=100);
  ```

- Implementar **chunking** (quebrar textos longos em partes menores).
- Adicionar autenticação na API.
- Integrar com **n8n** para orquestração de fluxos.
- Criar pipeline para ingestão de código, documentações e exemplos técnicos.

---

## Licença

MIT — Livre para uso, modificação e distribuição.
