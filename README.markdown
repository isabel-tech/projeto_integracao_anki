# Projeto Anki TTS Automator

## Descrição
O **Anki TTS Automator** é um projeto em Python que automatiza a criação de cartões no Anki para aprendizado de idiomas. Ele realiza as seguintes etapas:
1. Lê frases em inglês e suas traduções em português de arquivos `.docx`.
2. Converte as frases em inglês em áudio usando o serviço TTSMaker.
3. Renomeia e organiza os arquivos de áudio gerados.
4. Integra os áudios e as frases em um formato compatível com o Anki.
5. Adiciona os cartões ao Anki via AnkiConnect.
6. Limpa os arquivos temporários após a conclusão.

O projeto é composto por quatro scripts principais: `frente.py`, `ttmaker.py`, `audio.py` e `enviar_anki.py`, com um script orquestrador `main.py` que coordena a execução.

## Requisitos
- **Python 3.8+**
- **Bibliotecas Python**:
  ```bash
  pip install python-docx selenium webdriver-manager undetected-chromedriver requests
  ```
- **Google Chrome** instalado.
- **Anki** instalado com o plugin **AnkiConnect** ativado.
- **Conta no TTSMaker** (para conversão de texto em áudio).
- **Arquivos de entrada**:
  - `frente.docx`: Contém as frases em inglês.
  - `verso.docx`: Contém as traduções correspondentes em português.
  - `audio.docx`: É inicialmente um arquivo em branco que será usado para armazenar os áudios.
- **Configurações**:
  - Atualize os caminhos de diretórios (`caminho_dos_audios` e `caminho_midia_anki`) nos scripts `audio.py` e `enviar_anki.py` para corresponder ao seu sistema.
  - Atualize as credenciais de login do TTSMaker (email e senha) em `ttmaker.py`.
  - Atualize o nome do baralho do Anki em `enviar_anki.py`, se necessário.

## Estrutura do Projeto
- **`frente.py`**: Contém a função `ler_frases` para ler parágrafos de arquivos `.docx`.
- **`ttmaker.py`**: Usa Selenium com `undetected-chromedriver` para:
  - Fazer login no TTSMaker.
  - Inserir frases de `frente.docx` no campo de texto.
  - Converter as frases em áudio e baixá-las como arquivos MP3.
- **`audio.py`**: Organiza os arquivos MP3 baixados:
  - Renomeia os arquivos para um formato sequencial (ex.: `ttsmaker-vip-file-1.mp3`).
  - Cria um arquivo `audio.docx` com tags de áudio no formato `[sound:nome_do_arquivo.mp3]`.
  - Copia os arquivos MP3 para a pasta de mídia do Anki.
- **`enviar_anki.py`**: Integra as frases de `frente.docx`, `verso.docx` e `audio.docx`:
  - Cria cartões no Anki via AnkiConnect, vinculando áudios ao campo "Frente".
  - Limpa os arquivos `.docx` após a criação dos cartões.
- **`main.py`**: Orquestra a execução dos scripts na ordem correta e aguarda a conclusão dos downloads.

## Como Usar
1. **Configuração Inicial**:
   - Instale as dependências listadas em **Requisitos**.
   - Configure os caminhos de diretórios e credenciais nos scripts conforme descrito.
   - Certifique-se de que o Anki está aberto com o AnkiConnect ativo (porta padrão: 8765).
   - Prepare os arquivos `frente.docx` e `verso.docx` com frases correspondentes(não se esqueça de fechar esses arquivos antes de rodar o código).

2. **Execução**:
   - Coloque todos os scripts e arquivos `.docx` no mesmo diretório.
   - Execute o script principal:
     ```bash
     python main.py
     ```
   - O script executará automaticamente `ttmaker.py`, `audio.py` e `enviar_anki.py` na ordem correta.

3. **Saída**:
   - Os cartões serão adicionados ao baralho especificado no Anki.
   - Os arquivos MP3 serão movidos para a pasta de mídia do Anki.
   - Os arquivos `.docx` serão limpos, e os arquivos MP3 temporários serão removidos.

## Observações
- **AnkiConnect**: Certifique-se de que o Anki está aberto e o AnkiConnect está configurado para aceitar conexões na porta 8765.
- **TTSMaker**: O script assume que você tem uma conta válida no TTSMaker. Algumas funcionalidades podem exigir uma conta VIP.
- **Sistema de Arquivos**: Ajuste os caminhos de diretórios (`caminho_dos_audios` e `caminho_midia_anki`) para corresponder ao seu sistema operacional e configuração do Anki.
- **Erro de Timeout**: Se os arquivos MP3 não forem baixados dentro do tempo limite (60 segundos por padrão), o script será interrompido. Verifique sua conexão com a internet ou aumente o tempo limite em `main.py`.


## Licença
Este projeto é fornecido como está, sem garantias. Use por sua conta e risco. 


##
**"Confie no Senhor de todo o seu coração e não se apoie em seu próprio entendimento; reconheça-o em todos os seus caminhos, e Ele dirigirá seus passos." (Provérbios 3:5-6)**