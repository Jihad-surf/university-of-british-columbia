import re
from collections import Counter

palavras = ['covid-19', 'animal research', 'animal research activism', 'protest', 'student protest', 'cost of living']

texto_gigante = "Aqui está sua string gigante. protest e Student Protest deveriam contar como uma única palavra. covid 19"

def tratar_texto(texto):
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = texto.lower().replace(' ','')
    return texto

texto_tratado = tratar_texto(texto_gigante)

contagem_palavras = Counter()
for palavra in palavras:
    contagem_palavras[palavra] = texto_tratado.count(tratar_texto(palavra))

# Imprimir o dicionário de contagem
print(contagem_palavras)