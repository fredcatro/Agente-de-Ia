import os
from dotenv import load_dotenv
from google import genai

# Carga das variáveis de ambiente do arquivo .env
load_dotenv()

def carregar_contexto(pasta):
    """Lê todos os arquivos .txt da pasta e junta em um único texto de contexto."""
    contexto = ""
    for raiz, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            if arquivo.endswith(".txt"):
                caminho_completo = os.path.join(raiz, arquivo)
                with open(caminho_completo, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                    contexto += f"\n--- DOCUMENTO: {arquivo} ---\n{conteudo}\n"
    return contexto

def iniciar_agente():
    # Inicializa o cliente do Gemini usando a API Key do arquivo .env
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Erro: A chave GEMINI_API_KEY não foi encontrada no arquivo .env!")
        return

    client = genai.Client(api_key=api_key)
    
    print("🤖 Carregando base de conhecimento...")
    base_conhecimento = carregar_contexto("docs")
    
    print("✅ Base carregada com sucesso!")
    print("=" * 60)
    print("🤖 Agente de IA da empresa pronto! Faça suas perguntas (ou digite 'sair').")
    print("=" * 60 + "\n")

    # Inicializa a sessão de chat (evita os avisos de AFC do terminal)
    chat = client.chats.create(model="gemini-2.0-flash")

    while True:
        pergunta_usuario = input("Você: ")
        if pergunta_usuario.lower() in ["sair", "exit"]:
            print("🤖 Agente finalizado. Até logo!")
            break

        # Estrutura do prompt enviando a base de dados + pergunta do usuário
        prompt = f"""
Você é um assistente virtual de suporte interno de uma empresa.
Responda à pergunta do usuário utilizando estritamente as informações fornecidas abaixo na Base de Conhecimento.
Se a informação não estiver na base, responda educadamente que não possui essa informação nos documentos internos.

BASE DE CONHECIMENTO:
{base_conhecimento}

PERGUNTA DO USUÁRIO:
{pergunta_usuario}
"""

        try:
            resposta = chat.send_message(prompt)
            print(f"\n🤖 Agente: {resposta.text}\n")
            print("-" * 60)
        except Exception as e:
            print(f"\nErro ao consultar o Gemini: {e}\n")

if __name__ == "__main__":
    iniciar_agente()