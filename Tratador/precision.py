import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_precision(df):
    mean_reading = df['leitura'].mean()
    df['precisao'] = 1 - abs(df['leitura'] - mean_reading) / mean_reading
    return df

def plot_precision_histogram(df, sensor_number):
    plt.figure()
    # Agrupa por 'gramas' e obtém a média da precisão para cada grupo
    precision_by_gramas = df.groupby('gramas')['precisao'].mean()
    precision_by_gramas.plot(kind='bar')
    plt.title(f'Histograma de Precisão para o Sensor {sensor_number}')
    plt.xlabel('Gramas')
    plt.ylabel('Precisão Média')
    plt.savefig(f'histograma_precisao_sensor_{sensor_number}.png')
    plt.close()

# Usage
base_directory = ''  # Substitua pelo caminho correto
for sensor_num in range(1, 5):
    sensor_folder = os.path.join(base_directory, f'sensor_{sensor_num}')
    if os.path.isdir(sensor_folder):
        all_precisions = []  # Lista para armazenar todos os dados de precisão
        for filename in os.listdir(sensor_folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(sensor_folder, filename)
                df = pd.read_csv(file_path, sep='|')
                df = calculate_precision(df)
                all_precisions.append(df)
                df.to_csv(file_path, sep='|', index=False)
        # Combina todos os DataFrames em um único DataFrame
        if all_precisions:  # Verifica se a lista não está vazia
            df_precisions = pd.concat(all_precisions)
            plot_precision_histogram(df_precisions, sensor_num)
