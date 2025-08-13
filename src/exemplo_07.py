from llms import llm_padrao
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent

import warnings
warnings.filterwarnings('ignore')


# Criando o agente
def agente(pergunta:str) -> str: 
    prompt = PromptTemplate(
        input_variables=["pergunta", "agent_scratchpad"],
        template="""Você é um assistente inteligente com acesso a duas ferramentas:
                        1. Calculadora
                        2. Wikipedia    
                    Dado a pergunta abaixo, diga o que pretende fazer.
                    Pergunta: {pergunta}
                    {agent_scratchpad}
                    Responda no formato:
                    Ação: [Calculadora|Wikipedia|Responder diretamente]
                    Motivo: ...
        """
    )
    agente = create_tool_calling_agent(llm_padrao, [], prompt)
    executor_do_agente = AgentExecutor(agent=agente, tools=[])
    resposta = executor_do_agente.invoke({"pergunta": pergunta})
    return resposta


if __name__ == '__main__':
    resposta = agente("Qual a raiz quadrada de 256?")
    print(resposta.get("output", "Não encontrei a resposta"))