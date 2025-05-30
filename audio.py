import os
import shutil
import time
from docx import Document
from frente import ler_frases
from config import caminho_dos_audios, caminho_midia_anki


documento = Document()

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
#assert len(frente) == len(verso), "Os arquivos devem ter o mesmo número de frases!"


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
            
