# Projeto: Ambiente RAG Local com Ollama + Postgres (pgvector) + FastAPI

Este projeto cria um **ambiente local em Docker** para testar **RAG (Retrieval-Augmented Generation)** utilizando:

- **Ollama** â†’ roda modelos LLM open-source (Mistral, CodeLlama, StarCoder etc.).
- **Postgres com pgvector** â†’ banco de dados vetorial para armazenar embeddings.
- **API em FastAPI** â†’ ponto de entrada para indexar (`/ingest`) e consultar (`/ask`) documentos.

O objetivo Ã© fornecer uma base prÃ¡tica para desenvolvedores que desejam treinar e testar um fluxo de IA com foco em **programaÃ§Ã£o**.

---

## Arquitetura

- **Ollama**: responsÃ¡vel por carregar e executar modelos de linguagem localmente.
- **Postgres + pgvector**: armazena embeddings vetoriais dos documentos indexados.
- **API RAG (FastAPI)**: cria embeddings, salva no banco e realiza consultas usando similaridade antes de chamar o Ollama.

Fluxo simplificado:

1. O usuÃ¡rio envia documentos via `/ingest`.
2. O texto Ã© convertido em embeddings e armazenado no banco.
3. O usuÃ¡rio faz uma pergunta em `/ask`.
4. A API busca documentos mais relevantes no banco.
5. A API monta um prompt com contexto e chama o Ollama para gerar a resposta.

---

## Estrutura de Pastas

```
project/
 â”œâ”€ docker-compose.yml     # Orquestra containers
 â”œâ”€ ollama/                # PersistÃªncia dos modelos do Ollama
 â”œâ”€ pgdata/                # Dados persistidos do Postgres
 â””â”€ api/                   # API FastAPI para ingestÃ£o e consulta
     â”œâ”€ Dockerfile
     â”œâ”€ requirements.txt
     â””â”€ app.py
```

---

## Componentes do Projeto

### 1. **docker-compose.yml**
Define trÃªs serviÃ§os:
- **ollama**: expÃµe a API do Ollama na porta `11434`.
- **postgres**: banco Postgres com extensÃ£o pgvector habilitada.
- **api**: serviÃ§o FastAPI que conecta Ollama e Postgres.

### 2. **API FastAPI**
Endpoints principais:
- `POST /ingest` â†’ recebe texto + metadados, gera embeddings e armazena no banco.
- `GET /ask` â†’ recebe pergunta, busca contexto no banco e consulta o Ollama.
- `GET /health` â†’ retorna status simples do serviÃ§o.

### 3. **DependÃªncias**
- **FastAPI / Uvicorn** â†’ framework web da API.
- **psycopg2 + pgvector** â†’ comunicaÃ§Ã£o com Postgres + suporte vetorial.
- **sentence-transformers** â†’ geraÃ§Ã£o de embeddings.
- **requests** â†’ integraÃ§Ã£o com a API do Ollama.

---

## Modelos recomendados

Os seguintes modelos gratuitos funcionam bem para programaÃ§Ã£o:

- **CodeLlama** â†’ especializado em cÃ³digo.
- **Mistral 7B** â†’ rÃ¡pido e eficiente.
- **StarCoder / DeepSeek-Coder** â†’ focados em geraÃ§Ã£o de cÃ³digo.
- **Llama 3 Instruct** â†’ mais generalista, mas Ãºtil para programaÃ§Ã£o.

Para baixar modelos dentro do container do Ollama:
```bash
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull codellama
docker exec -it ollama ollama pull starcoder
```

---

## Como rodar

1. **Clonar repositÃ³rio**
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

4. **Testar ingestÃ£o**
   ```bash
   curl -X POST "http://localhost:8000/ingest" -H "Content-Type: application/json"      -d '{"text":"Exemplo de documento para IA de programadores"}'
   ```

5. **Testar consulta**
   ```bash
   curl "http://localhost:8000/ask?q=Como criar um Dockerfile em Python?"
   ```

---

## PrÃ³ximos passos

- Criar Ã­ndice vetorial em Postgres para buscas mais rÃ¡pidas:
  ```sql
  CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists=100);
  ```
- Implementar **chunking** (quebrar textos longos em partes menores).
- Adicionar autenticaÃ§Ã£o na API.
- Integrar com **n8n** para orquestraÃ§Ã£o de fluxos.
- Criar pipeline para ingestÃ£o de cÃ³digo, documentaÃ§Ãµes e exemplos tÃ©cnicos.

---

## LicenÃ§a
MIT â€” Livre para uso, modificaÃ§Ã£o e distribuiÃ§Ã£o.
