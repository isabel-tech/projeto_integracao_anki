import requests
import time
import os
import shutil
import pandas as pd
from docx import Document
from audio import frente, verso, audios
from config import caminho_midia_anki, baralho_anki
from ttmaker import limpar_apenas_novos_audios, obter_audios_existentes
import glob
from audio import caminho_dos_audios
def limpar_excel(caminho_excel):
    """Limpa as colunas Frente e Verso do Excel após a execução"""
    try:
        df = pd.read_excel(caminho_excel)
        df['Frente'] = ''
        df['Verso'] = ''
        df.to_excel(caminho_excel, index=False)
        print(f"Colunas 'Frente' e 'Verso' limpas no arquivo: {caminho_excel}")
    except Exception as e:
        print(f"Erro ao limpar Excel: {e}")
        
def copiar_arquivos_audio():
    """Copia apenas os arquivos de áudio necessários"""
    try:
        arquivos_copiados = 0
        for i, audio_tag in enumerate(audios):
            if audio_tag.startswith("[sound:") and audio_tag.endswith("]"):
                source_path = audio_tag[7:-1].strip()
                audio_file = os.path.basename(source_path)
                dest_path = os.path.join(caminho_midia_anki, audio_file)
                
                if os.path.exists(source_path):
                    try:
                        shutil.copy2(source_path, dest_path)
                        arquivos_copiados += 1
                    except Exception as e:
                        print(f"Erro ao copiar {audio_file}: {e}")
                else:
                    print(f"Arquivo não encontrado: {source_path}")
        
        print(f"Total de arquivos copiados: {arquivos_copiados}")
        return True
    except Exception as e:
        print(f"Erro ao copiar arquivos de áudio: {e}")
        return False

def adicionar_cartao_anki(frente_txt, verso_txt, audio_tag, baralho_anki, numero_cartao=0):
    try:
        # Extrai apenas o nome do arquivo
        if audio_tag.startswith("[sound:") and audio_tag.endswith("]"):
            source_path = audio_tag[7:-1].strip()
            audio_file = os.path.basename(source_path)
        else:
            audio_file = ""

        # Monta o campo Frente com o áudio incluído como texto
        campo_frente = f"{frente_txt}"
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
                    "options": {
                        "allowDuplicate": False
                    },
                    "tags": ["automatica"]
                }
            }
        }

        # Envia a requisição
        resposta = requests.post("http://localhost:8765", json=payload)
        resultado = resposta.json()
        
        if "error" in resultado and resultado["error"]:
            print(f"Erro ao criar cartão {numero_cartao}: {resultado['error']}")
            return False
        else:
            print("-" * 65)
            print(f"Frente: {frente_txt}")
            print(f"Verso: {verso_txt}")
            print(f"Audio: {audio_file}")
            print("-" * 65)
            return True
            
    except requests.exceptions.ConnectionError:
        print(f"Erro de conexão no cartão {numero_cartao}: Verifique se o Anki está aberto")
        return False
    except Exception as e:
        print(f"Erro inesperado no cartão {numero_cartao}: {e}")
        return False

try:
    audios_existentes_inicio = obter_audios_existentes()
    print(f"Áudios existentes antes da operação: {len(audios_existentes_inicio)}")
    # PRIMEIRO: Verifica os dados
    print("=== INICIANDO PROCESSO ===")
    print(f"Cartões a processar: {len(frente)}")
    print(f"Versos disponíveis: {len(verso)}") 
    print(f"Áudios disponíveis: {len(audios)}")

    # Verifica se as listas têm o mesmo tamanho
    if len(frente) != len(verso) :
        print("ERRO: As listas têm tamanhos diferentes!")
        print(f"Frente: {len(frente)}, Verso: {len(verso)}, Áudios: {len(audios)}")
        raise Exception("Listas com tamanhos inconsistentes")

    # DEPOIS: Copia os arquivos de áudio
    if not copiar_arquivos_audio():
        raise Exception("Falha ao copiar arquivos de áudio")

    # FINALMENTE: Cria os cartões
    cartoes_adicionados = 0

    # Usando um loop while com índice manual para melhor controle
    i = 0
    while i < len(frente):
        print(f"\nProcessando cartão {i+1} de {len(frente)}:")
        
        sucesso = adicionar_cartao_anki(
            frente[i], 
            verso[i], 
            audios[i], 
            baralho_anki, 
            numero_cartao=i+1
        )
        
        if sucesso:
            cartoes_adicionados += 1
            i += 1  # Só avança para o próximo se foi bem-sucedido
        else:
            print(f"Tentando novamente o cartão {i+1} após 2 segundos...")
            time.sleep(2)  # Espera 2 segundos antes de tentar novamente
            # Não incrementa i, então tenta o mesmo cartão novamente

    print(f"\nProcesso concluído! {cartoes_adicionados} cartões adicionados com sucesso.")

    # SÓ LIMPA SE TUDO DEU CERTO
    if cartoes_adicionados == len(frente):
        limpar_excel("cartoes.xlsx")
        print("Excel limpo com sucesso.")

        # === AQUI: REMOVE APENAS OS ÁUDIOS NOVOS (gerados nesta execução) ===
        print("Removendo áudios temporários gerados...")
        limpar_apenas_novos_audios(audios_existentes_inicio)
        print("Áudios temporários removidos com sucesso.")
    else:
        print(f"Apenas {cartoes_adicionados} de {len(frente)} cartões foram adicionados.")
        print("Mantendo áudios e dados do Excel para recuperação.")

except Exception as e:
    print(f"ERRO CRÍTICO: {e}")
    print("Mantendo arquivos de áudio e dados do Excel para recuperação.")
    print("Execute novamente após resolver o problema.")
    
    

