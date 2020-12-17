# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 19:54:52 2020

@author: juan
"""


from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import keras
import keras.backend as K
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import seaborn as sns
import warnings

#leitura das cotações
base = pd.read_csv('ABEV3.SA.csv')

#Mostra quantidade de dados 'NULL'
base.isnull().sum()

#remove os dados 'NULL'
base.dropna(inplace=True)
#base_treinamento recebe apenas os valores de Abertura
base_treinamento = base.iloc[:,1:2].values

#os dados serão normalizados para melhorar a performance e dimensionalidade (escala entre 0 e 1)
from sklearn.preprocessing import MinMaxScaler
min_scaler = MinMaxScaler(feature_range=(0,1))
base_treinamento_normalizado = min_scaler.fit_transform(base_treinamento)
base_treinamento_normalizado[0:5]

#Utilizaremos uma janela de 120 dias anteriores da base de treinamento para nossas previsões.
previsores = []
preco_real = []

for i in range(500, len(base)):
    previsores.append(base_treinamento_normalizado[i-500:i,0])
    preco_real.append(base_treinamento_normalizado[i,0])
    
print('Tamanho do Dataset criado de previsores', len(previsores))
print('Tamanho do Dataset criado de preco_real', len(preco_real))

#Os dados serão transformados para o formato do Numpy
previsores, preco_real = np.array(previsores), np.array(preco_real)
print('Formato Previsores', previsores.shape)
print('Formato Preco_real', preco_real.shape)

#Converter o formato para o padrão Keras
previsores = np.reshape(previsores, newshape = (previsores.shape[0], previsores.shape[1], 1))
previsores.shape

#Criação do regressor com Rede Neural Recorrente
regressor = Sequential()
regressor.add(LSTM(units = 100, return_sequences = True, input_shape = (previsores.shape[1], 1)))

regressor.add(Dropout(0.3))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.3))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.3))

regressor.add(LSTM(units = 50, return_sequences = False))
regressor.add(Dropout(0.3))

regressor.add(Dense(units=1, activation='linear'))

regressor.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])

#Treinamento da Rede Neural
regressor.fit(previsores, preco_real, epochs=5, batch_size=32)

#Recebe os valores reais das próximas 23 cotações
base_teste = pd.read_csv('ABEV3.SA_teste.csv')
#Remove os possíveis valores 'NULL'
base_teste.isnull().sum().max()
base_teste.dropna(inplace=True)
#Recebe a base mais os valores das proximas cotações
base_completa = pd.concat((base['Open'], base_teste['Open']), axis=0)
preco_real_teste = base_teste.iloc[:,1:2].values
preco_real_teste

#entradas recebe a base_completa[len(base_completa)-113:]
entradas = base_completa[len(base_completa) - len(base_teste) - 90:].values
len(entradas)

#Normalizar dados de entrada
entradas = entradas.reshape(-1,1)
entradas = min_scaler.transform(entradas)

X_teste = []
for i in range(90, 113):
    X_teste.append(entradas[i-90:i,0])
X_teste = np.array(X_teste)
X_teste = np.reshape(X_teste, newshape=(X_teste.shape[0], X_teste.shape[1], 1))

#Faz a predição da próxima cotação
previsoes = regressor.predict(X_teste)
#Inverte padronização dos dados para melhor vizualização
previsoes = min_scaler.inverse_transform(previsoes)

#Criação de um array de duas colunas (preço real e as previsões para comparação)
quadro_previsao = np.concatenate((preco_real_teste, previsoes), axis= 1)

#Quadro convertido em DataFrame para melhor visualização e adicionado uma segunda coluna 'Erro'
quadro_previsao = pd.DataFrame(quadro_previsao, columns=['Preco_real', 'Previsao'])
quadro_previsao['Erro'] = quadro_previsao['Preco_real'] - quadro_previsao['Previsao']
quadro_previsao

print('Media Preco Reais', preco_real_teste.mean())
print('Media Previsoes', previsoes.mean())
print('Diferenca da media entre o valor_real e a previsao', round(previsoes.mean() - preco_real_teste.mean(), 2))

plt.figure(figsize=(10,8))
plt.plot(preco_real_teste, color='red', label='Preco_Real')
plt.plot(previsoes, color = 'blue', label = 'Previsoes')
plt.title('Previsao de preco da PETR4')
plt.legend()
plt.xlabel('Periodo')
plt.ylabel('Precos')
plt.show