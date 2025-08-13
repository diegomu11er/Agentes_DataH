# Aula de Agentes - 2025

## Pré requisitos necessários

* Python 3.10+ (https://www.python.org/downloads/)
* UV (https://docs.astral.sh/uv/)
* Git Client (https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git)
* Sistema Operaciona: Linux ou Windows

```python
# Instalando o UV para gerenciar nosso projeto. 
pip install uv
```

## Configurando o projeto

1. Baixar o repositório do servidor Git.

```sh
# Baixa o projeto
git clone https://knowledgebase.datah.com.br/cmpiovan/aula-agentes-2005.git
# Entra na pasta do projeto
cd aula-agentes-2005
```

2. Iniciando o gerenciador de pacotes `UV` do projeto.

```python
uv init
```

3. Criando o ambiente para instalar os pacotes do projeto

```python
uv venv --python=3.10
```

4. Ativando o environment do projeto

```sh
# No Windows
.venv\Scripts\activate

# No Linux
venv/Scripts/activate
```

5. Instalando os pacotes utilizados

```sh
uv pip install python-dotenv openai ipykernel numexpr \
             langchain langchain_groq langchain_google_genai \
             langchain_openai langchain_experimental langchain-community langchain_groq google-generativeai \
             langgraph pypdf chromadb langchain_chroma fastmcp langchain_mcp_adapters==0.0.9 \
             pydantic graphviz grandalf pydot requests matplotlib pandas tabulate
```

6. Instalando o visualizador de Grafo - `Graphviz`

* **Linux - Ubuntu/Debian**

```sh
# Instalando o graphviz, para gerarmos nossos fluxos em PNG
apt install graphviz graphviz-dev -y

# Instalando o pacote do graphviz no python
pip install --config-settings="--global-option=build_ext" --config-settings="--global-option=-I/usr/include/graphviz" pygraphviz 
```

* **Windows**

Link para download do instalador: https://graphviz.org/download/

Link do download para Windows 11 64bits https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/11.0.0/windows_10_cmake_Release_graphviz-install-11.0.0-win64.exe

```sh
# Basta instalar usando o setup
# Adicionar no PATH do Windows ==> "C:\Program Files\Graphviz\bin"

pip install --config-settings="--global-option=build_ext" --config-settings="--global-option=-IC:\Program Files\Graphviz\include" --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz

```

7. Rodando os arquivos

Antes de rodar é necessário configurar o arquivo `.env`. Para isso faça uma cópia do arquivo `.env.sample` para o `.env` no mesmo diretório do projeto e edite o arquivo `.env` adicionando os valores as chaves.

Exemplo do arquivo:
```sh
# Chave da API do Groq. (https://groq.com/) - 95% dos exemplos baseado no Groq
GROQ_API_KEY=

# Chave da API da OpenAI. (https://platform.openai.com/docs/overview) - Alguns exemplos utilizam
OPENAI_API_KEY=

# Chave da API do Claude - Não obrigatório, não utilizamos.
ANTHROPIC_API_KEY=

# Chave da API do Gemini - (https://gemini.google.com/app?hl=pt-BR) - Utilizamos em um exemplo
GOOGLE_API_KEY=

# Usuário e senha do Gmail, para envio de e-mail
# Caso queira trocar de SMTP, edite o mcp_helpers.py
SMTP_USERNAME=
SMTP_PASSWORD=

```


* Rodando os arquivos
```sh
# Sintaxe: python <arquivo.py>

# Windows
.venv/Scripts/python.exe src/exemplo_01.py

# Linux
.venv/Scripts/python src/exemplo_01.py
```

# Anexo I - Groq

## Criando uma conta no Groq para conseguirmos uma **Free API Key** 😎

![groq](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iTGF5ZXJfMiIgZGF0YS1uYW1lPSJMYXllciAyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAuMTggNjkuNzYiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgewogICAgICAgIGZpbGw6ICNmZmY7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDxnIGlkPSJMYXllcl8xLTIiIGRhdGEtbmFtZT0iTGF5ZXIgMSI+CiAgICA8cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0xMTQuMjYuMTNjLTEzLjE5LDAtMjMuODgsMTAuNjgtMjMuODgsMjMuODhzMTAuNjgsMjMuOSwyMy44OCwyMy45LDIzLjg4LTEwLjY4LDIzLjg4LTIzLjg4aDBjLS4wMi0xMy4xOS0xMC43MS0yMy44OC0yMy44OC0yMy45Wk0xMTQuMjYsMzguOTRjLTguMjQsMC0xNC45My02LjY5LTE0LjkzLTE0LjkzczYuNjktMTQuOTMsMTQuOTMtMTQuOTMsMTQuOTMsNi42OSwxNC45MywxNC45M2MtLjAyLDguMjQtNi43MSwxNC45My0xNC45MywxNC45M2gwWiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJNMjQuMTEsMEMxMC45Mi0uMTEuMTMsMTAuNDcsMCwyMy42NmMtLjEzLDEzLjE5LDEwLjQ3LDIzLjk4LDIzLjY2LDI0LjExaDguMzF2LTguOTRoLTcuODZjLTguMjQuMTEtMTUtNi41LTE1LjEtMTQuNzQtLjExLTguMjQsNi41LTE1LDE0Ljc0LTE1LjFoLjM0YzguMjIsMCwxNC45NSw2LjY5LDE0Ljk1LDE0LjkzaDB2MjEuOThoMGMwLDguMTgtNi42NSwxNC44My0xNC44MSwxNC45My0zLjkxLS4wNC03LjYzLTEuNTktMTAuMzktNC4zOGwtNi4zMyw2LjMxYzQuNCw0LjQyLDEwLjM0LDYuOTIsMTYuNTcsNi45OWguMzJjMTMuMDItLjE5LDIzLjQ5LTEwLjc1LDIzLjU2LTIzLjc3di0yMi42OUM0Ny42NSwxMC4zNSwzNy4wNS4wMiwyNC4xMSwwWiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJNMTkxLjI4LDY4Ljc0VjIzLjQzYy0uMzItMTIuOTYtMTAuOTItMjMuMjgtMjMuODgtMjMuMy0xMy4xOS0uMTMtMjMuOTgsMTAuNDctMjQuMTEsMjMuNjYtLjEzLDEzLjE5LDEwLjQ5LDIzLjk4LDIzLjY4LDI0LjExaDguMzF2LTguOTRoLTcuODZjLTguMjQuMTEtMTUtNi41LTE1LjEtMTQuNzRzNi41LTE1LDE0Ljc0LTE1LjFoLjM0YzguMjIsMCwxNC45NSw2LjY5LDE0Ljk1LDE0LjkzaDB2NDQuNjNoMGw4LjkyLjA2WiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJNNTQuOCw0Ny45aDguOTJ2LTIzLjg4YzAtOC4yNCw2LjY5LTE0LjkzLDE0LjkzLTE0LjkzLDIuNzIsMCw1LjI1LjcyLDcuNDYsMmw0LjQ4LTcuNzVjLTMuNS0yLjAyLTcuNTgtMy4xOS0xMS45Mi0zLjE5LTEzLjE5LDAtMjMuODgsMTAuNjgtMjMuODgsMjMuODh2MjMuODhaIi8+CiAgICA8cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0xOTguMDEuNzRjLjY4LjM4LDEuMjEuOTEsMS41OSwxLjU5LjM4LjY4LjU3LDEuNDIuNTcsMi4yNXMtLjE5LDEuNTctLjU5LDIuMjdjLS40LjY4LS45MywxLjIzLTEuNjEsMS42MS0uNjguNC0xLjQ0LjU5LTIuMjUuNTlzLTEuNTctLjE5LTIuMjUtLjU5Yy0uNjgtLjQtMS4yMS0uOTMtMS41OS0xLjYxLS4zOC0uNjgtLjU5LTEuNDItLjU5LTIuMjVzLjE5LTEuNTcuNTktMi4yNWMuMzgtLjY4LjkzLTEuMjEsMS42MS0xLjYxczEuNDQtLjU5LDIuMjctLjU5Yy44MywwLDEuNTcuMTksMi4yNS41OVpNMTk3LjU3LDcuNzVjLjU1LS4zMi45OC0uNzYsMS4zLTEuMzIuMzItLjU1LjQ3LTEuMTcuNDctMS44NXMtLjE1LTEuMy0uNDctMS44NS0uNzQtLjk4LTEuMjctMS4zYy0uNTUtLjMyLTEuMTctLjQ3LTEuODUtLjQ3cy0xLjMuMTctMS44NS40OWMtLjU1LjMyLS45OC43Ni0xLjMsMS4zMnMtLjQ3LDEuMTctLjQ3LDEuODUuMTUsMS4zLjQ3LDEuODVjLjMyLjU1Ljc0LDEsMS4yNywxLjMyLjU1LjMyLDEuMTUuNDksMS44My40OS43LS4wNCwxLjMyLS4yMSwxLjg3LS41M1pNMTk3Ljg0LDQuODJjLS4xNS4yNS0uMzguNDUtLjY4LjU5bDEuMDYsMS42NGgtMS4zMmwtLjkxLTEuNDJoLS44N3YxLjQyaC0xLjMyVjIuMTdoMi4xMmMuNjYsMCwxLjE5LjE1LDEuNTcuNDcuMzguMzIuNTcuNzQuNTcsMS4yNywwLC4zNC0uMDguNjYtLjIzLjkxWk0xOTUuODUsNC42NWMuMywwLC41My0uMDYuNjgtLjE5LjE3LS4xMy4yNS0uMzIuMjUtLjU1cy0uMDgtLjQyLS4yNS0uNTctLjQtLjE5LS42OC0uMTloLS43NHYxLjUzaC43NHYtLjAyWiIvPgogIDwvZz4KPC9zdmc+)\
Fonte: https://groq.com/

**Groq** (https://groq.com) é uma empresa americana de inteligência artificial fundada em 2016 por ex-engenheiros do Google. Seu principal diferencial e inovação reside no desenvolvimento de um circuito integrado específico para aplicações de IA que eles chamam de **LPU** (**Language Processing Unit**), e hardware relacionado.

A missão da Groq é acelerar o desempenho da inferência de cargas de trabalho de IA, ou seja, o processo de usar um modelo de IA já treinado para gerar previsões ou respostas. Eles se destacam por oferecer velocidade de processamento e eficiência incomparáveis, superando as GPUs (Graphics Processing Units) nesse aspecto, que foram originalmente projetadas para processamento gráfico e adaptadas para IA.

**Pontos Chave sobre o Groq:**

1. **LPU (Language Processing Unit)**: É o chip especializado da Groq. Diferente das GPUs, que são mais versáteis, as LPUs foram projetadas especificamente para a inferência de modelos de IA, especialmente Large Language Models (LLMs - Grandes Modelos de Linguagem). Essa especialização permite que as LPUs atinjam latências ultrabaixas e alto throughput (taxa de geração de tokens por segundo).
2. **Velocidade Instantânea**: A Groq tem ganhado destaque no mercado por sua capacidade de gerar respostas de LLMs quase instantaneamente. Eles frequentemente demonstram que seus sistemas podem gerar centenas ou até milhares de tokens por segundo, um desempenho significativamente mais rápido do que muitas outras soluções disponíveis.
3. **Eficiência Energética e Custo**: Além da velocidade, a arquitetura da LPU também é otimizada para maior eficiência energética e menor custo por inferência em comparação com as GPUs tradicionais.

\
Em resumo, a **Groq** se posiciona como uma alternativa poderosa à **NVIDIA** no espaço de hardware de IA, focando especificamente em oferecer a inferência de LLMs mais rápida e eficiente do mercado por meio de sua inovadora tecnologia LPU.

Até a geração desse material o Groq oferece API Key gratuitas para desenvolvedores testarem diversos tipos de modelos. Para conseguir uma API, você deve se registrar no Groq e criar uma Free API Key.

\

![groq](https://middleware.datah.ai/groq.gif)


# Anexo II - Secrets

Agora vamos configurar nossa API nos **Secrets** Google Colaboratory.

\
![secrets](https://middleware.datah.ai/secrets.gif)