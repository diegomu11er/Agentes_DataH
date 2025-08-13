from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.globals import set_debug
from llms import llm_padrao
import warnings
warnings.filterwarnings('ignore')

set_debug(False)

# Criando o agente
def agente_lcel(pergunta:str) -> str:
    modelo:str = llm_padrao # Groq
    prompt:str = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um assistente inteligente com acesso a duas ferramentas:"),
            ("system", "1. Calculadora"),
            ("system", "2. Wikipedia"),
            ("system", "Dado a pergunta abaixo, diga o que pretende fazer."),
            ("human", "{pergunta}"),
            ("system", "Responda no formato:"),
            ("system", "Ação: [Calculadora|Wikipedia|Responder diretamente]"),
            ("system", "Motivo: ..."),
        ])

    # LCEL (LangChain Expression Language)
    cadeia = prompt | modelo | StrOutputParser()
    return cadeia.invoke({"pergunta": pergunta})


if __name__ == '__main__':
    resposta = agente_lcel("Qual a raiz quadrada de 256?")
    print(resposta)