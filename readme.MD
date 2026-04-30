
# AI Agents Framework

API FastAPI para orquestrar três abordagens de agentes com OpenAI:
CrewAI, LangGraph e saída estruturada com Pydantic.

## Visão geral

O projeto expõe uma API em `app/main.py` com as seguintes rotas:

- `GET /` retorna um resumo rápido da aplicação.
- `POST /api/agents/crewai` executa o fluxo com CrewAI.
- `POST /api/agents/langgraph` executa o fluxo com LangGraph.
- `POST /api/agents/pydantic` executa o agente com saída estruturada via Pydantic/OpenAI.

Os agentes foram pensados para responder consultas em português do Brasil, com foco em análise de e-commerce e métricas de negócio como LTV, CAC, ROI e ticket médio.

## Estrutura

- `app/main.py` inicializa a API FastAPI.
- `app/api/endpoints.py` concentra as rotas dos agentes.
- `app/core/models.py` define os contratos de request e response.
- `app/core/config.py` carrega as variáveis de ambiente.
- `app/agents/` contém as implementações de CrewAI, LangGraph e Pydantic.
- `app/utils/helpers.py` normaliza as respostas para `dict`.

## Requisitos

- Python 3.10 ou superior.
- Chave de API da OpenAI.

## Instalação

Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env` na raiz do projeto com a chave da OpenAI:

```env
OPENAI_API_KEY=sua-chave-aqui
```

## Executando a API

Você pode iniciar o servidor diretamente:

```bash
python3 app/main.py
```

Ou usar Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Depois disso, acesse:

- Swagger: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## Contrato da API

### Request

Todas as rotas recebem o mesmo payload:

```json
{
	"query": "Analise o comportamento de vendas do último trimestre",
	"session_id": "opcional"
}
```

### Response

As respostas seguem o modelo `AgentResponse`, com campos como `agent_name`, `status` e `result`.

## Exemplos de uso

### CrewAI

```bash
curl -X POST http://localhost:8000/api/agents/crewai \
	-H "Content-Type: application/json" \
	-d '{"query":"Analise CAC e ticket médio do e-commerce"}'
```

### LangGraph

```bash
curl -X POST http://localhost:8000/api/agents/langgraph \
	-H "Content-Type: application/json" \
	-d '{"query":"Crie uma análise executiva do funil de vendas"}'
```

### Pydantic

```bash
curl -X POST http://localhost:8000/api/agents/pydantic \
	-H "Content-Type: application/json" \
	-d '{"query":"Resuma os principais indicadores do negócio"}'
```

## Observações

- O projeto usa `gpt-4o-mini` nas implementações atuais dos agentes.
- Se a variável `OPENAI_API_KEY` estiver no ambiente, ela tem prioridade; caso contrário, o app tenta carregar o valor do `.env`.
- As respostas são normalizadas para facilitar o consumo via API.