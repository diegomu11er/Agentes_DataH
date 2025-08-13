import datetime
from langchain.tools import tool
from langchain.globals import set_debug
from langchain.memory import ConversationBufferMemory
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
    return f"A data e hora atual é: {now.strftime('%Y-%m-%d %H:%M:%S')}"


def agente_langchain(llm:BaseChatModel, usar_ferramentas:bool=True) -> dict:
    ferramentas = [get_current_time] if usar_ferramentas else []

    # Retorna o histórico como uma lista de objetos de mensagem
    memoria = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"), # O placeholder para o histórico
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"), # Onde o agente irá escrever suas anotações (Pensamento)
        ]
    )
    agente = create_tool_calling_agent(llm, ferramentas, prompt)
    executor_do_agente = AgentExecutor(agent=agente, tools=ferramentas, memory=memoria)
    return executor_do_agente


if __name__ == '__main__':
    executor_do_agente = agente_langchain(llm_padrao, usar_ferramentas=True)

    resposta = executor_do_agente.invoke({"input": "Qual é a data inicial e final dessa semana?"})
    print(f'\n\nResposta: {resposta.get("output", "Não encontrei a resposta")}\n')
    print('-'*40)
    resposta = executor_do_agente.invoke({"input": "Qual foi minha ultima pergunta?"})
    print(f'\n\nResposta com Memória: {resposta.get("output", "Não encontrei a resposta")}\n')   


