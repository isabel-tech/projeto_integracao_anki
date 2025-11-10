# Anki TTS Automator (Excel + TTSMaker + AnkiConnect)

## Descrição do Projeto

Este projeto automatiza a criação de cartões no **Anki** a partir de um arquivo Excel (`cartoes.xlsx`), convertendo frases em inglês em áudio com o **TTSMaker**, copiando os arquivos para a pasta de mídia do Anki e enviando os cartões via **AnkiConnect**.

Ideal para quem estuda idiomas com **repetição espaçada** e quer **áudio nativo** em cada cartão.

---

## Funcionalidades

- Lê frases de um arquivo `cartoes.xlsx` (colunas: `Frente`, `Verso`)
- Faz login automático no [TTSMaker](https://pro.ttsmaker.com)
- Converte cada frase em áudio MP3
- Renomeia e organiza os arquivos baixados
- Copia áudios para a pasta de mídia do Anki
- Cria cartões no Anki com áudio embutido no campo **Frente**
- Limpa o Excel após conclusão
- Tratamento robusto de erros com retentativas

---

## Estrutura de Arquivos

```
.
├── cartoes.xlsx          # Entrada: frases em inglês e português
├── config.py             # Credenciais e caminhos
├── frente.py             # Lê dados do Excel
├── ttmaker.py            # Converte texto em áudio
├── audio.py              # Organiza e copia áudios
├── enviar_anki.py        # Envia cartões ao Anki
└── README.md             # Este arquivo
```

---

## Pré-requisitos

- **Python 3.8+**
- **Bibliotecas Python**:
  ```bash
  pip install python-docx selenium webdriver-manager undetected-chromedriver requests
  ```
- **Google Chrome** instalado.
- **Anki** instalado com o plugin **AnkiConnect** ativado.
- **Conta no TTSMaker** (para conversão de texto em áudio).
- **Arquivos de entrada**:
  - `cartoes.xlsx` : Contém o frente(frases na língua de partida) e verso(frases na língua de destino)
- **Configurações**:
  - Atualize os caminhos de diretórios (`caminho_dos_audios` e `caminho_midia_anki`) nos scripts `audio.py` e `enviar_anki.py` para corresponder ao seu sistema.
  - Atualize as credenciais de login do TTSMaker (email e senha) em `ttmaker.py`.
  - Atualize o nome do baralho do Anki em `enviar_anki.py`, se necessário.

---

## Instalação (VS Code)

1. **Clone ou copie os arquivos** para uma pasta.
2. Abra a pasta no **VS Code**.
3. Abra o terminal integrado (`Ctrl + `` `) e instale as dependências:

```bash
pip install pandas openpyxl selenium webdriver-manager undetected-chromedriver requests
```

---

## Configuração (`config.py`)

Crie um arquivo `config.py` com:

```python
# config.py
email_tts = "seu_email@exemplo.com"
senha_tts = "sua_senha_aqui"

caminho_dos_audios = r"C:\Users\SEU_USUARIO\Downloads"  # Onde os MP3s são baixados
caminho_midia_anki = r"C:\Users\SEU_USUARIO\AppData\Roaming\Anki2\SEU_PERFIL\collection.media"
baralho_anki = "Inglês::Vocabulário"  # Nome exato do baralho no Anki
```

> **Importante**: Ajuste os caminhos para seu sistema.

---

## Formato do `cartoes.xlsx`

| Frente               | Verso                   | 
|----------------------|-------------------------|
| Hello, how are you?  | Olá, como vai?          |                  
| I love programming   | Eu amo programar        |                  

> - Use **apenas uma frase por célula**.  
> - O áudio será gerado automaticamente.

---

## Como Usar
1. **Configuração Inicial**:
   - Instale as dependências listadas em **Requisitos**.
   - Configure os caminhos de diretórios e credenciais nos scripts conforme descrito.
   - Certifique-se de que o Anki está aberto com o AnkiConnect ativo (porta padrão: 8765).
   - Prepare o arquivo `cartoes.xlsx`com frases correspondentes(não se esqueça de fechar esses arquivos antes de rodar o código).

2. **Execução**:
   - Coloque todos os scripts e arquivos `.docx` no mesmo diretório.
   - Execute o script principal:
     ```bash
     python main.py
     ```
   - O script executará automaticamente `ttmaker.py`, `audio.py` e `enviar_anki.py` na ordem correta.

## Autor

Feito com dedicação e propósito.  
Que cada cartão te aproxime mais do seu objetivo.

> **"Tudo posso naquele que me fortalece." (Filipenses 4:13)**