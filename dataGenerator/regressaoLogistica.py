##Import comuns
import numpy as np
import pandas as pd
##Import dados processados
import sys
sys.path.insert(1, r'processing')
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

## Data
students_in,students_out,dataframe,feature_cols = processing.getInputOutput()
X = dataframe[feature_cols]
Y = dataframe['evaded']
# Dividir o conjunto de dados em conjuntos de treinamento e teste
# test_size=0.3 significa que 30% dos dados serão usados para teste e 70% para treinamento
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=16)

logreg = LogisticRegression(random_state=16,max_iter=100000)
logreg.fit(X_train, Y_train)

print("Coeficiente de Regressão das Variáveis:")
coeficientes = logreg.coef_[0]
for i in range(len(feature_cols)):
    print(f"{feature_cols[i]} - [{coeficientes[i]}]")

Y_pred = logreg.predict(X_test)


# Exibir previsões feitas pelo modelo
# Matriz de confusão 
cnf_matrix = metrics.confusion_matrix(Y_test, Y_pred)

#c = 0
#n_Y = len(Y_test)
#for i in range(n_Y):
#    if Y_test.iloc[i] == Y_pred[i]:
#        c+=1
#print(f'##{c}')
#print(f'##{n_Y}')
#print(f'##{c/n_Y:.3f}')

#print(cnf_matrix)

#Plot da matrix
class_names=['Não evasão','Evasão'] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Valor Real')
plt.xlabel('Previsão')
plt.show()

#Métricas de avliação matriz de confusão
target_names = ["Não Evasão","Evasão"]
print(classification_report(Y_test,Y_pred,target_names=target_names))

#Curva ROC
y_pred_proba = logreg.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(Y_test,  y_pred_proba)
auc = metrics.roc_auc_score(Y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()