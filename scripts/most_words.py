import re
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import pandas as pd
from .key_words import read_keywords

# Download de recursos do nltk caso não estejam disponíveis
try:
    if not(nltk.data.find('tokenizers/punkt')):
        nltk.download('punkt')
    if not(nltk.data.find('corpora/stopwords')):
        nltk.download('stopwords')

except:
    nltk.download('punkt')
    nltk.download('stopwords')
    
def more_stopwords():
    """ Retorna uma lista de stop words adicionais """
    df = pd.read_excel('stop_words.xlsx', header=None)
    stop_words = df.values.flatten().tolist()
    stop_words = [str(word).lower() for word in stop_words if str(word) != 'nan']
    return stop_words

def obter_palavras_frequentes(texto, top_n=3):
    # Tokenização e remoção de pontuações
    palavras = word_tokenize(re.sub(r'[^\w\s]', '', texto.lower()))

    # Remoção de stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.update(more_stopwords())
    stop_words.update(read_keywords())
    palavras_filtradas = []
    for palavra in palavras:
        if palavra not in stop_words and len(palavra) > 1 and not palavra.isdigit():
            palavras_filtradas.append(palavra)

    contagem_palavras = Counter(palavras_filtradas)
    top_palavras = contagem_palavras.most_common(top_n)

    return top_palavras
