import sys
import os
import requests
from dotenv import load_dotenv
from IPython import get_ipython

try:
  from google.colab import userdata
except:
  pass

ENV_PATH:str = '.env'

RUNNING_IN_COLAB:str = 'google.colab' in str(get_ipython())
OUTPUT_DOCUMENTS_DIR:str = './documentos/' if not RUNNING_IN_COLAB else '/content/documentos/'

# Somente no Windows
if not RUNNING_IN_COLAB and sys.platform.lower() == "win32" and "Graphviz" not in os.environ["PATH"]: 
    os.environ["PATH"] = os.getenv("PATH", "") + ";C:\\Program Files\\Graphviz\\bin"


def carrega_variaveis_ambiente() -> None:

    # Modo local
    if os.path.exists(ENV_PATH) and not RUNNING_IN_COLAB:
        load_dotenv(ENV_PATH, override=True)

    # Modo Colab
    if RUNNING_IN_COLAB:
      os.environ['GROQ_API_KEY'] = userdata.get('GROQ_API_KEY')
      os.environ['OPENAI_API_KEY'] = userdata.get('OPENAI_API_KEY')
      os.environ['ANTHROPIC_API_KEY'] = userdata.get('ANTHROPIC_API_KEY')
      os.environ['GOOGLE_API_KEY'] = userdata.get('GOOGLE_API_KEY')

      os.environ['SMTP_USERNAME'] = userdata.get('SMTP_USERNAME')
      os.environ['SMTP_PASSWORD'] = userdata.get('SMTP_PASSWORD')


def download(url:str, output_dir:str=OUTPUT_DOCUMENTS_DIR) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    filename = url.split('/')[-1]
    filepath = os.path.join(output_dir, filename)

    if not os.path.exists(filepath):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            print(f"Arquivo baixado com sucesso: {filepath}")
        else:
            print(f"Erro ao baixar o arquivo. Código de status: {response.status_code}")