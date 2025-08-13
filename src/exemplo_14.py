import datetime
import pandas as pd

from langchain.tools import tool
from langchain.globals import set_debug
from langchain_core.prompts import PromptTemplate
from langchain_experimental.tools import PythonAstREPLTool
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain_core.language_models.chat_models import BaseChatModel
from configuracao import OUTPUT_DOCUMENTS_DIR
from llms import llm_padrao, llm_openai

set_debug(True)


@tool
def get_current_time(*args, **kwargs) -> str:
    """O objetivo dessa ferramenta é retornar a data e hora atual."""
    now = datetime.datetime.now()
    return f"A data e hora atual é: {now.strftime('%Y-%m-%d %H:%M:%S')}"


def dataframe_python_code(df) -> str:    
    return Tool(
                name="Códigos Python",
                func=PythonAstREPLTool(locals={"df": df}),
                description="""Utilize esta ferramenta sempre que o usuário solicitar cálculos, consultas, análises ou transformações
                específicas usando Python diretamente sobre o DataFrame `df`.
                Exemplos de uso incluem: "Quais seriam as principais notícias da semana?", "Quais são os valores únicos da coluna Y?",
                "Qual a correlação entre A e B?". Evite utilizar esta ferramenta para solicitações mais amplas ou descritivas,
                como informações gerais sobre o DataFrame, resumos estatísticos completos ou geração de gráficos — nesses casos,
                use as ferramentas apropriadas."""
            )


def agente_langchain(llm:BaseChatModel, df:pd.DataFrame) -> dict:
    ferramentas = [dataframe_python_code(df), get_current_time]

    df_head:str = df.head().to_markdown()

    prompt = PromptTemplate(
                    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
                    partial_variables={"df_head": df_head},
                    template = """
                        Você é um assistente que sempre responde em português.

                        Você tem acesso a um dataframe pandas chamado `df`.
                        Aqui estão as primeiras linhas do DataFrame, obtidas com `df.head().to_markdown()`:

                        {df_head}

                        Responda às seguintes perguntas da melhor forma possível.

                        Para isso, você tem acesso às seguintes ferramentas:

                        {tools}

                        Use o seguinte formato:

                        Question: a pergunta de entrada que você deve responder
                        Thought: você deve sempre pensar no que fazer
                        Action: a ação a ser tomada, deve ser uma das [{tool_names}]
                        Action Input: a entrada para a ação
                        Observation: o resultado da ação
                        ... (este Thought/Action/Action Input/Observation pode se repetir N vezes)
                        Thought: Agora eu sei a resposta final
                        Final Answer: a resposta final para a pergunta de entrada original.

                        Comece!

                        Question: {input}
                        Thought: {agent_scratchpad}"""
                )

    agente = create_react_agent(llm, ferramentas, prompt)
    executor_do_agente = AgentExecutor(agent=agente, tools=ferramentas, handle_parsing_errors=True)
    return executor_do_agente


if __name__ == '__main__':
    df = pd.read_csv(f'{OUTPUT_DOCUMENTS_DIR}noticias_publicadas_ultimos_30d.csv')
    agente = agente_langchain(llm_openai, df)
    resposta = agente.invoke({"input": "Quais foram as top 5 editorias com mais notícias na segunda semana de julho?"})
    print(resposta.get("output", "Não encontrei a resposta"))
    
    print('-'*40)
    
    df = pd.read_csv(f'{OUTPUT_DOCUMENTS_DIR}leitura_ultimos_5d_amostra.csv')
    agente = agente_langchain(llm_openai, df)
    resposta = agente.invoke({"input": "Qual é o percentual de assinantes e não assinantes?"})
    print(resposta.get("output", "Não encontrei a resposta"))

