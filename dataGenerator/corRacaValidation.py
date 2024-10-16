import pandas as pd
def load_large_json(file_path):
    return pd.read_json(file_path)
# Caminho para o arquivo JSON
file_path = r'data/students.json'
dataframe = load_large_json(file_path)

for aluno in dataframe:
    print(aluno[0])