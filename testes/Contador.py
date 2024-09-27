#Count occurrences of certain parameters
#Guilherme Fernandes, 2024

import numpy as np
import pandas as pd
import sys
sys.path.insert(1, r'C:\Users\m5253\VisualStudio\Icpreditor\processing')
import processing
def load_large_json(file_path):
    return pd.read_json(file_path)
file_path = r'data/students.json'
dataframe = load_large_json(file_path)
colunas = ['nome_do_curso','turno_do_curso','nome_do_setor','estado_civil', 'genero', 'idade',
        'situacao', 'motivo_de_evasao', 'periodo_de_evasao', 'periodo_de_ingresso', 'naturalidade',
        'cor', 'tipo_de_ensino_medio','politica_afirmativa', 'prac_renda_per_capita_ate',
        'taxa_de_sucesso']
#print(dataframe.columns)

for c in (colunas):
    print(c)
    print(dataframe.value_counts(c))
#print(dataframe.value_counts())


