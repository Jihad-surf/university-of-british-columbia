import pdfplumber
from scripts.executive_summary import get_files
import re
import threading

def start_get_texts():
    """ roda a função get_texts em paralelo para todos os arquivos pdfs"""
    texts = {}
    threads = []
    pdf_files = get_files()

    for file in pdf_files:
        thread = threading.Thread(target=get_texts, args=(texts , file))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    return texts


def get_texts(texts, file, semaphore=threading.Semaphore(8)):
    """ Extrai o texto de um arquivo pdf e o armazena em um dicionário"""
    with semaphore:
        texto_pagina = ''
        with pdfplumber.open(file) as pdf: 
            for page in pdf.pages:
                texto_pagina += page.extract_text()


        texto = tratar_texto(texto_pagina)
        file = file.replace('pdfs/','').replace('.pdf','').encode('ascii', errors='ignore').decode('ascii') 

        texts[file] = texto

def tratar_texto(texto):
    """ Remove caracteres especiais, números, pontuações"""
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = texto.lower()
    texto = texto.replace('\n', ' ').strip()
    texto = texto.encode('ascii', errors='ignore').decode('ascii')
    return texto