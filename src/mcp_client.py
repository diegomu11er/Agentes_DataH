import sys
import asyncio
from uuid import uuid4
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.globals import set_debug


from configuracao import carrega_variaveis_ambiente
carrega_variaveis_ambiente()

import warnings
warnings.filterwarnings('ignore')

set_debug(False)

server_params = {
    # "local-server-tools": {
    #     "command": "C:\\Dados\\Projetos\\aulas\\agent\\.venv\\Scripts\\python.exe",
    #     "args": ["C:/Dados/Projetos/aulas/agent/src/mcp_server.py"],
    #     "transport": "stdio",
    # },
    "server-tools": {
        "url": "http://127.0.0.1:5008/sse",
        "transport": "sse",
    }
}

async def run_agent():
    model:str = "gpt-4o-mini"
    checkpointer = InMemorySaver()
    
    async with MultiServerMCPClient(server_params) as client:

        all_tools = client.get_tools()
        if not all_tools:
            print("\033[31mNenhuma ferramenta disponível no servidor MCP.\033[0m")
            
        for server, tools in client.server_name_to_tools.items():
            print(f'\033[31m\n==== MCP Server UP! - {server} ====\033[0m')
            for tool in tools:
                print(f'\033[35m* {tool.name} *\033[0m\n{tool.description}\n')


        prompt = f"""
            Sua tarefa é solucionar as perguntas do usuário, usando as ferramentas disponíveis e seu próprio conhecimento.                 
            Responda sempre em português.
        """   
        agent = create_react_agent(model, all_tools, checkpointer=checkpointer, prompt=prompt)
        
        session_id = str(uuid4())
        config = {"configurable": {"thread_id": session_id}}

        while True:
            user_input = input("\033[33mFaça a sua pergunta: \033[0m")

            if user_input == "sair":
                break

            if user_input == "limpar":
                print("\033c")
                continue                    

            print(f"\033[34mUsuário: {user_input}\033[0m")    
            
            agent_response = await agent.ainvoke({"messages": user_input}, config=config)
            print(f"\033[32mAgente: {agent_response['messages'][-1].content}\033[0m")

            checkpoint = await checkpointer.aget(config)               


if __name__ == "__main__":
    result = asyncio.run(run_agent())