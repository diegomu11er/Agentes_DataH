from langchain.globals import set_debug
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.agents import AgentExecutor, create_react_agent
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain import hub
from llms import llm_groq_p

import warnings
warnings.filterwarnings('ignore')

# Visualizar os detalhes da execução
set_debug(True)


def agente_langchain(llm:BaseChatModel) -> dict:
    ferramentas = [PythonAstREPLTool()]

    prompt = hub.pull("hwchase17/react")
    print('\n','-'*40,'\n',prompt.template, '\n','-'*40, '\n')

    agente = create_react_agent(llm, ferramentas, prompt)
    executor_do_agente = AgentExecutor(agent=agente, tools=ferramentas, handle_parsing_errors=True)
    return executor_do_agente


if __name__ == '__main__':
    executor_do_agente = agente_langchain(llm_groq_p)  # DeepSeek R1

    pergunta = "Qual é a área do triângulo com base 10 e altura 5?"

    resposta = executor_do_agente.invoke({"input": pergunta})
    print(f'\n\nResposta DeepSeek R1: {resposta.get("output", "Não encontrei a resposta")}\n')


