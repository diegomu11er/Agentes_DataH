from langchain.globals import set_debug
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentExecutor, create_tool_calling_agent
from llms import llm_openai, llm_gemini
import warnings
warnings.filterwarnings('ignore')


# Visualizar os detalhes da execução
set_debug(False)

def agente_langchain(llm:BaseChatModel, pergunta:str) -> dict:
    # https://python.langchain.com/docs/integrations/tools/
    # https://python.langchain.com/docs/versions/migrating_chains/llm_math_chain/
    ferramentas = load_tools(["llm-math"], llm=llm)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um agente responsável por resolver problemas matemáticos."),
            ("system", "Utilize todas as suas ferramentas disponíveis e responda a pergunta do usuário."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"), # Onde o agente irá escrever suas anotações (Pensamento)
        ]
    )
    agente = create_tool_calling_agent(llm, ferramentas, prompt)
    executor_do_agente = AgentExecutor(agent=agente, tools=ferramentas)
    resposta = executor_do_agente.invoke({"input": pergunta})
    return resposta


if __name__ == '__main__':
    resposta = agente_langchain(llm_openai, "Qual é a raiz quadrada de 169 vezes 2?")
    print(f'\n\nResposta OpenAi: {resposta.get("output", "Não encontrei a resposta")}\n')
    print('-'*40)
    resposta = agente_langchain(llm_gemini, "Qual é a raiz quadrada de 169 vezes 2?")
    print(f'\nResposta Gemini: {resposta.get("output", "Não encontrei a resposta")}\n')