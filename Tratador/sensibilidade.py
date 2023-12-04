import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

def calculate_sensitivity_and_plot(sensor_folder, sensor_number):
    gramas = []
    mean_readings = []
    
    for filename in os.listdir(sensor_folder):
        if filename.startswith('amostra_') and filename.endswith('.csv'):
            grams_value = float(filename.split('_')[1].replace('.csv', ''))
            if grams_value > 0:  # Verifica se o valor em gramas é maior que 0
                gramas.append(grams_value)
                
                file_path = os.path.join(sensor_folder, filename)
                df = pd.read_csv(file_path, sep='|')
                mean_readings.append(df['leitura'].mean())

    X = np.array(mean_readings).reshape(-1, 1)
    y = np.array(gramas)
    
    model = LinearRegression()
    model.fit(X, y)
    sensitivity = model.coef_[0]

    plt.figure()
    plt.scatter(X, y, color='blue', label='Médias das Leituras')
    plt.plot(X, model.predict(X), color='red', label=f'Inclinação (Sensibilidade): {sensitivity:.4f}')
    plt.title(f'Sensibilidade do Sensor {sensor_number}')
    plt.xlabel('Gramas')
    plt.ylabel('Média das Leituras')
    plt.legend()
    plt.savefig(f'{sensor_folder}/sensibilidade_sensor_{sensor_number}.png')
    plt.close()

base_directory = ''

for sensor_num in range(1, 5):
    sensor_folder = os.path.join(base_directory, f'sensor_{sensor_num}')
    if os.path.isdir(sensor_folder):
        calculate_sensitivity_and_plot(sensor_folder, sensor_num)
