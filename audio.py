import os
import shutil
import time
from docx import Document
from frente import ler_frases

# Caminho da pasta de downloads
caminho_dos_audios = r'D:\Users\isabe\Downloads'  # Mude para seu usuário
documento = Document()

def aguardar_downloads(caminho_dos_audios, quantidade_esperada, timeout=180):
    inicio = time.time()
    
    while True:
        arquivos_mp3 = [f for f in os.listdir(caminho_dos_audios) 
                        if f.startswith("ttsmaker-vip-file") and f.endswith(".mp3")]
        
        arquivos_incompletos = [f for f in os.listdir(caminho_dos_audios) 
                                if f.endswith(".crdownload")]
        
        print(f"Aguardando... {len(arquivos_mp3)}/{quantidade_esperada} concluídos. "
              f"Downloads em andamento: {len(arquivos_incompletos)}")
        
        if len(arquivos_mp3) >= quantidade_esperada and len(arquivos_incompletos) == 0:
            print("Todos os downloads concluídos!")
            return True
        
        if time.time() - inicio > timeout:
            print("Timeout: Downloads não concluídos no tempo esperado.")
            return False
        
        time.sleep(2)
    
quantidade_de_frases = len(ler_frases("frente.docx"))  # assume que 1 áudio por frase
aguardar_downloads(caminho_dos_audios, quantidade_esperada=quantidade_de_frases)

# Lista todos os arquivos mp3 desejados
arquivos = [f for f in os.listdir(caminho_dos_audios) 
            if f.startswith("ttsmaker-vip-file") and f.endswith(".mp3")]

# Ordena por data de modificação (mais antigos primeiro)
arquivos.sort(key=lambda f: os.path.getmtime(os.path.join(caminho_dos_audios, f)))


# Renomeia e adiciona ao documento
for nome_antigo in arquivos:
    
    caminho_antigo = os.path.join(caminho_dos_audios, nome_antigo)
    
    # Adiciona ao Word com o formato que o Anki espera
    linha_audio = f"[sound:{caminho_antigo}]"
    documento.add_paragraph(linha_audio)

# Salva o documento
documento.save("audio.docx")
print("Todos os arquivos foram renomeados e salvos em 'audio.docx'.")

# Lê os arquivos
frente = ler_frases("frente.docx")
verso = ler_frases("verso.docx")
audios = ler_frases("audio.docx")

# Garante que todos têm o mesmo número de linhas
assert len(frente) == len(verso), "Os arquivos devem ter o mesmo número de frases!"

# Caminho da pasta de mídia do Anki (ajuste se necessário)
caminho_midia_anki = r'C:\Users\isabe\AppData\Roaming\Anki2\Isabel\collection.media' # Mude para seu usuário


# Copia os arquivos .mp3 da pasta Downloads para a pasta de mídia do Anki
for linha in audios:
    if linha.startswith("[sound:") and linha.endswith("]"):
        caminho_completo = linha[7:-1].strip()
        nome_arquivo = os.path.basename(caminho_completo)  
        origem = os.path.join(caminho_dos_audios, nome_arquivo)
        print(f"Verificando arquivo: {origem}")
        destino = os.path.join(caminho_midia_anki, nome_arquivo)
        if os.path.exists(origem):
            if os.path.abspath(origem) != os.path.abspath(destino): 
                shutil.copy2(origem, destino)
            else:
                print(f"Arquivo já está na pasta destino: {nome_arquivo}")
        else:
            print(f"Áudio não encontrado: {nome_arquivo}")
            
