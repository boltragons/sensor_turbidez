# calc_medias.py
#
# Descrição: Calcula a média das amostras
#            dos dados nos arquivos .csv.
#

import os
import pandas as pd

# Função para calcular a média dos valores da terceira coluna com base na segunda coluna
def calcular_media_por_sensor(dados):
    df = pd.DataFrame([linha.split('|') for linha in dados], columns=['ntu', 'sensor', 'leitura'])
    df['sensor'] = pd.to_numeric(df['sensor'])
    df['leitura'] = pd.to_numeric(df['leitura'])
    media_por_sensor = df.groupby('sensor')['leitura'].mean().to_dict()
    return media_por_sensor

# Função para ler o arquivo CSV e retornar os dados a partir da segunda linha em uma lista de linhas
def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        # Lê todas as linhas do arquivo
        linhas = arquivo.readlines()
        # Ignora a primeira linha (cabeçalho) e retorna as linhas restantes
        return linhas[1:]

PASTA_AMOSTRAS = 'amostras/'
# Lista para armazenar os resultados
resultados = []

# Percorre cada arquivo na pasta de dados
for nome_arquivo in os.listdir(PASTA_AMOSTRAS):
    if nome_arquivo.endswith('.csv'):
        caminho_arquivo = os.path.join(PASTA_AMOSTRAS, nome_arquivo)
        # Lê os dados do arquivo CSV a partir da segunda linha
        dados = ler_arquivo(caminho_arquivo)
        # Calcula a média da terceira coluna com base na segunda coluna para cada arquivo
        media_por_sensor = calcular_media_por_sensor(dados)
        # Extrai o valor da coluna 'ntu' do arquivo atual (o mesmo valor para todo o arquivo)
        amostra = dados[0].split('|')[0]
        # Salva o resultado em uma lista
        resultados.append([amostra] + [media_por_sensor.get(sensor, 0) for sensor in [1, 2]])

# Salva o DataFrame em um arquivo CSV de resultados
pd.DataFrame(resultados, columns=['amostra', 'media_sensor01', 'media_sensor02'])
    .to_csv('amostras/medias_amostras.csv', index=False)
