import pandas as pd

def ler_dados_excel(arquivo_excel="cartoes.xlsx"):
    """Lê os dados do arquivo Excel"""
    df = pd.read_excel(arquivo_excel)
    
    frente = df['Frente'].fillna('').tolist()
    verso = df['Verso'].fillna('').tolist()
    
    # Se tiver coluna de áudio, usa ela, senão cria lista vazia
    if 'Audio' in df.columns:
        audios = df['Audio'].fillna('').tolist()
    else:
        audios = [''] * len(frente)
    
    return frente, verso, audios