# gravar_csv.py
#
# Descrição: Lê a porta serial e grava
#            os valores em um .csv.
#

import serial
import csv

NUMERO_AMOSTRAS = 5000

# Dados da Porta Serial
porta = 'COM3'
baudrate = 115200
timeout = 1

ntu = input("Digite a quantidade de 'NTU' da amostra: ")
arquivo = f'amostra_{ntu}.csv'
porta_serial = serial.Serial(port, baudrate, timeout=timeout)
try:
    with open(arquivo, mode='w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv, delimiter='|', quoting=csv.QUOTE_NONE)
        escritor_csv.writerow(['ntu', 'sensor', 'leitura'])

        for i in range(NUMERO_AMOSTRAS)
            dados = porta_serial.readline().decode().strip()
            if dados:
                dados = dados.replace('\n', '').replace('\r', '')
                numero_sensor, valor_lido = map(int, dados.split(','))
                print(f'{ntu}|{numero_sensor}|{valor_lido}')
                escritor_csv.writerow([ntu,numero_sensor,valor_lido])
                
except KeyboardInterrupt:
    pass
    
porta_serial.close()
