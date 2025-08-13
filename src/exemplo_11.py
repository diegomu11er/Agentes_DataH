
from langchain.globals import set_debug
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from configuracao import OUTPUT_DOCUMENTS_DIR, carrega_variaveis_ambiente
from llms import llm_padrao

# Vamos carregar as variáveis de ambiente do arquivo .env
carrega_variaveis_ambiente()

import warnings
warnings.filterwarnings('ignore')

# Visualizar os detalhes da execução
set_debug(False)


def carrega_banco_de_dados_vetorial(path_documentos:str) -> Chroma:
    try:
        # Carrega o banco de dados vetorial existente
        embeddings = OpenAIEmbeddings() # .env/Secret = OPENAI_API_KEY
        vectorstore = Chroma(persist_directory=path_documentos, embedding_function=embeddings)
        return vectorstore
    except Exception as e:
        print(f"Erro ao carregar o banco de dados vetorial: {e}")
        return None


def busca_na_base_de_documentos(pergunta:str) -> str:
    """Use esta ferramenta para responder perguntas sobre a Data H, seus produtos como NIC, Consultoria, Cyber Segurança,
       ou qualquer informação contida na base de conhecimento. A entrada deve ser a pergunta do usuário."""
    vectorstore = carrega_banco_de_dados_vetorial(f'{OUTPUT_DOCUMENTS_DIR}vectorstore')
    contexto = None
    if vectorstore:
        retriever = vectorstore.as_retriever()
        docs = retriever.invoke(pergunta)
        contexto = "\n\n".join([doc.page_content for doc in docs])
    return contexto


def agente_langchain(llm:BaseChatModel) -> dict:
    ferramentas = []
    memoria = ConversationBufferMemory(memory_key="chat_history", return_messages=True, input_key="input") # Retorna o histórico como uma lista de objetos de mensagem
    prompt = PromptTemplate(
        input_variables=["input", "context", "chat_history", "agent_scratchpad"], # Variáveis de entrada
        template="""{chat_history}
            Você é um agente de IA especializado em responder perguntas.
            Contexto: {context}
            Pergunta: {input}
            {agent_scratchpad}
        """
    )
    agente = create_tool_calling_agent(llm, ferramentas, prompt)
    executor_do_agente = AgentExecutor(agent=agente, tools=ferramentas, memory=memoria)
    return executor_do_agente


if __name__ == '__main__':
    executor_do_agente = agente_langchain(llm_padrao)

    pergunta = "O que é o NIC?"

    contexto = ''
    resposta = executor_do_agente.invoke({"input": pergunta, "context": contexto})
    print(f'\n\nResposta sem Contexto: {resposta.get("output", "Não encontrei a resposta")}\n')
    
    print('-'*40)

    contexto = busca_na_base_de_documentos(pergunta) or ''
    resposta = executor_do_agente.invoke({"input": pergunta, "context": contexto})
    print(f'\n\nResposta com Contexto: {resposta.get("output", "Não encontrei a resposta")}\n')

    print('-'*40)

    pergunta = "De qual empresa é esse produto e onde ela fica?"
    contexto = busca_na_base_de_documentos(pergunta) or ''
    resposta = executor_do_agente.invoke({"input": pergunta, "context": contexto})
    print(f'\n\nResposta com Contexto e Memória: {resposta.get("output", "Não encontrei a resposta")}\n')
