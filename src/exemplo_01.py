import os

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

# Vamos carregar as variáveis de ambiente do arquivo .env
from configuracao import carrega_variaveis_ambiente
carrega_variaveis_ambiente()

import warnings
warnings.filterwarnings('ignore')

# Criando o client para trabalharmos com os agentes.
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
# ou
client = OpenAI()

# Criando o agente
def agente_manual(pergunta:str) -> str: 
    modelo:str = "gpt-4o-mini"
    prompt:str = f"""
Você é um assistente inteligente com acesso a duas ferramentas:
1. Calculadora
2. Wikipedia

Dado a pergunta abaixo, diga o que pretende fazer.

Pergunta: {pergunta}

Responda no formato:
Ação: [Calculadora|Wikipedia|Responder diretamente]
Motivo: ...
    """

    resposta:ChatCompletion = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}]
    )

    return resposta.choices[0].message.content


if __name__ == '__main__':
    # Utilizando nosso primeiro agente
    resposta = agente_manual("Qual a população de Ribeirão Preto.")
    print(resposta)
    print('-'*40)
    resposta = agente_manual("Qual a raiz quadrada de 256?")
    print(resposta)