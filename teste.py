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

def limpar_apenas_novos_audios(audios_existentes):
    """Remove apenas os áudios criados durante a operação"""
    try:
        audios_atuais = set(glob.glob(os.path.join(caminho_dos_audios, "*.mp3")))
        novos_audios = audios_atuais - audios_existentes
        
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

    print("Iniciando o script!")

    try:
        frente, verso, audios = ler_dados_excel()
        frases_em_ingles = frente

        if not frases_em_ingles:
            print("Nenhuma frase encontrada.")
            return False

        # CONFIGURAÇÕES COM SELENIUM COMUM
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions") 

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
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get("https://pro.ttsmaker.com/user/login")
        
        # ... TODO O RESTO DO SEU CÓDIGO PERMANECE IGUAL ...
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

        # ... resto do seu código igual ...

        print(" Todos os áudios baixados com sucesso!")
        sucesso_operacao = True
        return True

    except Exception as e:
        print(f" Erro durante a execução: {e}")
        sucesso_operacao = False
        return False

    finally:
        if 'driver' in locals() and driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Erro ao tentar fechar o driver: {e}")
        
        if sucesso_operacao:
            print("Operação bem-sucedida. Limpando áudios temporários...")
            limpar_apenas_novos_audios(audios_existentes_inicio)
        else:
            print("Operação com problemas. Mantendo áudios para debug.")

if __name__ == "__main__":
    main()