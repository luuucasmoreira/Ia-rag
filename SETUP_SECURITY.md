# 🔒 Guia de Segurança para Configuração

## ⚠️ INFORMAÇÕES SENSÍVEIS IDENTIFICADAS

Este projeto contém informações sensíveis que devem ser **MASCARADAS** antes de subir para o Git.

### 🔑 Arquivos Sensíveis Encontrados:

1. **`.vscode/settings.json`** 
   - ✅ **Mascarado:** `rag_pass` → `YOUR_PASSWORD_HERE`
   
2. **`Projecto/docker-compose.yaml`**
   - ✅ **Mascarado:** `POSTGRES_PASSWORD` → `SENSITIVE_PASSWORD_PLACEHOLDER`
   - ✅ **Mascarado:** `DB_URL` → `SENSITIVE_PASSWORD_PLACEHOLDER`
   - ✅ **Mascarado:** Keys do WebUI → `YOUR_SECRET_KEY_PLACEHOLDER`

3. **`Projecto/Api/app.py`**
   - ✅ **Mascarado:** Database connection string → `SENSITIVE_PASSWORD_HERE`

## 📁 Arquivos Backup Originais

Os arquivos originais foram salvos em: `../backups_security/`

### Arquivo de Configuração Pessoal 

Para viabilizar sua configuração individual:

1. **Copie este arquivo para variável de ambiente:**
```bash
# No seu terminal, antes de subir os containers:
export POSTGRES_PASSWORD=sua_senha_aqui
export WEBUI_SECRET_KEY=sua_chave_webui_aqui
export WEBUI_JWT_SECRET_KEY=sua_chave_jwt_aqui
```

2. **Ou crie arquivo `.env` (não commitir):**
```env
POSTGRES_PASSWORD=sua_senha_aqui
WEBUI_SECRET_KEY=sua_chave_webui_aqui  
WEBUI_JWT_SECRET_KEY=sua_chave_jwt_aqui
```

## 🚀 Como Usar Depois do Setup:

1. **Configure as variáveis de ambiente**
2. **Rode o Docker:**
   ```bash
   docker-compose up -d
   ```
3. **As senhas do Docker Compose serão obtidas das env vars se disponíveis**

## 🔒 O que foi protegido:

- ✅ Senhas do PostgreSQL  
- ✅ Chaves secretas do WebUI
- ✅ JWT tokens do sistema
- ✅ URLs de conexão com senhas
- ✅ Dados sensíveis do ambiente

Agora seu projeto está **SEGURO** para ser publicado no Git! 🔐
