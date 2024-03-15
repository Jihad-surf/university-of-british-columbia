import pytest
import json

with open('dados.json', 'r') as arquivo_json:
    dados = json.load(arquivo_json)

def get_keywords_by_keyword(keyword):
    for file, valor in dados.items():
        if keyword in file:
            return valor['key_words']

def test_employment_summary():
    key_words = get_keywords_by_keyword('Employment')
    assert key_words['faculty'] == 78