import pdfplumber
import tabula
import os
import threading
import json
import warnings
import fitz

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

    novo_dicionario = {chave: {"summary": valor} for chave, valor in dados.items()}
    json_result = json.dumps(novo_dicionario, indent=4)

    with open('dados.json', 'w') as arquivo_saida:
        arquivo_saida.write(json_result)
    return json_result 

def start_functions(dados, file, semaphore=threading.Semaphore(8)):
    """Chama as funcoes para processar o pdf e salva o texto em um dicionario. em no maximo 8 por vez"""
    with semaphore:
        print('Processando arquivo: ', file)
        chave = file.replace('pdfs/','').replace('.pdf','').encode('ascii', errors='ignore').decode('ascii')
        try:
            bolds, text_file = get_text_and_bold(file)
            second_paragraph = get_secund_paragraph(bolds)
            texto = text_file.split('EXECUTIVE SUMMARY')[1].split(second_paragraph)[0]
            dados[chave] = texto.strip()
        except Exception as e:
            print(f'Erro ao processar o arquivo {file}: {e}')
            dados[chave] = 'Erro ao processar o arquivo'

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
            return word.encode('ascii', errors='ignore').decode('ascii')
        
    return bolds[0]


def get_text_and_bold(pdf_path):
    """Retorna uma lista com as palavras em negrito do PDF. além do texto do PDF."""
    negrito = []
    texto_final = ''
    spans_rodape = letra_pequenas(pdf_path)
           
    with pdfplumber.open(pdf_path) as pdf: 
        for i, page in enumerate(pdf.pages):

            spans_rodape_page = [span for span, page_number in spans_rodape if page_number == i]
            texto_tabela = ''

            if i == 10:
                break

            texto_pagina = page.extract_text()
            
            # pega as palavras em negrito do pdf
            clean_text = page.filter(lambda obj: obj["object_type"] == "char" and "Bold" in obj["fontname"])
            palavras = clean_text.extract_text()
            
            # romeve o header 1
            if '\n' in texto_pagina:
                if texto_pagina.split('\n')[0] in palavras:
                    texto_pagina = texto_pagina.split('\n', 1)[1]

            #remove o rodape 1
            for line in texto_pagina.split('\n')[-6:]:
                for valor in spans_rodape_page:
                    if valor.strip() in line:
                        texto_pagina = texto_pagina[:texto_pagina.rfind(valor.strip())]
                        break
                else:
                    continue
                break
            
            # romeve subtextos
            for valir in spans_rodape_page:
                if len(valir) > 24:
                    texto_pagina = texto_pagina.replace(valir, '')

            # pega as tabelas do pdf e remove do texto
            tabelas = tabula.read_pdf(pdf_path,pages= i+1, multiple_tables=True, stream=True)
            for tabela in tabelas:
                try:
                    header = [word for word in tabela.columns if 'Unnamed' not in word]
                    header = ' '.join(header)
                    dados_ = tabela.to_string(index=False).replace('NaN', '').replace('Unnamed: 0', '').replace('Unnamed: 1', '').replace('Unnamed: 2', '')
                    dados = []
                    for linha in dados_.split('\n'):
                        linha = ' '.join(linha.split())
                        dados.append(linha)
                    dados = '\n'.join(dados)
                    ultimos = dados[-15:]
                    inicio = header[:15]
                    if len(inicio) < 14:
                        inicio = dados[:15]

                    # remove o titulo da tabela
                    i = texto_pagina.find(inicio)
                    texto_antes = texto_pagina[:i]

                    if texto_antes.endswith('\n'):
                        texto_antes = texto_antes[:-1]

                    texto_antes = texto_antes.split('\n')
                    if len(texto_antes) > 1:
                        texto_antes = texto_antes[:-1]
                    if len(texto_antes) == 1:
                        texto_antes = ''

                    texto_antes = '\n'.join(texto_antes)
                    texto_dps = texto_pagina[i:]
                    texto_pagina = texto_antes + texto_dps

                    tabela_ultimos = texto_pagina.split(ultimos)[0] + ultimos
                    tabela_incio = tabela_ultimos.split(inicio)[1]
                    texto_tabela = inicio + tabela_incio
                    texto_pagina = texto_pagina.replace(texto_tabela, '')
                except:
                    for _, row in tabela.iterrows():
                        for cell in row:
                            texto_pagina= texto_pagina.replace(str(cell), '')

            texto_pagina = remove_header_footer_fixos(texto_pagina)
            texto_final += texto_pagina

            # exceto as que estão na tabela
            negrito += [palavra for palavra in palavras.split('\n') if palavra not in texto_tabela]

    return negrito, texto_final


#funcao auxiliar
def letra_pequenas(filePath):
    results = []
    pdf = fitz.open(filePath) # filePath is a string that contains the path to the pdf

    for i ,page in enumerate(pdf):
        if page.number == 10:
            break

        dict = page.get_text("dict")
        blocks = dict["blocks"]
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                for span in spans:
                    data = span['spans']
                    for lines in data:
                        results.append((lines['text'], lines['size'], i))
    
    filtered_results = [(texto,i) for texto, font_size, i in results if font_size < 9.5 and len(texto) > 10]
    pdf.close()
    return filtered_results


def remove_header_footer_fixos(texto):
    """Remove o cabeçalho e rodapé do PDF."""
    texto = texto.split('\n')
    if 'Page' in texto[-1] or 'Template' in texto[-1]:
        texto = texto[:len(texto)-1]

    texto = ' '.join(texto)
    texto = texto.encode('ascii', errors='ignore').decode('ascii')

    return texto
    
if __name__ == "__main__":
    main()