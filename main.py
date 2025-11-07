import os
import subprocess
import time
from frente import ler_dados_excel
from audio import caminho_dos_audios
import sys
from ttmaker import obter_audios_existentes, limpar_apenas_novos_audios 

class Logger:
    def __init__(self):
        self.width = 80
        
    def header(self, title):
        print(f"\n{'=' * self.width}")
        print(f"{title:^{self.width}}")
        print(f"{'=' * self.width}")
    
    def section(self, title):
        print(f"\n{title}")
        print('-' * self.width)
    
    def info(self, message):
        print(f"[INFO] {message}")
    
    def success(self, message):
        print(f"[SUCCESS] {message}")
    
    def error(self, message):
        print(f"[ERROR] {message}")

logger = Logger()

def wait_for_files(directory, prefix, extension, expected_count, timeout=60):
    start_time = time.time()
    while True:
        files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)]
        if len(files) >= expected_count:
            return True
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout: Nao foram encontrados {expected_count} arquivos {prefix}*.{extension} em {directory}")
        time.sleep(1)

def run_script(script_name, capture_output=True):
    try:
        logger.info(f"Executando {script_name}...")
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=capture_output,
            text=True
        )
        if capture_output and result.stdout:
            print(f"Saída de {script_name}:")
            print(result.stdout)
        if capture_output and result.stderr:
            logger.error(f"Erros de {script_name}: {result.stderr}")
        logger.success(f"{script_name} concluído!")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro em {script_name}: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado em {script_name}: {e}")
        return False

def run_scripts():
    logger.header("INÍCIO DA AUTOMAÇÃO ANKI")
    
    # Captura o estado inicial dos áudios
    audios_existentes_inicio = obter_audios_existentes()
    
    # Lê o número de frases do Excel
    frente, verso, audios = ler_dados_excel()
    expected_mp3_count = len(frente)
    
    logger.section("ESTATISTÍCAS INICIAIS")
    logger.info(f"Frases encontradas: {expected_mp3_count}")

    logger.section("EXECUÇÃO DOS SCRIPTS")

    # Executa ttmaker.py
    if not run_script("ttmaker.py"):
        logger.error("Falha em ttmaker.py. Abortando.")
        return

    # Aguarda os arquivos MP3 serem baixados
    try:
        logger.info("Aguardando download dos arquivos MP3...")
        wait_for_files(caminho_dos_audios, "ttsmaker-vip-file", ".mp3", expected_mp3_count)
        logger.success("Todos os arquivos MP3 baixados com sucesso!")
    except TimeoutError as e:
        logger.error(str(e))
        return

    # Executa audio.py
    if not run_script("audio.py"):
        logger.error("Falha em audio.py. Abortando.")
        return

    # Executa enviar_anki.py
    if not run_script("enviar_anki.py"):
        logger.error("Falha em enviar_anki.py.")
        return

    logger.section("LIMPEZA FINAL")
    logger.info("Removendo audios criados durante a automacao...")
    if limpar_apenas_novos_audios(audios_existentes_inicio):
        logger.success("Áudios temporários removidos com sucesso!")
    else:
        logger.error("Falha ao remover audios temporarios.")

    logger.header("AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")

if __name__ == "__main__":
    try:
        if not os.path.exists("cartoes.xlsx"):
            logger.error("Arquivo 'cartoes.xlsx' nao encontrado!")
            logger.info("Crie o arquivo Excel com as colunas 'Frente' e 'Verso'")
        else:
            run_scripts()
    except Exception as e:
        logger.error(f"Erro geral: {e}")