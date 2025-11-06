import os
import pandas as pd

print("=== DIAGNÓSTICO DO SISTEMA ===")

# Verifica se o arquivo existe
arquivo_excel = "cartoes.xlsx"
print(f"📁 Arquivo Excel existe: {os.path.exists(arquivo_excel)}")

if os.path.exists(arquivo_excel):
    try:
        df = pd.read_excel(arquivo_excel)
        print(f"✅ Excel pode ser lido")
        print(f"📊 Colunas: {df.columns.tolist()}")
        print(f"📝 Número de linhas: {len(df)}")
        
        # Verifica frases na coluna Frente
        frases = df['Frente'].dropna().tolist()
        print(f"🎯 Frases encontradas: {len(frases)}")
        
        for i, frase in enumerate(frases, 1):
            print(f"  {i}. {frase}")
            
    except Exception as e:
        print(f"❌ Erro ao ler Excel: {e}")
else:
    print("❌ Arquivo cartoes.xlsx não encontrado!")
    print("💡 Certifique-se de que:")
    print("   - O arquivo está na mesma pasta do script")
    print("   - O nome está correto: cartoes.xlsx")
    print("   - Não está aberno no Excel")