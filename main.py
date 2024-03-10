import pdfplumber
import tabula
import os
import threading
import json
import warnings

warnings.filterwarnings("ignore")

def main():
    """Chama a funcao para encontrar os pdf e inicia as threads para processar esses pdfs e finalmente salva os dados em um arquivo json."""
    dados = {}
    threads = []
    pdf_files = get_files()

    for file in pdf_files:
        thread = threading.Thread(target=start_functions, args=(dados , file))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    with open('dados.json', 'w') as arquivo_json:
        json.dump(dados, arquivo_json)
    return dados

def start_functions(dados, file, semaphore=threading.Semaphore(8)):
    """Chama as funcoes para processar o pdf e salva o texto em um dicionario. em no maximo 8 por vez"""
    with semaphore:
        print('Processando arquivo: ', file)
        bolds, text_file = get_text_and_bold(file)
        second_paragraph = get_secund_paragraph(bolds)
        texto = text_file.split('EXECUTIVE SUMMARY')[1].split(second_paragraph)[0]
        file = file.replace('pdfs/','')
        dados[file] = texto.strip()

def get_files():
    """Retorna uma lista com os nomes dos arquivos PDF no diretório pdfs."""
    pdf_files = []
    for file in os.listdir('pdfs'):
        if file.endswith('.pdf'):
            pdf_files.append('pdfs/' + file)

    if not pdf_files:
        raise ValueError("Nenhum arquivo PDF encontrado no diretório atual.")   
    print('Arquivos encontrados: ', pdf_files) 
    return pdf_files

def get_secund_paragraph(bolds):
    """Retorna o titulo do segundo parágrafo do PDF. Para fazer o split do texto posteriormente."""
    index = bolds.index('EXECUTIVE SUMMARY')
    bolds = bolds[index + 1:]

    for word in bolds:
        word_ = word.replace('’s', '')
        if word_.isupper():
            return word
        
    return bolds[0]

def get_text_and_bold(pdf_path):
    """Retorna uma lista com as palavras em negrito do PDF. além do texto do PDF."""
    negrito = []
    texto_final = ''
           
    with pdfplumber.open(pdf_path) as pdf: 
        for i, page in enumerate(pdf.pages):
            texto_tabela = ''
            if i == 10:
                break
            texto_pagina = page.extract_text()

            # pega as tabelas do pdf e remove do texto
            tabelas = tabula.read_pdf(pdf_path,pages= i+1, multiple_tables=True, stream=True)
            for tabela in tabelas:
                try:
                    header = [word for word in tabela.columns if 'Unnamed' not in word]
                    header = ' '.join(header)
                    dados = tabela.to_string(index=False).replace('NaN', '').replace('  ',' ')
                    ultimos = dados[-25:]
                    inicio = header[:20]
                    tabela_ultimos = texto_pagina.split(ultimos)[0] + ultimos
                    tabela_incio = tabela_ultimos.split(inicio)[1]
                    texto_tabela = inicio + tabela_incio
                    texto_pagina = texto_pagina.replace(texto_tabela, '')
                except:
                    for _, row in tabela.iterrows():
                        for cell in row:
                            texto_pagina= texto_pagina.replace(str(cell), '')

            texto_pagina = remove_header_footer(texto_pagina)
            texto_final += texto_pagina

            # pega as palavras em negrito do pdf, exceto as que estão na tabela
            clean_text = page.filter(lambda obj: obj["object_type"] == "char" and "Bold" in obj["fontname"])
            palavras = clean_text.extract_text()
            negrito += [palavra for palavra in palavras.split('\n') if palavra not in texto_tabela]

    return negrito, texto_final

#funcao auxiliar
def remove_header_footer(texto):
    """Remove o cabeçalho e rodapé do PDF."""
    texto = texto.split('\n')
    if 'Page' in texto[-1]:
        texto = texto[1:len(texto)-1]
    else:
        texto = texto[1:]

    texto = ' '.join(texto)
    texto = texto.encode('ascii', errors='ignore').decode('ascii')

    return texto
    
if __name__ == "__main__":
    main()