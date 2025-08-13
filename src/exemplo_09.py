from langchain.globals import set_debug
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from configuracao import OUTPUT_DOCUMENTS_DIR, carrega_variaveis_ambiente

# Vamos carregar as variáveis de ambiente do arquivo .env
carrega_variaveis_ambiente()

import warnings
warnings.filterwarnings('ignore')

# Visualizar os detalhes da execução
set_debug(False)


def cria_banco_de_dados_vetorial(path_documentos:str) -> None:
    try:
        # Carrega os documentos do diretório especificado
        documents = PyPDFDirectoryLoader(path_documentos).load()

        # Usando embeddings do OpenAI
        embeddings = OpenAIEmbeddings() # .env/Secret = OPENAI_API_KEY

        # Cria um banco de dados vetorial usando Chroma
        split_documents = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100).split_documents(documents)

        # Cria o banco de dados vetorial
        vectorstore = Chroma.from_documents(split_documents, embeddings, persist_directory=f'{OUTPUT_DOCUMENTS_DIR}vectorstore')

        print("Banco de dados vetorial criado com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar documentos: {e}")
        


if __name__ == '__main__':
    cria_banco_de_dados_vetorial(path_documentos=OUTPUT_DOCUMENTS_DIR)
    