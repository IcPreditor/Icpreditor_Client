##Import comuns
import os
import numpy as np
import pandas as pd
##Import dados processados
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../processing')))

#sys.path.insert(1, r'./processingprocessingPrevisao')

import processing
import processingPrevisao
##Import Divisor de teste treino
from sklearn.model_selection import train_test_split
##Import Modelo Regressão Logística 
from sklearn.linear_model import LogisticRegression
##Import Metrics para matriz de confusão
from sklearn import metrics
##Import pyplot para plot da matriz de confusão
import matplotlib.pyplot as plt
import seaborn as sns
##Import para classificação da matriz de confusão
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

## Data treinamento 
X_train, Y_train, X_test, Y_test,dataframeTreinamento,feature_cols = processing.getInputOutput(undersampling=False,regressao=True)
logreg = LogisticRegression(random_state=16,max_iter=100000)
print(X_train)
print(Y_train)


#Garantir que motivo de evasão não é passado
for col in ['motivo_de_evasao']:
    if col in X_train.columns:
        X_train = X_train.drop(columns=[col])
    if col in X_test.columns:
        X_test = X_test.drop(columns=[col])
logreg.fit(X_train, Y_train)

Y_pred_test = logreg.predict(X_test)

acuracia = accuracy_score(Y_test, Y_pred_test)
print("Acurácia: ",acuracia)

#Dados a terem suas evasões previstas 
file_path = r'../data/studentsPrediction.json'

X_prev,dataframeCopia,columns_to_keep = processingPrevisao.studentsDataframe(file_path)

matriculas = X_prev['matricula_do_estudante']
X_prev = X_prev.drop(columns='matricula_do_estudante')

Y_prev = logreg.predict(X_prev)

# Mapeando os valores para as strings desejadas
Y_prev_mapped = ['Sem risco' if y == '0' else 'Com risco' for y in Y_prev]

# Criando um DataFrame com o resultado formatado
resultado_df = pd.DataFrame({
    'matrícula': matriculas,
    'Evasão': Y_prev_mapped
})

# Filtrando apenas os alunos com risco de evasão
resultado_risco_df = resultado_df[resultado_df['Evasão'] == 'Com risco']

if resultado_risco_df.empty:
    print("Não tem alunos com risco de evasão")
else:
    print("Matrícula - Evasão")
    # Exibindo no formato desejado
    for index, row in resultado_risco_df.iterrows():
        print(f"{row['matrícula']} - {row['Evasão']}")




