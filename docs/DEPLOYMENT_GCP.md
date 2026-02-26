# Guia de Deploy no Google Cloud Platform (Plano Pro)

Este documento descreve como migrar o ambiente local (Docker Compose) para a infraestrutura gerenciada do **Google Cloud Platform (GCP)**.

## 1. Arquitetura na Nuvem
- **Banco de Dados:** Cloud SQL for PostgreSQL
- **Backend (FastAPI):** Cloud Run (Serverless Container)
- **Frontend (React):** Cloud Run ou Firebase Hosting
- **IA Generativa:** Vertex AI / Gemini API via Google AI Studio

---

## 2. Setup do Cloud SQL (PostgreSQL)
Ao invés de rodar o Postgres num container local, usaremos a versão gerenciada:

1. Acesse o console do GCP: `Vá em SQL > Criar Instância > PostgreSQL`
2. Configure a senha do usuário `postgres` (ex: `cancermama_cloud_2026`)
3. Crie um banco de dados chamado `breast_cancer`
4. Na aba **Conexões**, adicione sua rede/IP ou configure IP Privado para que o Cloud Run acesse o banco internamente.

---

## 3. Deploy do Backend no Cloud Run
O Cloud Run permite rodar containers de forma escalável, pagando apenas pelas requisições processadas.

### 3.1. Preparar a Imagem Docker
```bash
# Autenticar no Google Cloud via CLI
gcloud auth login
gcloud config set project [SEU_PROJECT_ID]

# Construir e enviar a imagem para o Artifact Registry
gcloud builds submit --tag gcr.io/[SEU_PROJECT_ID]/cancermama-backend ./backend
```

### 3.2. Criar o Serviço no Cloud Run
1. Vá em **Cloud Run** > **Criar Serviço**
2. Selecione a imagem: `gcr.io/[SEU_PROJECT_ID]/cancermama-backend`
3. Habilite **"Permitir invocações não autenticadas"** (pois é uma API pública/frontend).
4. Em **Variáveis de Ambiente**, adicione:
   - `DATABASE_URL`: `postgresql://postgres:cancermama_cloud_2026@[IP_DO_CLOUDSQL]:5432/breast_cancer`
   - `GEMINI_API_KEY`: `Sua-chave-da-api-gerada-no-google-ai-studio`
   - `ENVIRONMENT`: `production`

---

## 4. Deploy do Frontend

Como o frontend é em React/Vite (SPA), temos duas opções no GCP:

### Opção A: Firebase Hosting (Recomendado para SPA)
```bash
cd frontend
npm run build
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```
*Não se esqueça de alterar a `baseURL` no arquivo `src/services/api.ts` para a URL pública gerada pelo Cloud Run do backend antes de rodar o build.*

### Opção B: Cloud Run (Servindo com NGINX)
Você precisará criar um `Dockerfile` no frontend usando a imagem do NGINX para servir a pasta `dist` gerada pelo `npm run build`, e usar os mesmos comandos de submit/deploy do Backend.

---

## 5. Próximos Passos
Após essas configurações, a aplicação CancerMama estará online, altamente escalável e usando os recursos nativos do Google Cloud de forma conectada ao Gemini!
