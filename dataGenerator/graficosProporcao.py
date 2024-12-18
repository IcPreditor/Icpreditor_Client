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

def traducaoCurso(curso):
    if curso=='LETRAS - LÍNGUA INGLESA (LIC) - D':
        return 'LETRAS INGLÊS'
    elif curso=='LETRAS- LÍNGUA PORTUGUESA (LIC) - D' or curso=='LETRAS - LÍNGUA PORTUGUESA (LIC) - N':
        return 'LETRAS PORTUGUÊS'
    elif curso=='LETRAS - LÍNG.PORT./LÍNG.FRANC.(LIC)-D':
        return 'LETRAS FRANC.'
    elif curso=='LETRAS - LIBRAS (LIC) - D':
        return 'LETRAS LIBRAS'
    elif curso=='LETRAS - ESPANHOL (LICENCIATURA) N':
        return 'LETRAS ESPANHOL'
    return curso.split('(')[0].split('-')[0]

def traducao(variavel):
    dicionario = {
        'idade':{'001':'Menor que 15','010':'16 - 18','011':'19 - 21','100':'22 - 25','101':'26 - 30', '110':'31 - 40','111':'+40'},
        'genero':{'0':'Masculino','1':'Feminino'},
        'estado_civil':{'000':'Solteiro','001':'Casado','010':'Viúvo','011':'Divorciado','101':'Não Informado'},
    }
    return dicionario[variavel]
def traducaoEvaded(x):
    if x==0:
        return 'Não Evasão'
    else:
        return 'Evasão'
# Carregar dados processados e fazer a divisão treino/teste
X_train, Y_train, X_test, Y_test, dataframeCopia, feature_cols = processing.getInputOutput(undersampling=False, regressao=True, evadedColumn=True)
dataframeCopia = pd.DataFrame(dataframeCopia)
print(feature_cols)

['idade', 'genero', 'estado_civil', 'politica_afirmativa',
'tipo_de_ensino_medio', 'turno_do_curso', 'cor',
'prac_renda_per_capita_ate', 'prac_deficiente',
'nome_do_setor', 'taxa_de_sucesso', 'cra', 'motivo_de_evasao',
'evaded']
dataframeCopia['evaded'] = dataframeCopia['evaded'].apply(traducaoEvaded)
print(dataframeCopia.value_counts('evaded'))
dataframeCopia['nome_do_curso'] = dataframeCopia['nome_do_curso'].apply(traducaoCurso)
# Frequência 
def gerarProporcao(col):
    frequencias = dataframeCopia.groupby([col,'evaded']).size().reset_index(name='contagem')
    
    frequencias['percentual'] = frequencias.groupby(col)['contagem'].transform(lambda x : 100 * x / x.sum())
    
    sim_freq = frequencias[frequencias['evaded'] == 'Evasão']

    sim_freq = sim_freq.sort_values(by='percentual',ascending=False)
    

    print(frequencias)

    # Criar o gráfico de barras horizontais
    plt.figure(figsize=(15, 10))
    ax = sns.barplot(
        data=sim_freq,
        x='percentual',
        y=col,
        palette=['#1f77b4']
    )
    for container in ax.containers:
        ax.bar_label(container,fmt='%.1f%%',padding=5)

    plt.title(f'Porcentagem de {col} relacionada a Evaded')
    plt.xlabel('Porcentagem (%)')
    plt.ylabel(f'Valores de {col}')
    plt.show()
    
gerarProporcao(col = 'nome_do_curso')