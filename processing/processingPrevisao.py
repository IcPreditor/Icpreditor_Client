#Data processing, mapping and transformation on the bases we use
#Guilherme Fernandes, 2024
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime as dt
sys.path.insert(1, r'processing')
import processing


def load_large_json(file_path):
    return pd.read_json(file_path)

def ajustDataframe(dataframe):
    dataframe = processing.mapeamentoDataframe(dataframe)

    # Colunas a serem mantidas
    columns_to_keep = ['matricula_do_estudante',"idade", "genero", "estado_civil", "politica_afirmativa", "tipo_de_ensino_medio", "turno_do_curso", "cor", "prac_renda_per_capita_ate", "prac_deficiente", "nome_do_setor",'taxa_de_sucesso','cra']
    
    #Salva Copia do dataframe
    dataframeCopia = dataframe
    # Remover todas as colunas que não estão em columns_to_keep
    dataframe = dataframe.drop(columns=[column for column in dataframe.columns if column not in columns_to_keep])
    dataframe = dataframe.astype(str)
    # Substituir NaN por binário de 0s
    dataframe.fillna("0", inplace=True)
    
    dataframe = dataframe.reindex(['matricula_do_estudante','turno_do_curso','nome_do_setor','estado_civil','genero','idade','cor','tipo_de_ensino_medio','politica_afirmativa','prac_renda_per_capita_ate','taxa_de_sucesso','prac_deficiente','cra'], axis=1)
    X_previsao = dataframe
    return(X_previsao,dataframeCopia,columns_to_keep)

def studentsDataframe(file_path):
    dataframe = load_large_json(file_path)
    return ajustDataframe(dataframe)
    