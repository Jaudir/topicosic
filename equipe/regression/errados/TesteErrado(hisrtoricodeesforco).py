import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn import linear_model


casas = fetch_california_housing()

print(casas.DESCR)

tabela = pd.DataFrame(casas.data)
tabela.columns = casas.feature_names
print (tabela.head())

tabela['HouseAge'] = casas.target

#seleciona duas colunas
X = tabela[["MedInc", "AveOccup"]]
print(X)
#separa em dois conjuntos, um para treinamento e outro para validação (20 últimos)
X_train = X[:-2000]
X_test = X[-2000:]

#print(X_t["RM"])
y_train = tabela["HouseAge"][:-2000]
y_test = tabela["HouseAge"][-2000:]

regr = linear_model.LinearRegression()

# treina o modelo
regr.fit(X_train, y_train)

# faz a predição
y_pred = regr.predict(X_test)

a = regr.coef_[0]
a2 = regr.coef_[1]
b = regr.intercept_
# coeficientes a
print('Coeficientes: \n', a, a2)
#intercepto b
print('Coeficientes: \n', b)
#y = 0.413*MedInc + -0.007*AveOccup + 0.523


#prediz manualmente os valores com base nos coeficientes encontrados na regressao
y_teste = a*X_test["MedInc"] - a2*X_test["AveOccup"]+ b

#exibe o valor predito manualmente y_teste, que começa de 18640
#exibe o valor real y_t
#exibe o valor predito pela regressão linear
print(y_teste[18640], y_train[0],y_pred[0])


#plota todos os valores de validação
plt.scatter(X_test["AveOccup"], y_test,  color='black')
plt.scatter(X_test["AveOccup"], y_pred, color='blue')
plt.legend(["Real", "Predito"])
