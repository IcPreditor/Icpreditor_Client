## Importar módulos necessários
import sys
sys.path.insert(1, r'processing')
import processing

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, precision_recall_curve, auc

# Carregar dados processados e fazer a divisão treino/teste
X_train, Y_train, X_test, Y_test, dataframeCopia, feature_cols = processing.getInputOutput(undersampling=False, regressao=True)

# Converter Y_train e Y_test para inteiros para garantir a consistência
Y_train = Y_train.astype(int)
Y_test = Y_test.astype(int)

# Verificar e converter `X_train` e `X_test` para numérico
X_train = X_train.apply(pd.to_numeric, errors='coerce').fillna(0)
X_test = X_test.apply(pd.to_numeric, errors='coerce').fillna(0)

# Treinar o modelo de Regressão Logística
logreg = LogisticRegression(random_state=16, max_iter=100000)
logreg.fit(X_train, Y_train)

# Exibir os coeficientes de cada variável
print("Coeficiente de Regressão das Variáveis:")
coeficientes = logreg.coef_[0]
coeficientes_dict = {feature_cols[i]: coef for i, coef in enumerate(coeficientes)}

# Exibir variáveis ordenadas por impacto (coeficientes normalizados)
coef_norm = {k: abs(v) for k, v in coeficientes_dict.items()}
sorted_coef_norm = sorted(coef_norm.items(), key=lambda x: x[1], reverse=True)
print("\nVariáveis mais impactantes (normalizadas):")
for item, coef in sorted_coef_norm:
    print(f"{item} - [{coef:.5f}]")

# Gráfico de importância das variáveis
plt.figure(figsize=(10, 6))
sns.barplot(x=list(coef_norm.values()), y=list(coef_norm.keys()))
plt.title("Importância das Variáveis na Predição de Evasão")
plt.xlabel("Impacto Normalizado")
plt.ylabel("Variável")
plt.show()

# Fazer previsões no conjunto de teste
Y_pred = logreg.predict(X_test)

# Exibir matriz de confusão
cnf_matrix = metrics.confusion_matrix(Y_test, Y_pred)
class_names = ['Não evasão', 'Evasão']
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# Criar heatmap da matriz de confusão
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Matriz de Confusão', y=1.1)
plt.ylabel('Valor Real')
plt.xlabel('Previsão')
plt.show()

# Exibir métricas de avaliação
target_names = ["Não Evasão", "Evasão"]
print(classification_report(Y_test, Y_pred, target_names=target_names))

# Verificar distribuição das classes em Y_test
print("\nDistribuição das classes em Y_test:")
print(pd.Series(Y_test).value_counts())

# Curva ROC e AUC, somente se ambas as classes estiverem presentes em Y_test
if len(set(Y_test)) > 1:
    y_pred_proba = logreg.predict_proba(X_test)[::, 1]  # Probabilidade da classe positiva (evasão)
    fpr, tpr, _ = metrics.roc_curve(Y_test, y_pred_proba, pos_label=1)
    auc_roc = metrics.roc_auc_score(Y_test, y_pred_proba)

    # Plot da Curva ROC
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label="AUC ROC = {:.2f}".format(auc_roc))
    plt.plot([0, 1], [0, 1], color="navy", linestyle="--")  # Linha diagonal para referência
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("True Positive Rate (TPR)")
    plt.title("Curva ROC")
    plt.legend(loc="lower right")
    plt.grid()
    plt.show()

    # Curva de Precisão-Revocação
    precision, recall, _ = precision_recall_curve(Y_test, y_pred_proba)
    pr_auc = auc(recall, precision)
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, label="AUC PR = {:.2f}".format(pr_auc))
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Curva de Precisão-Revocação")
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()
else:
    print("O conjunto de teste não contém ambas as classes, portanto a curva ROC e a Curva de Precisão-Revocação não podem ser exibidas.")

# Análise por Subgrupos: Exemplo de taxa de evasão por faixa etária
#todo: ajustar os dados do gráfico.

# age_evasion = dataframeCopia.groupby("idade")["evaded"].mean()
# plt.figure(figsize=(10, 6))
# sns.barplot(x=age_evasion.index, y=age_evasion.values)
# plt.title("Taxa de Evasão por Faixa Etária")
# plt.xlabel("Faixa Etária")
# plt.ylabel("Taxa de Evasão")
# plt.show()


# # Análise de Confusão com Limiar Customizado
# threshold = 0.3  # Exemplo de limiar customizado
# Y_pred_custom = (y_pred_proba >= threshold).astype(int)
# cnf_matrix_custom = metrics.confusion_matrix(Y_test, Y_pred_custom)

# sns.heatmap(pd.DataFrame(cnf_matrix_custom), annot=True, cmap="YlGnBu", fmt='g')
# plt.title(f"Matriz de Confusão com Limiar {threshold}")
# plt.xlabel("Previsão")
# plt.ylabel("Valor Real")
# plt.show()

# Verificação de Overfitting
train_accuracy = logreg.score(X_train, Y_train)
test_accuracy = logreg.score(X_test, Y_test)
print(f"\nAcurácia no Treinamento: {train_accuracy:.2f}")
print(f"Acurácia no Teste: {test_accuracy:.2f}")

# Comparação para possíveis sinais de overfitting
if train_accuracy - test_accuracy > 0.1:
    print("Possível overfitting: a acurácia no treino é significativamente maior que no teste.")
else:
    print("Modelo geral bem ajustado entre treino e teste.")
