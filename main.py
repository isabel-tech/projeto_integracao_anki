import os
import subprocess
import time
from frente import ler_frases
from audio import caminho_dos_audios
import sys

def wait_for_files(directory, prefix, extension, expected_count, timeout=60):
    """Aguarda até que o número esperado de arquivos com o prefixo e extensão exista."""
    start_time = time.time()
    while True:
        files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)]
        print(f"Aguardando... {len(files)}/{expected_count} arquivos encontrados.")
        if len(files) >= expected_count:
            print(f"Encontrados {len(files)} arquivos {prefix}*.{extension}")
            return True
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout: Não foram encontrados {expected_count} arquivos {prefix}*.{extension} em {directory}")
        time.sleep(1)

def run_script(script_name, capture_output=True):
    """Executa um script e retorna True se bem-sucedido, False caso contrário."""
    try:
        print(f"Executando {script_name}...")
        result = subprocess.run(
            [sys.executable, script_name],  # Substitui "python" por sys.executable
            check=True,
            capture_output=capture_output,
            text=True,
            encoding='utf-8',
            errors="ignore"
        )
        if capture_output:
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
    # Lê o número de frases em frente.docx para determinar quantos arquivos MP3 esperar
    frases = ler_frases("frente.docx")
    expected_mp3_count = len(frases)

    # Executa ttmaker.py
    if not run_script("ttmaker.py"):
        print("Falha em ttmaker.py. Abortando.")
        return

    # Aguarda os arquivos MP3 serem baixados
    print("Aguardando arquivos MP3 serem baixados...")
    try:
        wait_for_files(caminho_dos_audios, "ttsmaker-vip-file", ".mp3", expected_mp3_count, timeout=60)
    except TimeoutError as e:
        print(e)
        return

    # Executa audio.py
    if not run_script("audio.py"):
        print("Falha em audio.py. Abortando.")
        return

    # Verifica se audio.docx foi criado
    if not os.path.exists("audio.docx"):
        print("Erro: audio.docx não foi criado por audio.py.")
        return

    # Executa enviar_anki.py
    if not run_script("enviar_anki.py"):
        print("Falha em enviar_anki.py.")
        return

    print("Todos os scripts foram executados com sucesso!")

if __name__ == "__main__":
    try:
        run_scripts()
    except Exception as e:
        print(f"Erro geral: {e}")