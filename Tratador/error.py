import pandas as pd
import os

def calculate_error(df, Y_fs):
    # Calcula o erro absoluto e o erro percentual
    df['erro_absoluto'] = df['leitura'] - Y_fs
    df['erro_percentual'] = (df['erro_absoluto'] / Y_fs) * 100
    return df

# Suponha que Y_fs (valor verdadeiro ou ideal) seja 5.0 para este exemplo
Y_fs = 5.0

# Usage
base_directory = ''  # Substitua pelo caminho correto
for sensor_num in range(1, 5):
    sensor_folder = os.path.join(base_directory, f'sensor_{sensor_num}')
    if os.path.isdir(sensor_folder):
        for filename in os.listdir(sensor_folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(sensor_folder, filename)
                df = pd.read_csv(file_path, sep='|')
                df = calculate_error(df, Y_fs)
                df.to_csv(file_path, sep='|', index=False)
