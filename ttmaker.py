from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from frente import ler_dados_excel
import time
import os
import glob
from config import email_tts, senha_tts, caminho_dos_audios

def obter_audios_existentes():
    """Retorna lista de arquivos MP3 existentes antes da operação"""
    return set(glob.glob(os.path.join(caminho_dos_audios, "*.mp3")))

def limpar_apenas_novos_audios(audios_existentes_inicio):
    """Remove apenas os áudios criados durante a operação"""
    try:
        # DEBUG: Verificar o que temos
        print(f"Áudios existentes no início: {len(audios_existentes_inicio)}")
        
        audios_atuais = set(glob.glob(os.path.join(caminho_dos_audios, "*.mp3")))
        print(f"Áudios atuais: {len(audios_atuais)}")
        
        novos_audios = audios_atuais - audios_existentes_inicio
        print(f"Novos áudios a serem removidos: {len(novos_audios)}")
        
        # DEBUG: Listar os arquivos
        print("Áudios existentes no início:")
        for audio in sorted(audios_existentes_inicio):
            print(f"  - {os.path.basename(audio)}")
        
        print("Áudios atuais:")
        for audio in sorted(audios_atuais):
            print(f"  - {os.path.basename(audio)}")
        
        print("Áudios a serem removidos:")
        for arquivo in novos_audios:
            print(f"  - {os.path.basename(arquivo)}")

        for arquivo in novos_audios:
            try:
                os.remove(arquivo)
                print(f"Removido: {os.path.basename(arquivo)}")
            except Exception as e:
                print(f"Erro ao remover {arquivo}: {e}")
        
        print(f"Áudios da operação removidos. {len(novos_audios)} arquivos deletados.")
        return True
    except Exception as e:
        print(f"Erro ao limpar áudios: {e}")
        return False

def main():
    """Função principal para ser chamada pelo main.py"""
    # Guarda os áudios existentes antes de começar
    audios_existentes_inicio = obter_audios_existentes()
    sucesso_operacao = False  # Flag para controlar se a operação foi bem-sucedida
    driver = None  # Definir driver como None no início

    print("Iniciando o script!")

    try:
        frente, verso, audios = ler_dados_excel()
        frases_em_ingles = frente

        if not frases_em_ingles:
            print("Nenhuma frase encontrada.")
            return False

        # Configurações para download
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        chrome_options.add_argument("--log-level=3")  # SILENCIA TODOS OS LOGS
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        os.environ['WDM_LOG_LEVEL'] = '0'
        os.environ['WDM_PRINT_FIRST_LINE'] = 'False'

        # Configura o download para a pasta específica
        prefs = {
            "download.default_directory": caminho_dos_audios,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # INICIALIZAÇÃO COM SELENIUM COMUM
        service = Service(ChromeDriverManager().install())
        
        service.creationflags = 0x08000000  # Silencia processos do Windows

        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get("https://pro.ttsmaker.com/user/login")
        
        # Preenche email e senha
        email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="you@email.com"]')))
        email_input.send_keys(email_tts)
        password_input = driver.find_element(By.ID, "password-vue-id")
        password_input.send_keys(senha_tts)

        # Clica em "Sign In"
        button_sign_in = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Sign in"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_sign_in)
        button_sign_in.click()

        # Clica em "Open Studio"
        button_open_studio = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[1]/div/div/div[2]/a'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_open_studio)
        button_open_studio.click()

        # Loop para converter e baixar cada frase
        for i, frase in enumerate(frases_em_ingles, 1):
            try:                
                caixa_texto = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "UserInputTextarea"))
                )
                time.sleep(1)
                # Coloca a frase no campo
                caixa_texto.clear()
                caixa_texto.send_keys(frase)

                # Espera o "toast" sair da frente, se existir
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, 'toast-message'))
                )
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "toast-info"))
                )
                
                # Clica no botão de conversão
                time.sleep(5)
                button_convert = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, 'tts_order_submit'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_convert)
                button_convert.click()
                time.sleep(5)
                
                # Clica no botão de download
                button_download = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, 'tts_mp3_download_btn'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_download)
                button_download.click()
                time.sleep(5)
                
                # Espera o download
                timeout = 30
                start_time = time.time()
                while True:
                    arquivos = os.listdir(caminho_dos_audios)
                    mp3s = [f for f in arquivos if f.endswith(".mp3")]
                    if mp3s:
                        break
                    if time.time() - start_time > timeout:
                        print("Timeout no download do áudio")
                        break
                    time.sleep(1)
                
                time.sleep(5)
                
            except Exception as e:
                print(f"Erro ao processar frase {i}: {e}")
                print("Continuando para a próxima frase...")
                continue

        print("Todos os áudios baixados com sucesso!")
        sucesso_operacao = True  # Marca que a operação foi bem-sucedida
        return True

    except Exception as e:
        print(f" Erro durante a execução: {e}")
        sucesso_operacao = False
        return False

    finally:
        # FECHAMENTO CORRETO COM SELENIUM COMUM
        if driver is not None:
            try:
                driver.quit()
                print("Navegador fechado com sucesso!")
            except Exception as e:
                print(f"Erro ao fechar navegador: {e}")
        
        

# Para executar diretamente
if __name__ == "__main__":
    main()