import pytest
import json

with open('dados.json', 'r') as arquivo_json:
    dados = json.load(arquivo_json)

def get_summary_by_keyword(keyword):
    for file in dados:
        if keyword in file:
            return dados[file]

def test_employment_summary():
    summary = get_summary_by_keyword('Employment')
    assert summary.startswith('The purpose of the Employment') == True
    assert summary.endswith('at UBC Okanagan.') == True

def test_generative_ai_summary():
    summary = get_summary_by_keyword('Generative-AI')
    assert summary.startswith('One academic term') == True
    assert summary.endswith(' generative AI at UBC.') == True

def test_International_summary():
    summary = get_summary_by_keyword('International')
    assert summary.startswith('UBCO is launching') == True
    assert summary.endswith('to careers post-graduation.') == True

def test_satfFood_summary():
    summary = get_summary_by_keyword('SATF Food') 
    assert summary.startswith('In March 2022, the') == True
    assert summary.endswith('for food and housing insecurity.') == True

def test_annual_summary():
    summary = get_summary_by_keyword('Annual')
    assert summary.startswith('In accordance with') == True
    assert summary.endswith('its related government.') == True

def test_evolution_summary():
    summary = get_summary_by_keyword('Evolution')
    assert summary.startswith('An analysis was completed') == True
    assert summary.endswith(' at UBC Vancouver.') == True

def test_Human_summary():
    summary = get_summary_by_keyword('Human')
    assert summary.startswith('The Human Rights Team works collaboratively') == True
    assert summary.endswith('or the period of May 1, 2022–April 30, 2023.') == True

def test_Indigenous_summary():
    summary = get_summary_by_keyword('Indigenous')
    assert summary.startswith('Adrienne Vedan, Senior Advisor to the Deputy Vice-Chancellor on Indigenou') == True
    assert summary.endswith('e Okanagan and Vancouver campuses.') == True

def test_Campus_summary():
    summary = get_summary_by_keyword('Campus')
    assert summary.startswith('This briefing provides the final') == True
    assert summary.endswith(' continuing Wesbrook Place development.') == True

def test_Housing_summary():
    summary = get_summary_by_keyword('Housing')
    assert summary.startswith('This briefing provides the final ten-year Housing') == True
    assert summary.endswith(' reviews if these barriers are removed.') == True

if __name__ == "__main__":
    pytest.main()