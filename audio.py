import os
import shutil
from docx import Document
from frente import ler_frases

# Caminho da pasta de downloads
caminho_dos_audios = r'D:\Users\isabe\Downloads'  # Mude para seu usuário
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
assert len(frente) == len(verso), "Os arquivos devem ter o mesmo número de frases!"

# Caminho da pasta de mídia do Anki (ajuste se necessário)
caminho_midia_anki = r'C:\Users\isabe\AppData\Roaming\Anki2\Isabel\collection.media' # Mude para seu usuário


# Copia os arquivos .mp3 da pasta Downloads para a pasta de mídia do Anki
for linha in audios:
    if linha.startswith("[sound:") and linha.endswith("]"):
        nome_arquivo = linha[7:-1].strip()
        origem = os.path.join(caminho_dos_audios, nome_arquivo)
        print(f"Verificando arquivo: {origem}")
        destino = os.path.join(caminho_midia_anki, nome_arquivo)
        if os.path.exists(origem):
            shutil.copy2(origem, destino)
        else:
            print(f"Áudio não encontrado: {nome_arquivo}")
            
