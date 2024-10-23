import pandas as pd
def load_large_json(file_path):
    return pd.read_json(file_path)
# Caminho para o arquivo JSON
file_path = r'data/students.json'
dataframe = load_large_json(file_path)
prac_count = 0
erro = 0

for i in range(len(dataframe)):
    aluno = dataframe.iloc[i]
    if aluno["prac_cor"]!="-":
        print( aluno["prac_cor"])
        print(aluno["cor"])
        prac_count+=1
        
        if aluno["prac_cor"].upper() != aluno["cor"].upper():
            erro+=1
print("#")
print(f"Com registro de cor Prac:  {prac_count}")
print(f"Com registro de cor que difere do registro Prac:  {erro}")
print(f"Taxa de irregularidade: {(erro/prac_count)*100:.2f}%")