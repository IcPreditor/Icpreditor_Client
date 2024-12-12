## Importar módulos necessários
import sys

from matplotlib.colors import LinearSegmentedColormap
sys.path.insert(1, r'processing')
import processing

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.metrics import classification_report, precision_recall_curve, auc

# Carregar dados processados e fazer a divisão treino/teste
X_train, Y_train, X_test, Y_test, dataframeCopia, feature_cols = processing.getInputOutput(undersampling=False, regressao=True, evadedColumn=True)
dataframeCopia = pd.DataFrame(dataframeCopia)
print(feature_cols)

['idade', 'genero', 'estado_civil', 'politica_afirmativa',
'tipo_de_ensino_medio', 'turno_do_curso', 'cor',
'prac_renda_per_capita_ate', 'prac_deficiente',
'nome_do_setor', 'taxa_de_sucesso', 'cra', 'motivo_de_evasao',
'evaded']
dataframeCopia['evaded'] = dataframeCopia['evaded'].replace({'1':'Evasão','0':'Não Evasão'})
def traducao(variavel):
    dicionario = {
        'idade':{'001':'Menor que 15','010':'16 - 18','011':'19 - 21','100':'22 - 25','101':'26 - 30', '110':'31 - 40','111':'+40'},
        'genero':{'0':'Masculino','1':'Feminino'},
        'estado_civil':{'000':'Solteiro','001':'Casado','010':'Viúvo','011':'Divorciado','101':'Não Informado'},
    }
    return dicionario[variavel]

# Frequência 
def gerarProporcao(col):
    
    print(dataframeCopia)
    agrupamento = dataframeCopia.groupby([col,'evaded']).size().reset_index(name='frequencia')
    agrupamento['percentual'] = agrupamento['frequencia'] / agrupamento.groupby(col)['frequencia'].transform('sum') * 100
    print(agrupamento)
    
    #agrupamento[col] = agrupamento[col].replace(traducao(col))

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=agrupamento, y=col, x='percentual', hue='evaded')

    for bar, freq in zip(ax.containers, agrupamento['frequencia']):
        ax.bar_label(bar, labels=[f'{freq} ({pct:.1f}%)' for pct in bar.datavalues]) 

    plt.title(f'Proporção Percentual de {col} em Relação a Evasão')
    plt.xlabel(f'{col}')
    plt.xlim(0,100)
    plt.ylabel('Proporção (%)')
    #plt.ylim(0, 100)  # Para limitar o eixo Y a 100%
    plt.legend(title='Evasão')
    plt.show()
gerarProporcao(col = 'nome_do_curso')