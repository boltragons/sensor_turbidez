import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

def read_sensor_data(sensor_folder):
    readings_by_grams = {}
    for filename in os.listdir(sensor_folder):
        if filename.endswith('.csv'):
            grams_value = float(filename.split('_')[1].replace('.csv', ''))
            if grams_value > 0:
                file_path = os.path.join(sensor_folder, filename)
                df = pd.read_csv(file_path, sep='|')
                if grams_value not in readings_by_grams:
                    readings_by_grams[grams_value] = []
                readings_by_grams[grams_value].extend(df['leitura'].tolist())
    return readings_by_grams

def perform_linear_regression(readings_by_grams):
    X = np.array(list(readings_by_grams.keys())).reshape(-1, 1)
    y = [np.mean(readings) for readings in readings_by_grams.values()]
    model = LinearRegression().fit(X, y)
    predictions = model.predict(X)
    return model, predictions

def calculate_errors(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    return mae, mse

def plot_regression(X, y, model, title):
    plt.scatter(X, y, color='blue')
    plt.plot(X, model.predict(X), color='red')
    plt.title(title)
    plt.xlabel('Grams')
    plt.ylabel('Sensor Reading')
    plt.show()

# Main Execution
base_directory = ''
all_sensors_data = []

for sensor_num in range(1, 5):
    sensor_folder = os.path.join(base_directory, f'sensor_{sensor_num}')
    if os.path.isdir(sensor_folder):
        readings_by_grams = read_sensor_data(sensor_folder)
        all_sensors_data.append(readings_by_grams)
        model, predictions = perform_linear_regression(readings_by_grams)
        X = np.array(list(readings_by_grams.keys())).reshape(-1, 1)
        y = [np.mean(readings) for readings in readings_by_grams.values()]
        plot_regression(X, y, model, f"Sensor {sensor_num}")
        mae, mse = calculate_errors(y, predictions)
        print(f"Sensor {sensor_num} - MAE: {mae}, MSE: {mse}")

def average_sensor_readings(all_sensors_data):
    # Extrair todos os valores únicos de gramas
    unique_grams = set().union(*[list(sensor_data.keys()) for sensor_data in all_sensors_data])

    average_readings = {}
    for gram in unique_grams:
        gram_readings = []
        for sensor_data in all_sensors_data:
            if gram in sensor_data:
                # Garantir que todas as listas tenham o mesmo tamanho
                # Aqui, escolhemos a menor lista como referência
                min_length = min(len(sensor_data[gram]) for sensor_data in all_sensors_data if gram in sensor_data)
                truncated_readings = sensor_data[gram][:min_length]
                gram_readings.append(truncated_readings)
        
        # Calculando a média ao longo do eixo 0 (média de todas as listas)
        average_readings[gram] = np.mean(gram_readings, axis=0)

    return average_readings

# Calcular a média das leituras de todos os sensores
average_readings = average_sensor_readings(all_sensors_data)

# Converter a média dos dados para o formato necessário para regressão
X_avg = np.array(list(average_readings.keys())).reshape(-1, 1)
y_avg = [np.mean(readings) for readings in average_readings.values()]

# Realizar a regressão linear na média dos sensores
average_model = perform_linear_regression(average_readings)
plot_regression(X_avg, y_avg, average_model, "Average of All Sensors")
average_model, average_predictions = perform_linear_regression(average_readings)
plot_regression(X_avg, y_avg, average_model, "Average of All Sensors")

average_mae, average_mse = calculate_errors(y_avg, average_predictions)
print(f"Average of All Sensors - MAE: {average_mae}, MSE: {average_mse}")