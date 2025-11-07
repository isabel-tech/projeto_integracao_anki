import os
import shutil
import pandas as pd
import requests
import time
from frente import ler_dados_excel
from config import caminho_dos_audios, caminho_midia_anki, baralho_anki

class Logger:
    def __init__(self):
        self.width = 65
        
    def header(self, title):
        print(f"\n{'-' * self.width}")
        print(f"{title:^{self.width}}")
        print(f"{'-' * self.width}")
    
    def info(self, message):
        print(f"[INFO] {message}")
    
    def success(self, message):
        print(f"[SUCCESS] {message}")
    
    def error(self, message):
        print(f"[ERROR] {message}")
    
    def card_details(self, card_num, total, frente, verso, audio):
        print(f"\nCartao {card_num} de {total}:")
        print('-' * self.width)
        print(f"Frente: {frente}")
        print(f"Verso: {verso}")
        print(f"Audio: {audio}")
        print('-' * self.width)

logger = Logger()

def limpar_excel(caminho_excel):
    """Limpa as colunas Frente e Verso do Excel após a execução"""
    try:
        df = pd.read_excel(caminho_excel)
        df['Frente'] = ''
        df['Verso'] = ''
        df.to_excel(caminho_excel, index=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao limpar Excel: {e}")
        return False

def preparar_audios():
    """Lê os arquivos MP3 baixados e retorna tags para o Anki"""
    arquivos_mp3 = [f for f in os.listdir(caminho_dos_audios) 
                    if f.startswith("ttsmaker-vip-file") and f.endswith(".mp3")]
    arquivos_mp3.sort(key=lambda f: os.path.getmtime(os.path.join(caminho_dos_audios, f)))
    audios = [f"[sound:{os.path.join(caminho_dos_audios, f)}]" for f in arquivos_mp3]
    return audios

def copiar_arquivos_audio(audios):
    """Copia apenas os arquivos de áudio necessários para a pasta do Anki"""
    try:
        arquivos_copiados = 0
        for audio_tag in audios:
            if audio_tag.startswith("[sound:") and audio_tag.endswith("]"):
                source_path = audio_tag[7:-1].strip()
                nome_arquivo = os.path.basename(source_path)
                dest_path = os.path.join(caminho_midia_anki, nome_arquivo)

                if os.path.exists(source_path):
                    if os.path.abspath(source_path) != os.path.abspath(dest_path):
                        shutil.copy2(source_path, dest_path)
                        arquivos_copiados += 1
                    else:
                        logger.info(f"Arquivo já está na pasta destino: {nome_arquivo}")
                else:
                    logger.error(f"Arquivo não encontrado: {source_path}")

        logger.info(f"Total de arquivos copiados: {arquivos_copiados}")
        return True
    except Exception as e:
        logger.error(f"Erro ao copiar arquivos de audio: {e}")
        return False

def adicionar_cartao_anki(frente_txt, verso_txt, audio_tag, baralho_anki, numero_cartao=0):
    try:
        audio_file = ""
        if audio_tag.startswith("[sound:") and audio_tag.endswith("]"):
            audio_file = os.path.basename(audio_tag[7:-1].strip())

        campo_frente = frente_txt
        if audio_file:
            campo_frente += f"\n[sound:{audio_file}]"

        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": baralho_anki,
                    "modelName": "Básico",
                    "fields": {
                        "Frente": campo_frente,
                        "Verso": verso_txt
                    },
                    "options": {"allowDuplicate": False},
                    "tags": ["automatica"]
                }
            }
        }

        resposta = requests.post("http://localhost:8765", json=payload)
        resultado = resposta.json()

        if resultado.get("error"):
            logger.error(f"Erro ao criar cartao {numero_cartao}: {resultado['error']}")
            return False
        else:
            logger.card_details(numero_cartao, len(frente), frente_txt, verso_txt, audio_file)
            return True

    except requests.exceptions.ConnectionError:
        logger.error(f"Erro de conexão no cartao {numero_cartao}: verifique se o Anki está aberto")
        return False
    except Exception as e:
        return False

def main():
    logger.header("ENVIANDO CARTÕES PARA ANKI")

    try:
        # Lê os dados diretamente do Excel
        frente, verso, _ = ler_dados_excel()
        audios = preparar_audios()

        if len(frente) != len(verso):
            logger.error("ERRO: As listas têm tamanhos diferentes!")
            return

        if len(frente) != len(audios):
            logger.info(f"Ajustando lista de áudios para corresponder às frases...")
            audios = audios[:len(frente)]

        logger.info(f"Cartões a processar: {len(frente)}")

        # Copia os arquivos de áudio para a pasta do Anki
        if not copiar_arquivos_audio(audios):
            raise Exception("Falha ao copiar arquivos de áudio")

        # Cria os cartões
        cartoes_adicionados = 0
        for i in range(len(frente)):
            tentativas = 0
            sucesso = False
            max_tentativas = 3

            while tentativas < max_tentativas and not sucesso:
                tentativas += 1
                sucesso = adicionar_cartao_anki(frente[i], verso[i], audios[i], baralho_anki, numero_cartao=i+1)
                if not sucesso and tentativas < max_tentativas:
                    time.sleep(2)
                audio_nome = ""
                if audios[i].startswith("[sound:") and audios[i].endswith("]"):
                    audio_nome = os.path.basename(audios[i][7:-1].strip())

                logger.card_details(i+1, len(frente), frente[i], verso[i], audio_nome)

            if sucesso:
                cartoes_adicionados += 1

        logger.success(f"Total de cartões adicionados: {cartoes_adicionados}/{len(frente)}")

    except Exception as e:
        logger.error(f"ERRO CRÍTICO: {e}")
        logger.info("Mantendo arquivos de áudio e dados do Excel para recuperação.")

    # Limpa o Excel
    logger.info("Limpando arquivo Excel...")
    if limpar_excel("cartoes.xlsx"):
        logger.success("Excel limpo com sucesso.")
    else:
        logger.error("Falha ao limpar Excel.")

if __name__ == "__main__":
    main()
