import os

import google.generativeai as gemini

# Vamos carregar as variáveis de ambiente do arquivo .env
from configuracao import carrega_variaveis_ambiente
carrega_variaveis_ambiente()

import warnings
warnings.filterwarnings('ignore')


# Criando o client para trabalharmos com os agentes.
gemini.configure(api_key=os.environ["GOOGLE_API_KEY"])


# Criando o agente
def agente_manual_gemini(pergunta: str) -> str:    
    model_name: str = "gemini-1.5-flash"
    prompt: str = f"""
Você é um assistente inteligente com acesso a duas ferramentas:
1. Calculadora
2. Wikipedia

Dado a pergunta abaixo, diga o que pretende fazer.

Pergunta: {pergunta}

Responda no formato:
Ação: [Calculadora|Wikipedia|Responder diretamente]
Motivo: ...
    """
    
    # Inicializa o modelo
    model = gemini.GenerativeModel(model_name)
    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [prompt]
            }
        ]
    )

    return response.text


if __name__ == '__main__':
    resposta = agente_manual_gemini("Qual a raiz quadrada de 256?")
    print("Resposta Gemini:", resposta)
    print('-'*40)
    resposta = agente_manual_gemini("Qual a população de Ribeirão Preto.")
    print("Resposta Gemini:", resposta)
