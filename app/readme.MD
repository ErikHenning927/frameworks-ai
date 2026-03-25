
---

## 🚀 Guia Rápido: Como Instalar e Rodar o Projeto

### 1. Pré-requisitos
- Python 3.10 ou superior.
- Chave de API da OpenAI.

### 2. Configurando o Ambiente Virtual e a API Key
Na raiz do projeto, crie um ambiente virtual (venv) para evitar sobreposição de bibliotecas na sua máquina:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac. Se usar Windows, rode: venv\Scripts\activate
```

Instale as dependências essenciais do framework base
```bash
pip install -r requirements.txt
```

Crie um arquivo estrito `.env` na raiz do projeto para setar sua chave. Você pode se basear no `.env.example`:
```env
OPENAI_API_KEY=sk-sua-chave-aqui
```

### 3. Rodando os Agentes Individuais (A Base do Projeto)
Em um terminal (com o `venv` ativo acima), inicie a API FastAPI principal que cuida do tráfego para os motores. O padrão é subir na **porta 8000**:
```bash
python3 app/main.py
```
Esse servidor expõe a infraestrutura limpa do LangGraph, Pydantic e CrewAI em suas devidas rotas limpas. Vá para `http://localhost:8000/docs` no navegador para interagir com o Swagger.