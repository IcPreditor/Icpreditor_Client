import pandas as pd
import numpy as np

# Exemplo de dados
data = [
    {
        "age": 35, 
        "gender": "FEMININO", 
        "maritalStatus": "DESCONHECIDO", 
        "status": "INATIVO", 
        "inactivityReason": "DESISTENCIA", 
        "affirmativePolicy": "BONUS", 
        "secondarySchoolType": "DESCONHECIDA", 
        "courseCode": "13301100", 
        "curriculumCode": "2017"
    }
]

df = pd.DataFrame(data)

# Mapeamento binário para valores categóricos
binary_mappings = {
    "gender": {"MASCULINO": "00", "FEMININO": "01", "OUTRO": "10", "DESCONHECIDO": "11"},
    "maritalStatus": {"SOLTEIRO": "000", "CASADO": "001", "SEPARADO": "010", "VIUVO": "011", "DIVORCIADO": "100", "DESCONHECIDO": "101"},
    "status": {"GRADUADO": "00", "ATIVO": "01", "INATIVO": "10"},
    "inactivityReason": {"ABANDONO": "000", "DESCONHECIDO": "001", "TRANSFERENCIA": "010", "CONCLUIU_MAS_NAO_COLOU_GRAU": "011", "DESISTENCIA": "100"},
    "affirmativePolicy": {"A0": "000", "L1": "001", "L2": "010", "L5": "011", "L6": "100", "L9": "101", "L10": "110", "L13": "111", "L14": "1000", "BONUS": "1001"},
    "secondarySchoolType": {"PRIVADA": "00", "PUBLICA": "01", "MAJORITARIAMENTE_PUBLICA": "10", "MAJORITARIAMENTE_PRIVADA": "11", "DESCONHECIDA": "100"}
}

# Converter valores categóricos para sua representação binária
for col, mapping in binary_mappings.items():
    df[col] = df[col].map(mapping)

# Converter valores numéricos para binário
df["age"] = df["age"].apply(lambda x: format(int(x), '08b') if pd.notnull(x) else "0"*8)
df["courseCode"] = df["courseCode"].apply(lambda x: format(int(x), '020b') if pd.notnull(x) else "0"*20)
df["curriculumCode"] = df["curriculumCode"].apply(lambda x: ''.join(format(ord(i), '08b') for i in x) if pd.notnull(x) else "0"*32)

# Substituir NaN por binário de 0s
df.fillna("0", inplace=True)

# Visualizar o DataFrame resultante
print(df.to_string(index=False))
