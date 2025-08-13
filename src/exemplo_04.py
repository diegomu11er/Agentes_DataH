import datetime
from langchain.globals import set_debug
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.agents import AgentExecutor, create_tool_calling_agent
from llms import llm_padrao

import warnings
warnings.filterwarnings('ignore')

# Visualizar os detalhes da execução
set_debug(False)

@tool
def get_current_time(*args, **kwargs) -> str:
    """O objetivo dessa ferramenta é retornar a data e hora atual."""
    now = datetime.datetime.now()
    return f"A data e hora atual é {now.strftime('%Y-%m-%d %H:%M:%S')}"


def agente_langchain(llm:BaseChatModel, usar_ferramentas:bool=True) -> dict:
    ferramentas = [get_current_time] if usar_ferramentas else []
    prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"), # Onde o agente irá escrever suas anotações (Pensamento)
        ]
    )
    agente = create_tool_calling_agent(llm, ferramentas, prompt)
    executor_do_agente = AgentExecutor(agent=agente, tools=ferramentas)
    return executor_do_agente
    


if __name__ == '__main__':
    executor_do_agente = agente_langchain(llm_padrao, usar_ferramentas=False)
    resposta = executor_do_agente.invoke({"input": "Qual é a data inicial e final dessa semana?"})
    print(f'\n\nResposta sem Ferramenta: {resposta.get("output", "Não encontrei a resposta")}\n')
    print('-'*40)
    executor_do_agente = agente_langchain(llm_padrao, usar_ferramentas=True)
    resposta = executor_do_agente.invoke({"input": "Qual é a data inicial e final dessa semana?"})
    print(f'\n\nResposta com Ferramenta: {resposta.get("output", "Não encontrei a resposta")}\n')
    print('-'*40)
    resposta = executor_do_agente.invoke({"input": "Qual foi minha ultima pergunta?"})
    print(f'\n\nResposta sem Memória: {resposta.get("output", "Não encontrei a resposta")}\n')    

