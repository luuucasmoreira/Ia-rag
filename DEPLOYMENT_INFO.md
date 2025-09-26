# 🚀 Guia de Deploy Depois do Clone

Após fazer `git clone` este projeto, você precisará **restaurar as credenciais sensíveis** que foram mascaradas por segurança.

## 🔧 Passos do Primeiro Setup:

### 1️⃣ **Configurar as credenciais reais:**

Edite o arquivo principal `Projecto/docker-compose.yaml` e substitua os placeholders:

```bash
# Procurar e substituir:
# SENSITIVE_PASSWORD_PLACEHOLDER ⟶ sua_senha_postgres_aqui
# YOUR_SECRET_KEY_PLACEHOLDER ⟶ sua_chave_secreta_webui
# YOUR_JWT_SECRET_PLACEHOLDER ⟶ sua_jwt_key_aqui
```

**Arquivos que precisam de ajuste:**
- ✅ `Projecto/docker-compose.yaml` - linhas ~61, ~112, ~154-155
- ✅ `Projecto/Api/app.py` - linha ~12 (DB connection)

### 2️⃣ **Execução segura:**

```bash
# 1. Configure as variáveis de ambiente 
export POSTGRES_PASSWORD=sua_senha_real
export WEBUI_SECRET_KEY=sua_chave_webui  
export WEBUI_JWT_SECRET_KEY=sua_jwt_real

# 2. Suba os containers
docker-compose up -d --build

# 3. Verifique status
docker-compose ps
```

### 3️⃣ **Acessos finais:**

- 🌐 **Open WebUI:** http://localhost:3000
- ⚡ **API Diret:** http://localhost:8000/health

---

## 🔒 **Arquivos de Origem Backup:**

As configurações originais sensíveis foram salvas em: `backups_security/`  
❌ **Não commite estes backups no Git** (já protegidos no .gitignore)

---

## ✅ **Verificação de Segurança:**

∎ Configurei `postsgres_password` work‏ releمـ  
❌ Removeu creds hardcoded  
∎ Set placeholders‎ secure  
∎ Build backup inогаك­ بلальный жеْاليйه| Safe to Git! 🚀🤝👀
