from docx import Document

# Lê as frases do docx
def ler_frases(path):
    doc = Document(path)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]
