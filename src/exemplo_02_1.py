from langchain.globals import set_debug
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from llms import llm_padrao

import warnings
warnings.filterwarnings('ignore')


# Visualizar os detalhes da execução
set_debug(False)

def agente_langchain(pergunta:str) -> dict:
    modelo = llm_padrao # Groq
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um assistente inteligente com acesso a duas ferramentas:"),
            ("system", "1. Calculadora"),
            ("system", "2. Wikipedia"),
            ("system", "Dado a pergunta abaixo, diga o que pretende fazer."),
            ("human", "{pergunta}"),
            ("system", "Responda no formato:"),
            ("system", "Ação: [Calculadora|Wikipedia|Responder diretamente]"),
            ("system", "Motivo: ..."),
            MessagesPlaceholder(variable_name="agent_scratchpad"), # Onde o agente irá escrever suas anotações (Pensamento)
        ]
    )
    agente = create_tool_calling_agent(modelo, tools=[], prompt=prompt)
    executor_do_agente = AgentExecutor(agent=agente, tools=[])
    resposta = executor_do_agente.invoke({"pergunta": pergunta})
    return resposta['output']


if __name__ == '__main__':
    resposta = agente_langchain("Qual a raiz quadrada de 256?")
    print(resposta)