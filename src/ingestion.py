import pdfplumber
import re
import nltk
from nltk.tokenize import sent_tokenize

#nltk.download('punkt', quiet=True)
#nltk.download('punkt_tab', quiet=True)


def encontrar_secao(texto, titulo):
    """
    Procura um título de seção ignorando:
    - maiúsculas/minúsculas
    - espaços extras
    - numeração antes do título (2, 2.1, 2.1.3, etc.)
    """

    padrao = (
        r'(?:^|\n)\s*'
        r'(?:\d+(?:\.\d+)*)?\s*'
        + re.escape(titulo)
        + r'\s*'
    )

    return re.search(
        padrao,
        texto,
        flags=re.IGNORECASE | re.MULTILINE
    )

def extrair_e_limpar_pdf(caminho_pdf, texto_inicio=None, texto_fim=None):
    texto_completo = ""

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()

            if texto:
                texto_completo += texto + "\n"

    # Recorta o início
    if texto_inicio:
        match_inicio = encontrar_secao(
            texto_completo,
            texto_inicio
        )

        if match_inicio:
            texto_completo = texto_completo[match_inicio.start():]
        else:
            print(
                f"Aviso: seção '{texto_inicio}' não encontrada."
            )

    # Recorta o fim
    if texto_fim:
        match_fim = encontrar_secao(
            texto_completo,
            texto_fim
        )

        if match_fim:
            texto_completo = texto_completo[:match_fim.start()]
        else:
            print(
                f"Aviso: seção '{texto_fim}' não encontrada."
            )

    texto_limpo = re.sub(r'(?i)página\s*\d+', '', texto_completo) #Remove paginação
    texto_limpo = re.sub(r'-\n', '', texto_limpo)                 #Remove hifenização
    texto_limpo = re.sub(r'\n', ' ', texto_limpo)                 #Remove quebras de linha
    texto_limpo = re.sub(r'\s{2,}', ' ', texto_limpo)             #Remove espaços duplos

    sentencas = sent_tokenize(texto_limpo, language='portuguese')

    sentencas = [s.strip() for s in sentencas if len(s.split()) > 3]

    return sentencas