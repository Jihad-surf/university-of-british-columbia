# Instalação

Certifique-se de ter o Python instalado. Clone o repositório e navegue até o diretório do projeto.

```bash
git clone https://github.com/Jihad-surf/trinity_recibo_ferias.git
```
Instale os pacotes necessarios
```bash
pip install -r requirements.txt
```


# Modo de uso
basta deixar os pdfs a serem analisados dentro da pasta pdfs e rodar a main.py, ele ira gerar um output chamado dados.json

# observações
1. Caso queira rodar apenas um codigo basta trocar os valores no dicionario presente dentro da main.py     
  start_scripts = {
      'excecutive summary': True,
      'key words': True,
      'most words': True
  } .    
  True = Ira executar a função.   
  Falso = Ira ignorar a função
1. para o processo de contagem de keywords, basta adicionar ou retirar as palavras do aquivo Key Words.xlsx, inserir as palavras no singular, assim vai dar match tanto pra palavras no plural quanto no singular, a mesma logica segue para covid-19, colocar apenas covid ira contar tanto covid-19 quanto covid. Caso queira contar realmente covid-19, ai sim inserir covid-19
1. Para o processo de contagem de palavras mais comum, foi criado um arquivo chamado stop_words.xlsx, onde as palavras presentes nele seram ignordas na contagem. Caso queira que apareça mais do que as top3, basta alterar o paramentro no arquivo main.py --> most_words = mw.obter_palavras_frequentes(texto,{qtd_de_top_palavras})

