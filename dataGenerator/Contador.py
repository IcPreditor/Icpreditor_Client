#Count occurrences of certain parameters
#Guilherme Fernandes, 2024

import numpy as np
import pandas as pd
import sys
sys.path.insert(1, r'processing')
import processing
students_in,students_out,dataframe = processing.getInputOutput()

#def load_large_json(file_path):
#    return pd.read_json(file_path)
#file_path = r'data/students.json'
#dataframe = load_large_json(file_path)
colunas = ['nome_do_curso','turno_do_curso','nome_do_setor','estado_civil', 'genero', 'idade',
        'situacao', 'motivo_de_evasao', 'periodo_de_evasao', 'periodo_de_ingresso', 'naturalidade',
        'cor', 'tipo_de_ensino_medio','politica_afirmativa', 'prac_renda_per_capita_ate',
        'taxa_de_sucesso']
#print(dataframe.iloc[9199])
#rint(dataframe.iloc[9200])
#print(dataframe.columns)
#print(dataframe.value_counts("taxa_de_sucesso"))

for i in range(len(students_in)):
    if len(students_in[i])!=34:
        print('#')
        print(i)
        print(len(students_in[i]))
#print(dataframe.value_counts())


