import requests
import time
import os
import glob
import sys
from docx import Document
from audio import frente, verso, audios, caminho_midia_anki, caminho_dos_audios
from config import baralho_anki

sys.stdout.reconfigure(encoding='utf-8')
def limpar_documento(caminho):
    doc = Document()
    doc.save(caminho)
    print(f"Conteúdo apagado de: {caminho}")

def adicionar_cartao_anki(frente_txt, verso_txt, audio_tag, baralho_anki): # Mude para seu baralho
    # Extrai o nome do arquivo de áudio (remove [sound: e ])
    audio_file = audio_tag[7:-1].strip() if audio_tag.startswith("[sound:") and audio_tag.endswith("]") else ""
    
    # Valida os campos
    if not frente_txt.strip() or not verso_txt.strip():
        print(f"Pulando cartão: Frente ou verso vazios (Frente: '{frente_txt}', Verso: '{verso_txt}')")
        return False
    
    # Monta o payload
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": baralho_anki,
                "modelName": "Básico",
                "fields": {
                    "Frente": frente_txt,  # Áudio será adicionado separadamente
                    "Verso": verso_txt
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": ["automatica"],
                "audio": [
                    {
                        "filename": audio_file,
                        "path": os.path.join(caminho_midia_anki, audio_file),
                        "fields": ["Frente"]  # Vincula o áudio ao campo Front
                    }
                ] if audio_file else []
            }
        }
    }

    # Envia a requisição
    try:
        resposta = requests.post("http://localhost:8765", json=payload)
        resultado = resposta.json()
        if "error" in resultado and resultado["error"]:
            print(f"Erro ao criar cartão (Frente: '{frente_txt}'): {resultado['error']}")
            return False
        else:
            print(f"Cartão criado com sucesso: '{frente_txt}'".encode('utf-8', errors='ignore').decode())
            return True
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao Anki. Certifique-se de que o Anki está aberto e o AnkiConnect está ativo.")
        return False

# Verifica os dados de entrada
print("Verificando dados de entrada...")
for i, (f, v, a) in enumerate(zip(frente, verso, audios), 1):
    print(f"Cartão {i}: Frente='{f.encode('ascii', 'ignore').decode()}', Verso='{v.encode('ascii', 'ignore').decode()}', Áudio='{a}'")


# Envia todos os cartões
cartoes_adicionados = 0
for en, pt, audio in zip(frente, verso, audios):
    if adicionar_cartao_anki(en, pt, audio, baralho_anki): 
        cartoes_adicionados += 1
    time.sleep(0.5)

print(f"Processo concluído! {cartoes_adicionados} cartões adicionados com sucesso.")

arquivos = ["frente.docx", "verso.docx", "audio.docx"]

for arquivo in arquivos:
   limpar_documento(arquivo)

print("Processo concluído com sucesso!")

# Arquivos gerados pelo TTSMaker
arquivos_mp3 = glob.glob(os.path.join(caminho_dos_audios, "ttsmaker-vip-file*.mp3"))

for arquivo in arquivos_mp3:
    try:
        os.remove(arquivo)
        print(f"[LIMPO] Arquivo removido: {os.path.basename(arquivo)}")
    except Exception as e:
        print(f"[ERRO] Falha ao remover {os.path.basename(arquivo)}: {e}")