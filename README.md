# Projeto_FuturoV1

O **Projeto_FuturoV1** é uma aplicação modular baseada em contêineres Docker, composta por três serviços principais:

- **API (FastAPI)**: expõe uma interface HTTP para inferência de dados.
- **Worker**: agenda tarefas recorrentes para execution e grava dados em um banco local.
- **NN (Neural Network)**: É um serviço FastAPI que carrega um modelo treinado (Linear Regression baseado no dia do ano para prever o preço do Bitcoin) e expõe um endpoint para fornecer previsões.

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
  - `POST /predictions` → Recebe um JSON com `{'day_of_year': int}`. Consulta o serviço NN para obter uma nova previsão e a retorna.

### 🔹 Worker (Agendador)
- **Local**: `worker/`
- **Imagem**: `projeto_futurov1-worker`
- **Função**: Periodicamente (conforme configurado, ex: via cron) busca o dia do ano atual, solicita uma previsão ao serviço NN e grava o resultado em `/data/app.db`. Também pode acionar o re-treinamento do modelo.

### 🔹 NN (Rede Neural)
- **Local**: `nn/`
- **Imagem**: `projeto_futurov1-nn` (Nota: o nome da imagem pode ser `nn_service` ou similar dependendo do `docker-compose.yml`)
- **Função**: Serviço FastAPI rodando na porta 8001. Carrega o modelo `modelo_btc.pkl` (regressão linear que usa o dia do ano para prever o preço do BTC) e fornece previsões através do endpoint `POST /predict` (interno ao sistema Docker). É chamado pela API e pelo Worker.
- **Porta exposta (container)**: `8001`

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
| POST   | `/predictions`     | Recebe um JSON no corpo da requisição com `{'day_of_year': int}`. Aciona o serviço NN para obter uma nova previsão e a retorna diretamente. |


Segurança

    O SQLite está isolado via volume Docker.

    Nenhum dado sensível é armazenado ou versionado no Git.

    Para produção, considere usar PostgreSQL e autenticação JWT na API.

Contribuição

Sinta-se livre para abrir issues, sugerir melhorias ou criar Pull Requests!
Licença

Este projeto está licenciado sob a MIT License.
