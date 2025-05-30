from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from frente import ler_frases
from config import email_tts, senha_tts
import undetected_chromedriver as uc
import time

print("Iniciando o script!")

frases_em_ingles = ler_frases("frente.docx")
if not frases_em_ingles:
    print("Nenhuma frase encontrada.")
    exit()

# Configurações para download
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions") 

servico = Service(ChromeDriverManager().install())
driver = None 

try:
    driver = uc.Chrome(options=chrome_options)
    driver.get("https://pro.ttsmaker.com/user/login")
	# Preenche email e senha
    email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="you@email.com"]')))
    email_input.send_keys(email_tts) # Mude para o seu email
    password_input = driver.find_element(By.ID, "password-vue-id")
    password_input.send_keys(senha_tts) # Mude para a sua senha

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
        print(f"Processando frase {i}: {frase}")
        caixa_texto = WebDriverWait(driver, 20).until(
			EC.presence_of_element_located((By.ID, "UserInputTextarea"))
		)
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
        time.sleep(5)
		# Clica no botão de conversão
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
        print("Botão de download clicado com sucesso!")
        time.sleep(1)
        
except Exception as e:
    print("Erro durante a execução:", e)

finally:
    if driver:
        try:
            driver.quit()  # fecha o driver explicitamente
        except Exception as e:
            print("Erro ao tentar fechar o driver:", e)

print("Finalizado com sucesso!")