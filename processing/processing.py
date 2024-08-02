import json
import pandas as pd
import numpy as np
from dicTurno import getTurno

# Carrega dicionario com codeCurso/turno
dicTurnos = getTurno()
def whatTurno(row):
    return dicTurnos[str(row["courseCode"])]

def load_large_json(file_path):
    return pd.read_json(file_path)

#Ajuste do secondarySchoolType desconhecido
def adjust_secondary_school_type(row):
    if row["secondarySchoolType"] == "DESCONHECIDA":
        if row["affirmativePolicy"] == "A0":
            return "PRIVADA"    
        else:
            return "PUBLICA"
    return row["secondarySchoolType"]
def getInputOutput():
    # Caminho para o arquivo JSON
    file_path = r'data/students.json'

    # Carregar os dados
    df = load_large_json(file_path)
        
    #Definir Turno
    df["courseCode"] = df.apply(whatTurno, axis=1)


    # Mapeamento binário para valores categóricos
    binary_mappings = {
        "gender": {"MASCULINO": "00", "FEMININO": "01", "OUTRO": "10", "DESCONHECIDO": "11"},
        "nationality": {"BRASILEIRA": "0", "ESTRANGEIRA": "1"},
        "maritalStatus": {"SOLTEIRO": "000", "CASADO": "001", "SEPARADO": "010", "VIUVO": "011", "DIVORCIADO": "100", "DESCONHECIDO": "101"},
        "status": {"GRADUADO": "00", "ATIVO": "01", "INATIVO": "10"},
        "inactivityReason": {"ABANDONO": "000", "DESCONHECIDO": "001", "TRANSFERENCIA": "010", "CONCLUIU_MAS_NAO_COLOU_GRAU": "011", "DESISTENCIA": "100"},
        "affirmativePolicy": {"A0": "0000", "L1": "0001", "L2": "0010", "L5": "0011", "L6": "0100", "L9": "0101", "L10": "0110", "L13": "0111", "L14": "1000", "BONUS": "1001"},
        "secondarySchoolType": {"PRIVADA": "000", "PUBLICA": "001", "MAJORITARIAMENTE_PUBLICA": "010", "MAJORITARIAMENTE_PRIVADA": "011", "DESCONHECIDA": "100"}
    }


    #Ajustar Secondary_School_type
    df["secondarySchoolType"] = df.apply(adjust_secondary_school_type, axis=1)

    # Converter valores categóricos para sua representação binária
    for col, mapping in binary_mappings.items():
        df[col] = df[col].map(mapping)

    # Converter valores numéricos para binário
    df["age"] = df["age"].apply(lambda x: format(int(x), '08b') if pd.notnull(x) else "0"*8)

    # Colunas a serem mantidas
    columns_to_keep = ["age", "gender", "nationality", "maritalStatus", "status", "inactivityReason", "affirmativePolicy", "secondarySchoolType", "courseCode"]

    # Remover todas as colunas que não estão em columns_to_keep
    df = df.drop(columns=[col for col in df.columns if col not in columns_to_keep])
    # Substituir NaN por binário de 0s
    df["nationality"] = df["nationality"].fillna("0")
    df["inactivityReason"] = df["inactivityReason"].fillna("000")
    df = df.astype(str)
    #Fazer uma lista dos estudantes que evadiram com base na sua razao de inatividade
    df['evaded'] = df.apply(lambda row: '1' if row['status'] == '10' and row['inactivityReason'] != '010' else '0', axis=1)
    #Concatenar os resultados em uma string binária por linha
    binary_strings = df.apply(lambda row: ["".join(row.values)], axis=1).to_list()
    evaded_list = df["evaded"].apply(lambda row:[ int("".join(row))]).to_list()
    return binary_strings,evaded_list

# Visualizar o resultado

#print(evaded_list)
#print(df)