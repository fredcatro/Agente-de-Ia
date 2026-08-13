import os

def carregar_documentos(pasta):
    print(f"--- Lendo arquivos na pasta: {pasta} ---")
    for raiz, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            print(f"Documento encontrado: {caminho_completo}")

if __name__ == "__main__":
    carregar_documentos("docs")