import os
from datetime import datetime
from crewai import Agent, Task, Crew, Process

from app.core.config import settings

def run_crewai_agent(query: str) -> dict:
    """ 
    Executa um fluxo usando CrewAI como Orquestrador.
    Sempre retorna um dicionário que pode ser serializado para JSON.
    """
    if not os.environ.get("OPENAI_API_KEY") and settings.OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

    llm = "gpt-4o-mini"
    
    current_date = datetime.now().strftime('%d/%m/%Y')
    date_context = f" A data atual do sistema é {current_date}."

    manager = Agent(
        role="Orquestrador Especialista em Dados de E-commerce",
        goal="Analisar a requisição de negócios e coordenar a pesquisa focada em dados do varejo para gerar a resposta mais analítica e estruturada possível.",
        backstory=f"Uma IA sênior, experiente no mercado de e-commerce, especializada em planejar fluxos de análise de dados, métricas financeiras de varejo e delegação de pesquisas.{date_context}",
        llm=llm,
        allow_delegation=True
    )

    researcher = Agent(
        role="Analista Chefe de Dados de E-commerce",
        goal="Fornecer análises profundas sobre métricas de e-commerce (LTV, CAC, ticket médio) e avaliar tendências de vendas com rigor analítico.",
        backstory=f"Especialista renomado no processamento de informações de e-commerce, análise de concorrentes e avaliação do comportamento do cliente no varejo online.{date_context}",
        llm=llm,
        allow_delegation=False
    )

    task = Task(
        description=f"O usuário solicitou: '{query}'. Processe essa requisição utilizando o seu profundo conhecimento de negócios e dados de e-commerce. Lembre-se, a data de hoje é {current_date}.",
        expected_output="Retorne EXCLUSIVAMENTE um JSON válido e puramente estruturado contendo duas chaves: 'reasoning' (seu processo passo a passo de raciocínio lógico) e 'conteudo' (a própria resposta e insights métricos, podendo conter parágrafos). Responda em Português do Brasil.",
        agent=researcher
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        manager=manager,
        process=Process.sequential # Trabalhando sequencialmente mas definindo o papel do manager explicitamente
    )
    
    result = crew.kickoff()
    
    # O result em novas versões do crewai pode ter a propriedade 'raw'
    final_output = result.raw if hasattr(result, 'raw') else str(result)
    
    import json
    reasoning = "O reasoning não pôde ser extraído separadamente, revise a string bruta."
    conteudo = final_output
    
    try:
        clean_json = final_output.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean_json)
        reasoning = parsed.get("reasoning", reasoning)
        conteudo = parsed.get("conteudo", conteudo)
    except:
        pass
    
    return {
        "orquestrador": "CrewAI",
        "tarefa_resolvida": True,
        "reasoning": reasoning,
        "conteudo": conteudo
    }
