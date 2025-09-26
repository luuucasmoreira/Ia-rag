# 🚀 Otimizações de Performance do Docker

## 📊 Configurações Aplicadas

### 🎯 Distribuição de Recursos (24GB RAM + Ryzen 5 3600 + GTX 1660)

| Serviço | RAM | CPU | Observações |
|---------|-----|-----|-------------|
| **Ollama** | 12GB | 6 cores | GPU habilitada, processamento paralelo |
| **PostgreSQL** | 4GB | 4 cores | Otimizado para vetores e RAG |
| **API RAG** | 2GB | 2 cores | Processamento de embeddings |
| **Open WebUI** | 2GB | 2 cores | Interface otimizada |
| **Sistema** | 4GB | - | Reservado para SO e Docker |

### 🔧 Configurações do Docker Desktop

Acesse: **Docker Desktop > Settings > Resources > Advanced**

```
Memória: 18GB (75% da RAM total)
CPUs: 7 cores (87.5% dos 8 cores)
Swap: 2GB
Disk image size: 100GB
```

### ⚡ Otimizações Implementadas

#### 🧠 Ollama (IA)
- ✅ GPU NVIDIA habilitada
- ✅ 2 requests paralelos
- ✅ 2 modelos carregados simultaneamente
- ✅ Fila de 512 requests
- ✅ 12GB RAM dedicada

#### 🗄️ PostgreSQL (Banco)
- ✅ shared_buffers: 2GB
- ✅ effective_cache_size: 6GB
- ✅ 8 workers paralelos
- ✅ Otimizado para pgvector
- ✅ WAL otimizado

#### 🌐 Rede
- ✅ Rede customizada para comunicação interna
- ✅ MTU otimizado (1500)
- ✅ Comunicação inter-container otimizada

## 🚀 Como Aplicar

### 1. Parar containers atuais
```bash
docker-compose down
```

### 2. Configurar Docker Desktop
- Abra Docker Desktop
- Vá em Settings > Resources > Advanced
- Configure conforme especificado acima
- Clique em "Apply & Restart"

### 3. Reiniciar com otimizações
```bash
docker-compose up -d
```

### 4. Verificar performance
```bash
# Monitorar recursos
docker stats

# Verificar GPU do Ollama
docker exec ollama ollama list
```

## 📈 Melhorias Esperadas

- ⚡ **Resposta 3-5x mais rápida** do Ollama
- 🚀 **Processamento paralelo** de requests
- 💾 **Cache otimizado** no PostgreSQL
- 🎯 **GPU dedicada** para inferência
- 🔄 **Menos latência** entre serviços

## 🔍 Monitoramento

### Comandos úteis:
```bash
# Status dos containers
docker-compose ps

# Uso de recursos em tempo real
docker stats

# Logs do Ollama
docker logs ollama -f

# Verificar modelos carregados
docker exec ollama ollama ps
```

## ⚠️ Troubleshooting

### Se a GPU não for detectada:
1. Instale NVIDIA Container Toolkit
2. Reinicie o Docker Desktop
3. Verifique: `docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi`

### Se houver erro de memória:
1. Reduza `OLLAMA_MAX_LOADED_MODELS` para 1
2. Diminua `shared_buffers` do PostgreSQL
3. Ajuste limites no Docker Desktop

### Para melhor performance ainda:
1. Use modelos menores (7B ao invés de 13B+)
2. Configure `OLLAMA_NUM_PARALLEL=1` se houver instabilidade
3. Monitore uso com `docker stats`

