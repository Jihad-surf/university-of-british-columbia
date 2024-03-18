import re
import pandas as pd
from collections import Counter


def read_keywords():
    """ Read the keywords from the excel file and return a list of keywords """
    df = pd.read_excel('Key words.xlsx', header=None)
    key_words = df.values.flatten().tolist()
    key_words = [str(word).lower() for word in key_words if str(word) != 'nan']
    return key_words

def count_keywords(text):
    """ Count the number of times each keyword appears in the text """
    key_words = read_keywords()

    count = Counter()
    for word in key_words:
        count[word] = len(re.findall(r'\b' + word + r'\b', text, re.IGNORECASE))

    count_filt = Counter({chave: valor for chave, valor in count.items() if valor > 0})

    return count_filt
