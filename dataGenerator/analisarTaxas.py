import pandas as pd
def load_large_json(file_path):
    return pd.read_json(file_path)
# Caminho para o arquivo JSON
file_path = r'data/students.json'

#Carregar os dados
dataframe = load_large_json(file_path)
print(dataframe.count(axis='columns'))
print(dataframe.value_counts("estado_civil",dropna=False))

#Mapeamento binário somente para motivo de evasão, pois é muito extenso
motivo_de_evasao_mapping = {
    "REGULAR": "000000",
    "GRADUADO": "000001",
    "TRANSFERIDO PARA OUTRA IES": "000010",
    "FALECIMENTO": "000011",
    "CANCELAMENTO NOVO CURRICULO": "000100",
    "CANCELAMENTO POR ABANDONO": "000101",
    "CANCELAMENTO DE MATRICULA ": "000110",
    "CANCELAMENTO P/ MUDANCA CURSO": "000111",
    "CANCELAMENTO P/ DECISAO JUDICIAL": "001000",
    "CANCELAMENTO P/ SOLICITACAO ALUNO": "001001",
    "SUSPENSAO TEMPORARIA": "001010",
    "CONCLUIDO - NAO COLOU GRAU": "001011",
    "CANCELAMENTO_NAO_CUMPRIMENTO_PEC": "001100",
    "CANCELADO NOVO INGRESSO MESMO CURSO": "001101",
    "CANCELADO NOVO INGRESSO OUTRO CURSO": "001110",
    "CUMPRIMENTO_CONVENIO": "001111",
    "NAO COMPARECEU CADASTRO": "010000",
    "REMANEJADO_CURSO_OU_PERIODO": "010001",
    "NAO_COMPARECEU_AO_REMANEJAMENTO": "010010",
    "INGRESSANTE NAO FEZ 1ª MATRICULA": "010011",
    "TERMINO_DO_INTERCAMBIO": "010100",
    "GRADUADO - DECISAO JUDICIAL": "010101",
    "CANCELADO REPROVOU TODAS POR FALTAS": "010110",
    "SUSPENSO_DEBITO_BIBLIOTECA": "010111",
    "CANCELADO 3 REPROV MESMA DISCIPLINA": "011000",
    "SOLICITOU DESVÍNCULO SEM MATRÍCULA": "011001",
    "AGUARDANDO_CADASTRAMENTO": "011010",
    "VALIDACAO_DECLARACAO_PENDENTE": "011011"
}
# Definindo as categorias a serem removidas
categorias_para_remover = [
    "000100",
    "001010",
    "001101",
    "010000",
    "010011",
    "011010"
]
print(dataframe.value_counts("motivo_de_evasao",dropna=False))

dataframe['motivo_de_evasao'] = dataframe['motivo_de_evasao'].map(motivo_de_evasao_mapping)

print(dataframe.value_counts("motivo_de_evasao",dropna=False))
# Removendo os registros do DataFrame
