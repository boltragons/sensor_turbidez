# calc_medias.py
#
# Descrição: Calcula a média das amostras
#            dos dados nos arquivos .csv.
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Substitua 'caminho/do/arquivo.csv' pelo caminho correto do seu arquivo CSV
data = pd.read_csv('medias_amostras.csv')

x_columns = data.columns[1:]  # Colunas das tensões em mV
y_column = data.columns[0]    # Coluna da quantidade de NTU

equations = []  # Lista para armazenar as equações das regressões

for x_col in x_columns:
    x = data[x_col].values.reshape(-1, 1)
    y = data[y_column].values

    # Criando o modelo de regressão linear
    model = LinearRegression()
    model.fit(x, y)

    # Coeficiente angular e linear da reta
    coef_angular = model.coef_[0]
    coef_linear = model.intercept_

    # Armazenando a equação da reta na lista
    equation = f'{coef_angular:.2f}x + {coef_linear:.2f}'
    equations.append(equation)

# Criando uma figura com 2x2 subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Plot dos gráficos de dispersão e das retas de regressão
for i, ax in enumerate(axs.ravel()):
    x = data[x_columns[i]].values
    y = data[y_column].values

    # Criando o modelo de regressão linear
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)

    # Plot dos pontos de dados
    ax.scatter(x, y, label='Leituras', color='blue', alpha=0.7)

    # Plot da reta de regressão
    ax.plot(x, model.predict(x.reshape(-1, 1)), color='red', label='Reta de Regressão')

    # Configurações do gráfico
    ax.set_title(f'Círculo {i+1}')
    ax.set_xlabel('Tensão (mV)')
    ax.set_ylabel('Turbidez (NTU)')
    ax.legend()

# Ajustar o espaçamento entre os gráficos
plt.tight_layout()

# Exibir a imagem
plt.show()

for i in range(4):
    print(equations[i])
