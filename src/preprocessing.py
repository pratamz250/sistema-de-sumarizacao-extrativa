import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

#nltk.download('stopwords', quiet=True)

def pre_processar_sentencas(sentencas):
    stop_words = set(stopwords.words('portuguese'))
    stemmer = SnowballStemmer('portuguese')
    
    sentencas_processadas = []
    
    for sentenca in sentencas:
        sentenca_limpa = re.sub(r'[^\w\s]', '', sentenca.lower())
        palavras = sentenca_limpa.split()
        
        palavras_uteis = [
            stemmer.stem(palavra) 
            for palavra in palavras 
            if palavra not in stop_words
        ]
        
        sentencas_processadas.append(" ".join(palavras_uteis))
        
    return sentencas_processadas