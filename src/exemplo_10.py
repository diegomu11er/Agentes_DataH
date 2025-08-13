from langchain.globals import set_debug
from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from configuracao import OUTPUT_DOCUMENTS_DIR, carrega_variaveis_ambiente

import warnings
warnings.filterwarnings('ignore')

# Vamos carregar as variáveis de ambiente do arquivo .env
carrega_variaveis_ambiente()

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


if __name__ == '__main__':
    vectorstore = carrega_banco_de_dados_vetorial(f'{OUTPUT_DOCUMENTS_DIR}vectorstore')
    docs = None

    if vectorstore:
        retriever = vectorstore.as_retriever()
        docs = retriever.invoke("Data H")
        print(docs)
    else:
        print("Não foi possível carregar o banco de dados vetorial.")

