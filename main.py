import os
import subprocess
import time
from frente import ler_dados_excel  # Já está correto
from audio import caminho_dos_audios
import sys

def wait_for_files(directory, prefix, extension, expected_count, timeout=60):
    start_time = time.time()
    while True:
        files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)]
        if len(files) >= expected_count:
            return True
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout: Não foram encontrados {expected_count} arquivos {prefix}*.{extension} em {directory}")
        time.sleep(1)

def run_script(script_name, capture_output=True):
    try:
        print(f"Executando {script_name}...")
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=capture_output,
            text=True
        )
        if capture_output:
            if result.stdout:
                print(f"Saída de {script_name}:\n{result.stdout}")
            if result.stderr:
                print(f"Erros de {script_name}:\n{result.stderr}")
        print(f"{script_name} concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro em {script_name}:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"Erro inesperado em {script_name}: {e}")
        return False

def run_scripts():
    # Lê o número de frases do Excel (NÃO MAIS DO DOCX)
    frente, verso, audios = ler_dados_excel()
    expected_mp3_count = len(frente)
    
    print(f"Encontradas {expected_mp3_count} frases")

    # Executa ttmaker.py
    if not run_script("ttmaker.py"):
        print("Falha em ttmaker.py. Abortando.")
        return

    # Aguarda os arquivos MP3 serem baixados
    try:
        wait_for_files(caminho_dos_audios, "ttsmaker-vip-file", ".mp3", expected_mp3_count)
    except TimeoutError as e:
        print(e)
        return

    # Executa audio.py
    if not run_script("audio.py"):
        print("Falha em audio.py. Abortando.")
        return

    # VERIFICAÇÃO REMOVIDA: Não precisa mais verificar audio.docx
    # O audio.py agora trabalha diretamente com os arquivos MP3

    # Executa enviar_anki.py
    if not run_script("enviar_anki.py"):
        print("Falha em enviar_anki.py.")
        return

    print("Todos os scripts foram executados com sucesso!")


if __name__ == "__main__":
    try:
        # Verifica se o arquivo Excel existe
        if not os.path.exists("cartoes.xlsx"):
            print("Arquivo 'cartoes.xlsx' não encontrado!")
            print("Crie o arquivo Excel com as colunas 'Frente' e 'Verso'")
        else:
            run_scripts()
    except Exception as e:
        print(f"Erro geral: {e}")