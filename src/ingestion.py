import pdfplumber
import re
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

def extrair_e_limpar_pdf(caminho_pdf):
    texto_completo = ""
    
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + " "
                
    texto_limpo = re.sub(r'(?i)página\s*\d+', '', texto_completo) # Remove paginação
    texto_limpo = re.sub(r'-\n', '', texto_limpo)                 # Remove hifenização
    texto_limpo = re.sub(r'\n', ' ', texto_limpo)                 # Remove quebras de linha
    texto_limpo = re.sub(r'\s{2,}', ' ', texto_limpo)             # Remove espaços duplos
    
    # Segmentação
    sentencas = sent_tokenize(texto_limpo, language='portuguese')
    
    # Filtro de ruído (frases muito curtas)
    sentencas = [s.strip() for s in sentencas if len(s.split()) > 3]
    
    return sentencas