#Data processing, mapping and transformation on the bases we use
#Eduardo Augusto, 2024

import json
import pandas as pd
import numpy as np
from dicTurno import getTurno

# Carrega dicionario com codeCurso/turno
dictionaryTurnos = getTurno()
def whatTurno(row):
    return dictionaryTurnos[str(row["courseCode"])]

def load_large_json(file_path):
    return pd.read_json(file_path)

# Caminho para o arquivo JSON
file_path = r'C:\Users\Usuário\Icpreditor\data\students.json'

# Carregar os dados
dataframe = load_large_json(file_path)
    
# Obter dados dos estudantes

#Fazer lista de turnos
dataframe["turno"] = dataframe.apply(lambda row: getTurno()  , axis=1)

# Mapeamento binário para valores categóricos
binary_mappings = {
    "gender": {"MASCULINO": "0000", "FEMININO": "0001", "OUTRO": "0010", "DESCONHECIDO": "0011"},
    "nationality": {"BRASILEIRA": "0000", "ESTRANGEIRA": "0001"},
    "maritalStatus": {"SOLTEIRO": "0000", "CASADO": "0001", "SEPARADO": "0010", "VIUVO": "0011", "DIVORCIADO": "0100", "DESCONHECIDO": "0101"},
    "status": {"GRADUADO": "0000", "ATIVO": "0001", "INATIVO": "0010"},
    "inactivityReason": {"ABANDONO": "0000", "DESCONHECIDO": "0001", "TRANSFERENCIA": "0010", "CONCLUIU_MAS_NAO_COLOU_GRAU": "0011", "DESISTENCIA": "0100"},
    "affirmativePolicy": {"A0": "0000", "L1": "0001", "L2": "0010", "L5": "0011", "L6": "0100", "L9": "0101", "L10": "0110", "L13": "0111", "L14": "1000", "BONUS": "1001"},
    "secondarySchoolType": {"PRIVADA": "0000", "PUBLICA": "0001", "MAJORITARIAMENTE_PUBLICA": "0010", "MAJORITARIAMENTE_PRIVADA": "0011", "DESCONHECIDA": "0100"}
}

#Ajuste do secondarySchoolType desconhecido
def adjust_secondary_school_type(row):
    if row["secondarySchoolType"] == "DESCONHECIDA":
        if row["affirmativePolicy"] == "A0":
            return "PRIVADA"    
        else:
            return "PUBLICA"
    return row["secondarySchoolType"]

def age_to_binary(age):
    if age <= 17:
        return '0000'
    elif 18 <= age <= 20:
        return '0001'
    elif 20 <= age <= 22:
        return '0010'
    elif 22 <= age <= 24:
        return '0011'
    elif 24 <= age <= 26:
        return '0100'
    elif 26 <= age <= 28:
        return '0101'
    elif 28 <= age <= 30:
        return '0110'
    elif 30 <= age <= 33:
        return '0111'
    elif 33 <= age <= 36:
        return '1000'
    elif 36 <= age <= 45:
        return '1001'
    elif 46 <= age <= 60:
        return '1010'
    else:
        return '1011'

def getInputOutput():
    # Caminho para o arquivo JSON
    file_path = r'data/students.json'
    
    #Carregar os dados
    dataframe = load_large_json(file_path)

    dataframe["secondarySchoolType"] = dataframe.apply(adjust_secondary_school_type, axis=1)

    # Converter valores categóricos para sua representação binária
    for column, mapping in binary_mappings.items():
        dataframe[column] = dataframe[column].map(mapping)

    # Converter valores numéricos para binário
    dataframe["age"] = dataframe["age"].apply(age_to_binary)

    dataframe["courseCode"] = dataframe["courseCode"].apply(lambda x: format(int(x), '020b') if pd.notnull(x) else "0"*20)

    #dataframe["curriculumCode"] = dataframe["curriculumCode"].apply(lambda x: ''.join(format(ord(i), '08b') for i in x) if pd.notnull(x) else "0"*32)
    dataframe["curriculumCode"] = dataframe["curriculumCode"].apply(
        lambda x: ''.join(format(ord(i), '08b') for i in str(x)) if pd.notnull(x) else "0"*32
    )

    #Fazer uma lista dos estudantes que evadiram com base na sua razao de inatividade
    dataframe['evaded'] = dataframe.apply(lambda row: '1' if row['status'] == '0010' and row['inactivityReason'] != '0010' else '0', axis=1)
    evaded_list = dataframe['evaded'].tolist()
    
    # Colunas a serem mantidas
    columns_to_keep = ["age", "gender", "nationality", "maritalStatus", "affirmativePolicy", "secondarySchoolType", "courseCode", "curriculumCode"]

    # Remover todas as colunas que não estão em columns_to_keep
    dataframe = dataframe.drop(columns=[column for column in dataframe.columns if column not in columns_to_keep])

    # Substituir NaN por binário de 0s
    dataframe.fillna("0", inplace=True)
    dataframe = dataframe.astype(str)

    #Concatenar os resultados em uma string binária por linha
    binary_strings = dataframe.apply(lambda row: "".join(row.values), axis=1).to_list()
    print(binary_strings)

    # Visualizar o resultado
    print(evaded_list)

getInputOutput()