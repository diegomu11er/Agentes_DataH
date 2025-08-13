from langchain.prompts import (
    ChatPromptTemplate, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate, 
    MessagesPlaceholder
)
from langchain.agents import AgentExecutor, create_tool_calling_agent
from llms import llm_padrao

import warnings
warnings.filterwarnings('ignore')


# Criando o agente
def agente(pergunta:str) -> str: 
    prompt:str = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template("Você é um assistente inteligente com acesso a duas ferramentas:"),
            SystemMessagePromptTemplate.from_template("1. Calculadora"),
            SystemMessagePromptTemplate.from_template("2. Wikipedia"),
            SystemMessagePromptTemplate.from_template("Dado a pergunta abaixo, diga o que pretende fazer."),
            HumanMessagePromptTemplate.from_template("{pergunta}"), 
            SystemMessagePromptTemplate.from_template("Responda no formato:"),
            SystemMessagePromptTemplate.from_template("Ação: [Calculadora|Wikipedia|Responder diretamente]"),
            SystemMessagePromptTemplate.from_template("Motivo: ..."),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

    agente = create_tool_calling_agent(llm_padrao, [], prompt)
    executor_do_agente = AgentExecutor(agent=agente, tools=[])    
    resposta = executor_do_agente.invoke({"pergunta": pergunta})
    return resposta


if __name__ == '__main__':
    resposta = agente("Qual a raiz quadrada de 256?")
    print(resposta.get("output", "Não encontrei a resposta"))