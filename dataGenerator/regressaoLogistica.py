##Import comuns
import numpy as np
import pandas as pd
##Import dados processados
import sys
sys.path.insert(1, r'processing')
sys.path.insert(1, r'processingPrevisao')
from processingPrevisao import getInputOutput
import processing 
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

## Data
X_train, Y_train, X_test, Y_test,dataframe,feature_cols = processing.getInputOutput(undersampling=False,regressao=True)
logreg = LogisticRegression(random_state=16,max_iter=100000)
logreg.fit(X_train, Y_train)

print("Coeficiente de Regressão das Variáveis:")
coeficientes = logreg.coef_[0]
coeficientes_dict = {}
for i in range(len(feature_cols)):
    coeficientes_dict[feature_cols[i]]=coeficientes[i]
for item in sorted(coeficientes_dict,key=coeficientes_dict.get):
    print(f"{item} - [{coeficientes_dict[item]:.5f}]")

Y_pred = logreg.predict(X_test)

acuracia = accuracy_score(Y_test, Y_pred)
print("Acurácia: ",acuracia)

X_prev,dataframeCopia,columns_to_keep = getInputOutput()

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

print("Matrícula - Evasão")
# Exibindo no formato desejado
for index, row in resultado_df.iterrows():
    print(f"{row['matrícula']} - {row['Evasão']}")

#Métricas de avliação matriz de confusão
target_names = ["Não Evasão","Evasão"]
print(classification_report(Y_test,Y_pred,target_names=target_names))

# Exibir coeficientes de cada variável
print("Coeficiente de Regressão das Variáveis:")

# Calcular e organizar coeficientes em um DataFrame para melhor análise
coef_df = pd.DataFrame({
    'Variável': feature_cols,
    'Coeficiente': logreg.coef_[0]
})

# Ordenar pelo valor absoluto do coeficiente para identificar as variáveis com maior impacto
coef_df['Impacto Absoluto'] = coef_df['Coeficiente'].abs()
coef_df = coef_df.sort_values(by='Impacto Absoluto', ascending=False)

# Exibir as variáveis em ordem decrescente de impacto
print(coef_df[['Variável', 'Coeficiente']])



