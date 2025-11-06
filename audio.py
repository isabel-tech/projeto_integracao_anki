import os
import shutil
import pandas as pd
from frente import ler_dados_excel
from config import caminho_dos_audios, caminho_midia_anki

# Lê os dados do Excel
frente, verso, audios = ler_dados_excel()

assert len(frente) == len(verso), "Os arquivos devem ter o mesmo número de frases!"

# Lista todos os arquivos mp3 desejados
arquivos_mp3 = [f for f in os.listdir(caminho_dos_audios) 
               if f.startswith("ttsmaker-vip-file") and f.endswith(".mp3")]

# Ordena por data de modificação (mais antigos primeiro)
arquivos_mp3.sort(key=lambda f: os.path.getmtime(os.path.join(caminho_dos_audios, f)))

# Cria lista de áudios no formato do Anki
lista_audios = []
for nome_arquivo in arquivos_mp3:
    caminho_completo = os.path.join(caminho_dos_audios, nome_arquivo)
    linha_audio = f"[sound:{caminho_completo}]"
    lista_audios.append(linha_audio)

# Atualiza a lista de audios com os arquivos baixados
audios = lista_audios

# Copia os arquivos .mp3 para a pasta de mídia do Anki
for linha in audios:
    if linha.startswith("[sound:") and linha.endswith("]"):
        caminho_completo = linha[7:-1].strip()
        nome_arquivo = os.path.basename(caminho_completo)  
        origem = os.path.join(caminho_dos_audios, nome_arquivo)
        destino = os.path.join(caminho_midia_anki, nome_arquivo)
        
        if os.path.exists(origem):
            if os.path.abspath(origem) != os.path.abspath(destino): 
                shutil.copy2(origem, destino)
            else:
                print(f"Arquivo já está na pasta destino: {nome_arquivo}")
        else:
            print(f"Áudio não encontrado: {nome_arquivo}")