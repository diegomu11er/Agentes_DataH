import os
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langchain.globals import set_debug
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from llms import llm_padrao


import warnings
warnings.filterwarnings('ignore')

# Visualizar os detalhes da execução
set_debug(False)

# Formatação das respostas
def formatar_classificacao_para_estado(classificacao: str):
    palavra_chave = classificacao.lower().strip().split()[0]
    return {"classificacao": palavra_chave}

def formatar_resposta_caes(resposta: str):
    return {"resposta": resposta}

def formatar_resposta_gatos(resposta: str):
    return {"resposta": resposta}


# Cadeias para cada especialidade
def cadeia_cachorro(llm):
    prompt_caes = ChatPromptTemplate.from_template(
        "Você é um especialista em cães. Responda a pergunta a seguir de forma concisa: {pergunta}"
    )
    return prompt_caes | llm | StrOutputParser() | RunnableLambda(formatar_resposta_caes)


def cadeia_gato(llm):
    prompt_gatos = ChatPromptTemplate.from_template(
        "Você é um especialista em gatos. Responda a pergunta a seguir de forma concisa: {pergunta}"
    )
    return prompt_gatos | llm | StrOutputParser() | RunnableLambda(formatar_resposta_gatos)


def cadeia_classificador(llm):
    classificador_prompt = PromptTemplate.from_template(
        """Classifique a seguinte pergunta como 'caes' ou 'gatos'.
            Responda apenas com a palavra 'caes' ou 'gatos'.
        Pergunta: {pergunta}
        
        Tópico:"""
    )    
    return classificador_prompt | llm | StrOutputParser() | RunnableLambda(formatar_classificacao_para_estado)


# Define o estado do nosso grafo
class GrafoState(TypedDict):
    pergunta: str
    classificacao: str
    resposta: str


# Condicional para rotear a pergunta
def rotear_pergunta(state):
    if "caes" in state["classificacao"].lower():
        return "cadeia_caes"
    elif "gatos" in state["classificacao"].lower():
        return "cadeia_gatos"
    else:
        # Padrão para cães se não conseguir classificar
        return "cadeia_caes" 


def fluxo(llm):
    workflow = StateGraph(GrafoState)

    # Adiciona os nós (etapas)
    workflow.add_node("classificador", cadeia_classificador(llm))
    workflow.add_node("cadeia_caes", cadeia_cachorro(llm))
    workflow.add_node("cadeia_gatos", cadeia_gato(llm))

    # O início do grafo
    workflow.set_entry_point("classificador")

    workflow.add_conditional_edges(
        "classificador",
        rotear_pergunta,
        {
            "cadeia_caes": "cadeia_caes",
            "cadeia_gatos": "cadeia_gatos",
        },
    )
    
    # E os pontos de saída
    workflow.add_edge("cadeia_caes", END)
    workflow.add_edge("cadeia_gatos", END)

    # Compila o grafo para uso
    return workflow.compile()

if __name__ == '__main__':
    llm_openai = ChatOpenAI(temperature=0, model='gpt-4o-mini') # .env = OPENAI_API_KEY

    workflow = fluxo(llm_openai)
    
    os.environ["PATH"] = os.getenv("PATH", "") + ";C:\\Program Files\\Graphviz\\bin" 

    print(workflow.get_graph().draw_mermaid())
    print(workflow.get_graph().draw_png("graph.png"))
    workflow.get_graph().print_ascii()

    # Executando o grafo com uma pergunta sobre cães
    pergunta_caes = "Por que os cachorros gostam tanto de brincar de buscar?"
    resultado_caes = workflow.invoke({"pergunta": pergunta_caes})
    print(f"Pergunta: {pergunta_caes}")
    print(f"Resposta: {resultado_caes['resposta']}\n")

    print('-'*40)

    # Executando o grafo com uma pergunta sobre gatos
    pergunta_gatos = "Qual é o som mais comum que os gatos fazem?"
    resultado_gatos = workflow.invoke({"pergunta": pergunta_gatos})
    print(f"Pergunta: {pergunta_gatos}")
    print(f"Resposta: {resultado_gatos['resposta']}")