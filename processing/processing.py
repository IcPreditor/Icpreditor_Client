import json
import pandas as pd
import numpy as np

binaryTurnos = {
    "M":'00',
    "V":'01',
    "N":'10',
    "D":'11'
}

def getTurno(course):
    saida = '00'
    for c in json.load(open("data/coursesActives.json", encoding='utf-8')):
        if c['code'] == course:
            saida = binaryTurnos[c["name"][-1]]
            break
    
    return saida

def load_large_json(file_path):
    return pd.read_json(file_path)

# Caminho para o arquivo JSON
file_path = r'C:\Users\Usuário\Icpreditor\data\students.json'

# Carregar os dados
dataframe = load_large_json(file_path)
    
# Obter dados dos estudantes
#df = get_student_data()
#Fazer lista de turnos
dataframe["turno"] = dataframe.apply(lambda row: getTurno(row["courseCode"])  , axis=1)

# Mapeamento binário para valores categóricos
binary_mappings = {
    "gender": {"MASCULINO": "00", "FEMININO": "01", "OUTRO": "10", "DESCONHECIDO": "11"},
    "nationality": {"BRASILEIRA": "00", "ESTRANGEIRA": "01"},
    "maritalStatus": {"SOLTEIRO": "000", "CASADO": "001", "SEPARADO": "010", "VIUVO": "011", "DIVORCIADO": "100", "DESCONHECIDO": "101"},
    "status": {"GRADUADO": "00", "ATIVO": "01", "INATIVO": "10"},
    "inactivityReason": {"ABANDONO": "000", "DESCONHECIDO": "001", "TRANSFERENCIA": "010", "CONCLUIU_MAS_NAO_COLOU_GRAU": "011", "DESISTENCIA": "100"},
    "affirmativePolicy": {"A0": "000", "L1": "001", "L2": "010", "L5": "011", "L6": "100", "L9": "101", "L10": "110", "L13": "111", "L14": "1000", "BONUS": "1001"},
    "secondarySchoolType": {"PRIVADA": "00", "PUBLICA": "01", "MAJORITARIAMENTE_PUBLICA": "10", "MAJORITARIAMENTE_PRIVADA": "11", "DESCONHECIDA": "100"}
}

#Ajuste do secondarySchoolType desconhecido
def adjust_secondary_school_type(row):
    if row["secondarySchoolType"] == "DESCONHECIDA":
        if row["affirmativePolicy"] == "A0":
            return "PRIVADA"    
        else:
            return "PUBLICA"
    return row["secondarySchoolType"]

dataframe["secondarySchoolType"] = dataframe.apply(adjust_secondary_school_type, axis=1)

# Converter valores categóricos para sua representação binária
for col, mapping in binary_mappings.items():
    dataframe[col] = dataframe[col].map(mapping)
# Converter valores numéricos para binário
dataframe["age"] = dataframe["age"].apply(lambda x: format(int(x), '08b') if pd.notnull(x) else "0"*8)
dataframe["courseCode"] = dataframe["courseCode"].apply(lambda x: format(int(x), '020b') if pd.notnull(x) else "0"*20)
#df["curriculumCode"] = df["curriculumCode"].apply(lambda x: ''.join(format(ord(i), '08b') for i in x) if pd.notnull(x) else "0"*32)
dataframe["curriculumCode"] = dataframe["curriculumCode"].apply(
    lambda x: ''.join(format(ord(i), '08b') for i in str(x)) if pd.notnull(x) else "0"*32
)
# Colunas a serem mantidas
columns_to_keep = ["age", "gender", "nationality", "maritalStatus", "affirmativePolicy", "secondarySchoolType", "courseCode", "curriculumCode"]

# Remover todas as colunas que não estão em columns_to_keep
dataframe = dataframe.drop(columns=[column for column in dataframe.columns if column not in columns_to_keep])
# Substituir NaN por binário de 0s
dataframe.fillna("0", inplace=True)
dataframe = dataframe.astype(str)

#Concatenar os resultados em uma string binária por linha
binary_strings = dataframe.apply(lambda row: "".join(row.values), axis=1).to_list()

# Visualizar o resultado
print(binary_strings)
#print(evaded_list)
#print(dataframe)

#Fazer uma lista dos estudantes que evadiram com base na sua razao de inatividade
#dataframe['evaded'] = dataframe.apply(lambda row: '1' if row['status'] == '10' and row['inactivityReason'] != '010' else '0', axis=1)
#evaded_list = dataframe['evaded'].tolist()
