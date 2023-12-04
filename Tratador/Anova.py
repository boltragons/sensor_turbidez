import os
import pandas as pd
from scipy.stats import f_oneway

def perform_anova(sensor_folder):
    # Dicionário para coletar todas as leituras para cada valor de gramas
    readings_by_grams = {}

    # Coletar todas as leituras dos arquivos CSV
    for filename in os.listdir(sensor_folder):
        if filename.endswith('.csv'):
            grams_value = float(filename.split('_')[1].replace('.csv', ''))
            if grams_value > 0:  # Ignorar amostras com 0 gramas
                file_path = os.path.join(sensor_folder, filename)
                df = pd.read_csv(file_path, sep='|')
                if grams_value not in readings_by_grams:
                    readings_by_grams[grams_value] = []
                readings_by_grams[grams_value].extend(df['leitura'].tolist())

    # Preparar listas de leituras para a ANOVA
    groups = list(readings_by_grams.values())

    # Executar ANOVA
    F_statistic, p_value = f_oneway(*groups)
    print(f"ANOVA F-Statistic: {F_statistic}, p-value: {p_value}")

# Usage
base_directory = ''

for sensor_num in range(1, 5):
    sensor_folder = os.path.join(base_directory, f'sensor_{sensor_num}')
    if os.path.isdir(sensor_folder):
        print(f"Performing ANOVA for Sensor {sensor_num}")
        perform_anova(sensor_folder)
