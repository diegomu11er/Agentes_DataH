from langchain.schema import HumanMessage
from llms import llm_padrao


import warnings
warnings.filterwarnings('ignore')


# Criando o agente
def agente(pergunta:str) -> str: 
    # [HumanMessage(content=pergunta)] == [("human", f"{pergunta}")]
    resposta = llm_padrao.invoke([HumanMessage(content=pergunta)])
    return resposta


if __name__ == '__main__':
    resposta = agente("Qual a raiz quadrada de 256?")
    print(resposta.content)