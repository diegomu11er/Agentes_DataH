import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# Vamos carregar as variáveis de ambiente do arquivo .env
from configuracao import carrega_variaveis_ambiente
carrega_variaveis_ambiente()

# Cria os modelos do Curs
llm_padrao = ChatGroq(temperature=0, groq_api_key=os.getenv('GROQ_API_KEY'), model_name='llama-3.3-70b-versatile')        # .env/Secret = GROQ_API_KEY
llm_openai = ChatOpenAI(temperature=0, model="gpt-4o-mini")                                                               # .env/Secret = OPENAI_API_KEY
llm_gemini = ChatGoogleGenerativeAI(temperature=0, model='gemini-1.5-flash-latest')                                       # .env/Secret = GOOGLE_API_KEY
llm_groq_p = ChatGroq(temperature=0, groq_api_key=os.getenv('GROQ_API_KEY'), model_name='deepseek-r1-distill-llama-70b')  # .env/Secret = GROQ_API_KEY

    