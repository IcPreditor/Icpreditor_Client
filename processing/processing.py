#Data processing, mapping and transformation on the bases we use
#Eduardo Augusto, 2024

import json
import pandas as pd
import numpy as np
# Mapeamento de dados do bando
# idade faixas <=15:001, <=18:010, <=21:011, <=25:100, <=30:101, <=40:110, >40:111
# genero masculino:00 feminino:01 outro:10 descinhecido:11
# estado_civil solteiro:000 casado:001 separado:010 viuvo:011 divorciado:100 desconhecido:101
# politica_afirmativa "A0": "0000", "L1": "0001", "L2": "0010", "L5": "0011", "L6": "0100", "L9": "0101", "L10": "0110", "L13": "0111", "L14": "1000", "BONUS": "1001"
# tipo_de_ensino_medio "PRIVADA": "000", "PUBLICA": "001", "MAJORITARIAMENTE_PUBLICA": "010", "MAJORITARIAMENTE_PRIVADA": "011", "DESCONHECIDA": "100"
# turno: "Integral":'11',"Matutino":'01',"Noturno":"10"
# nacionalidade: brasileira:0 estrangeira:1
# cor: "BRANCA": "001", "PRETA": "010", "PARDA": "10", "INDÍGENA": "011", "MESTIÇA": "100", "ORIENTAL": "101", "OUTRAS": "110"
# prac_renda_per_capita_ate: Faixa de renda, semelhante ao idade
# prac_deficiencias: "-": "0", "Sim": "1"

# Carrega dicionario com codeCurso/turno


def load_large_json(file_path):
    return pd.read_json(file_path)


# Mapeamento binário para valores categóricos
binary_mappings = {
    "genero": {"MASCULINO": "00", "FEMININO": "01", "OUTRO": "10", "DESCONHECIDO": "11"},
    "nacionalidade": {"BRASILEIRA": "0", "ESTRANGEIRA": "1"},
    "estado_civil": {"SOLTEIRO": "000", "CASADO": "001", "SEPARADO": "010", "VIUVO": "011", "DIVORCIADO": "100", "DESCONHECIDO": "101"},
    "situacao": {"GRADUADO": "00", "ATIVO": "01", "INATIVO": "10"},
    "motivo_de_evasao": {"CANCELAMENTO POR ABANDONO": "0000", "REGULAR": "0001", "NAO COMPARECEU CADASTRO": "0010", "CANCELADO REPROVOU TODAS POR FALTAS": "0011", "CANCELADO NOVO INGRESSO OUTRO CURSO": "0100", "CANCELADO NOVO INGRESSO MESMO CURSO": "1111"},
    "politica_afirmativa": {"A0": "0000", "L1": "0001", "L2": "0010", "L5": "0011", "L6": "0100", "L9": "0101", "L10": "0110", "L13": "0111", "L14": "1000", "BONUS": "1001"},
    "tipo_de_ensino_medio": {"PRIVADA": "000", "PUBLICA": "001", "MAJORITARIAMENTE_PUBLICA": "010", "MAJORITARIAMENTE_PRIVADA": "011", "DESCONHECIDA": "100"},
    "cor": {"BRANCA": "001", "PRETA": "010", "PARDA": "10", "INDÍGENA": "011", "MESTIÇA": "100", "ORIENTAL": "101", "OUTRAS": "110"},
    "prac_deficiente": {"-": "0", "Sim": "1"},
    "turno_do_curso":{"Integral":'11',"Matutino":'01',"Noturno":"10"}
}

#Ajuste do tipo_de_ensino_medio desconhecido
def adjust_secondary_school_type(row):
    if row["tipo_de_ensino_medio"] == "DESCONHECIDA":
        if row["politica_afirmativa"] == "A0":
            return "PRIVADA"    
        else:
            return "PUBLICA"
    return row["tipo_de_ensino_medio"]

#Classificação de faixa etária
def age_to_binary(idade):
    if idade <= 15:
        return '001'
    elif idade <= 18 :
        return '010'
    elif idade <= 21:
        return '011'
    elif idade <= 25:
        return '100'
    elif idade <= 30:
        return '101'
    elif idade <= 40:
        return '110'
    else:
        return '111'
    
#Classificação de renda per capita
def income_to_binary(prac_renda_per_capita_ate):
    if prac_renda_per_capita_ate <= 1.5:
        return '001'
    elif prac_renda_per_capita_ate <= 3.0 :
        return '010'
    elif prac_renda_per_capita_ate <= 5.0:
        return '011'
    elif prac_renda_per_capita_ate <= 7.0:
        return '100'
    elif prac_renda_per_capita_ate <= 10.0:
        return '101'
    else:
        return '110'

def getInputOutput():
    # Caminho para o arquivo JSON
    file_path = r'data/students.json'
    
    #Carregar os dados
    dataframe = load_large_json(file_path)
    # Aleatoriza banco de dados
    dataframe = dataframe.sample(frac=1,ignore_index=True,random_state=100)
    #Fazer lista de turnos
    dataframe["tipo_de_ensino_medio"] = dataframe.apply(adjust_secondary_school_type, axis=1)

    # Converter valores categóricos para sua representação binária
    for column, mapping in binary_mappings.items():
        dataframe[column] = dataframe[column].map(mapping)

    # Converter valores numéricos para binário
    dataframe["idade"] = dataframe["idade"].apply(age_to_binary)

    dataframe["prac_renda_per_capita_ate"] = dataframe["prac_renda_per_capita_ate"].apply(income_to_binary)

    #Fazer uma lista dos estudantes que evadiram com base na sua razao de inatividade
    dataframe['evaded'] = dataframe.apply(lambda row: 1 if row['situacao'] == '10' and row['motivo_de_evasao'] != '010' else 0, axis=1)

    # Verificar a proporção antes do balanceamento
    print(dataframe.value_counts("evaded"))

    # A coluna 'evaded' contem 1 para evadidos e 0 para não evadidos
    evadidos = dataframe[dataframe['evaded'] == 1]
    nao_evadidos = dataframe[dataframe['evaded'] == 0]

    # Realizando um undersampling, que seria diminuir da classe maior para igualar com a menor
    if len(evadidos) < len(nao_evadidos):
        nao_evadidos_balanced = nao_evadidos.sample(n=len(evadidos), random_state=42)
        dataframe_balanced = pd.concat([evadidos, nao_evadidos_balanced])
    else:
        evadidos_balanced = evadidos.sample(n=len(nao_evadidos), random_state=42)
        dataframe_balanced = pd.concat([evadidos_balanced, nao_evadidos])

    # Embaralhar o dataframe
    dataframe_balanced = dataframe_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

    # Verificar a proporção após o balanceamento
    print(dataframe_balanced['evaded'].value_counts(normalize=True))

    evaded_list = dataframe_balanced['evaded'].tolist()

    # Colunas a serem mantidas
    columns_to_keep = ["idade", "genero", "nacionalidade", "estado_civil", "politica_afirmativa", "tipo_de_ensino_medio", "turno", "cor", "prac_renda_per_capita_ate", "prac_deficiente"]

    # Remover todas as colunas que não estão em columns_to_keep
    # Dataframe se torna dataframe_balanced
    dataframe = dataframe_balanced.drop(columns=[column for column in dataframe.columns if column not in columns_to_keep])

    dataframe = dataframe.astype(str)

    # Substituir NaN por binário de 0s
    dataframe.fillna("0", inplace=True)
    #Concatenar os resultados em uma string binária por linha
    binary_strings = dataframe.apply(lambda row: "".join(row.values), axis=1).to_list()
    #print(dataframe)
    return(binary_strings,evaded_list)

getInputOutput()