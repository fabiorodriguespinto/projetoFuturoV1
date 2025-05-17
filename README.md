# Projeto_FuturoV1

O **Projeto_FuturoV1** é uma aplicação modular baseada em contêineres Docker, composta por três serviços principais:

- **API (FastAPI)**: expõe uma interface HTTP para inferência de dados.
- **Worker**: agenda tarefas recorrentes para execução e grava dados em um banco local.
- **NN (Neural Network)**: executa inferência com base em um modelo predefinido.

## Arquitetura

Projeto_FuturoV1/
├── api/ → API REST com FastAPI
├── worker/ → Serviço de agendamento e persistência de previsões
├── nn/ → Serviço de rede neural
├── .data/ → Volume persistente compartilhado (banco SQLite)
├── docker-compose.yml → Orquestrador de containers
├── .gitignore → Ignora arquivos que não devem ser versionados
└── README.md → Este arquivo


---

## Serviços

### 🔹 API (FastAPI)
- **Local**: `api/`
- **Imagem**: `projeto_futurov1-api`
- **Porta exposta**: `8000`
- **Endpoints principais**:
  - `GET /healthcheck` → Verifica se a API está ativa
  - `POST /predictions` → Recebe requisições e consulta a NN

### 🔹 Worker (Agendador)
- **Local**: `worker/`
- **Imagem**: `projeto_futurov1-worker`
- **Função**: Roda a cada intervalo (via cron ou APScheduler) e grava previsões em `/data/app.db`

### 🔹 NN (Rede Neural)
- **Local**: `nn/`
- **Imagem**: `projeto_futurov1-nn`
- **Função**: Recebe chamadas da API e retorna previsões simuladas ou reais.

---

## Como executar

### ✅ Pré-requisitos

- Docker
- Docker Compose
- Git

### 🔧 Configuração

Clone o repositório:

```bash
git clone git@github.com:SEU_USUARIO/projetoFuturoV1.git
cd projetoFuturoV1

Construa e suba os serviços:
docker compose up --build -d

Verifique se a API está no ar:
curl http://localhost:8000/healthcheck

Manutenção
📄 Ver logs dos serviços

docker compose logs api
docker compose logs worker
docker compose logs nn

🚫 Parar e remover containers

docker compose down

🔄 Reconstruir todos os serviços
docker compose up --build -d

Volume de Dados

Os serviços compartilham um volume local .data/ onde o banco SQLite app.db é armazenado. Este volume é montado em /data dentro dos containers.
Git & Versionamento

Antes de subir alterações:

git add .
git commit -m "Mensagem clara do que foi alterado"
git push origin main

Certifique-se de que o .gitignore ignora .data/, __pycache__/, arquivos .pyc, etc.

Endpoints principais

### 🔹 API (FastAPI)
- **Local**: `api/`
- **Imagem**: `projeto_futurov1-api`
- **Porta exposta**: `8000`

#### Endpoints principais:

| Método | Rota               | Descrição                                      |
|--------|--------------------|-----------------------------------------------|
| GET    | `/healthcheck`     | Verifica se a API está no ar                  |
| POST   | `/predictions`     | Recebe parâmetros, aciona o serviço NN e retorna a previsão |


Segurança

    O SQLite está isolado via volume Docker.

    Nenhum dado sensível é armazenado ou versionado no Git.

    Para produção, considere usar PostgreSQL e autenticação JWT na API.

Contribuição

Sinta-se livre para abrir issues, sugerir melhorias ou criar Pull Requests!
Licença

Este projeto está licenciado sob a MIT License.
