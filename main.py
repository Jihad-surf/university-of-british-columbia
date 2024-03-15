from scripts.executive_summary import main as start_executive_summary
from scripts.texts import start_get_texts 
import scripts.key_words as kw
import scripts.most_words as mw
import json

start_scripts = {
    'excecutive summary': True,
    'key words': True,
    'most words': True
}

def main(start_scripts):
    # chama a função de extrair o executive summary, ela ja atualiza o json
    if start_scripts['excecutive summary']:
        start_executive_summary()


    # carrega os textos e o json final
    textos = start_get_texts()
    with open('dados.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)


    # para cada arquivo chama a função de contar as palavras chaves e atualiza o json
    for file, texto in textos.items(): 
        if start_scripts['key words']:
            try:
                key_words = {}
                key_words = kw.count_keywords(texto)
                key_words = dict(key_words.most_common())
            except:
                key_words = {'erro': 'erro ao contar palavras chaves'}

            key_words_objeto = {'key_words': key_words}
            dados[file].update(key_words_objeto)
        
        if start_scripts['most words']:
            try:
                most_words = {}
                most_words = mw.obter_palavras_frequentes(texto,5)
                most_words = dict(most_words)
            except:
                most_words = {'erro': 'erro ao contar palavras chaves'}

            most_words_objeto = {'most_words': most_words}
            dados[file].update(most_words_objeto)

    with open('dados.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main(start_scripts)