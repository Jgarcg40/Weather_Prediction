import json
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, mean_absolute_error
from keras.models import Sequential
from keras.layers import LSTM, Dense, Bidirectional, Dropout
from keras.optimizers import Adam
import random
import tensorflow as tf
import warnings

warnings.filterwarnings("ignore", message="X does not have valid feature names, but MinMaxScaler was fitted with feature names")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Para ignorar warnings

#semilla aleatoria para que no varien los resultados
seed_value = 42
os.environ['PYTHONHASHSEED'] = str(seed_value)
random.seed(seed_value)
np.random.seed(seed_value)
tf.random.set_seed(seed_value)

# Lista para almacenar todos los datos de los archivos JSON
data_list = []

# Rango de años desde 1930 hasta 2023
rango_anios = list(range(1930, 2024))

# Leer los archivos JSON y almacenar los datos en data_list
for anio in rango_anios:
    archivo_json = f"Datos_AEMET-Leon_{anio}-{anio + 5}.json"
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r') as archivo:
                data = json.load(archivo)
                if 'valores_climatologicos' in data and isinstance(data['valores_climatologicos'], list) and len(
                        data['valores_climatologicos']) > 0:
                    data_list.append(data)
        except Exception as e:
            print(f"Error al procesar el archivo '{archivo_json}': {str(e)}")

# Concatenar los datos de todos los archivos JSON en un único DataFrame
df = pd.DataFrame()
for data in data_list:
    df_temp = pd.DataFrame(data['valores_climatologicos'])
    df = pd.concat([df, df_temp])

# Cambiar comas por puntos
def str_to_float(valor):
    try:
        return float(valor.replace(",", "."))
    except:
        return None

# Preparar los datos secuenciales
n_timesteps = 1 # Utilizaremos datos de 1 día consecutivo para predecir el día siguiente

# Convertir la columna "fecha" a tipo datetime
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')
df['year'] = df['fecha'].dt.year
df['month'] = df['fecha'].dt.month
df['day'] = df['fecha'].dt.day
df["tmed"] = df["tmed"].apply(str_to_float)
df["prec"] = df["prec"].apply(str_to_float)
df["tmin"] = df["tmin"].apply(str_to_float)
df["tmax"] = df["tmax"].apply(str_to_float)
df["dir"] = df["dir"].apply(str_to_float)
df["velmedia"] = df["velmedia"].apply(str_to_float)
df["racha"] = df["racha"].apply(str_to_float)
df["sol"] = df["sol"].apply(str_to_float)
df["presMax"] = df["presMax"].apply(str_to_float)
df["presMin"] = df["presMin"].apply(str_to_float)

# Eliminar las filas que contienen valores nulos
df.dropna(inplace=True)

# Escalar los datos entre 0 y 1
scaler = MinMaxScaler()
columns_to_scale = ['tmed', 'prec', 'tmin', 'tmax', 'dir', 'velmedia', 'racha', 'sol', 'presMax', 'presMin', 'year', 'month', 'day']
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Obtener las características de entrada (X) y las etiquetas (y)
X = df[columns_to_scale].values
y = df[columns_to_scale].shift(-1).values

# Reorganizar los datos secuenciales para tener la estructura requerida para la LSTM
X_seq = []
y_seq = []
for i in range(n_timesteps, len(X) - 1):  # Ajustar la longitud del bucle para excluir el último ejemplo
    X_seq.append(X[i - n_timesteps:i])
    y_seq.append(y[i])

X_seq = np.array(X_seq)
y_seq = np.array(y_seq)

# Dividir los datos en conjuntos de entrenamiento y prueba (80% - 20%)
n_train = int(0.8 * len(X_seq))
X_train, X_test = X_seq[:n_train], X_seq[n_train:]
y_train, y_test = y_seq[:n_train], y_seq[n_train:]


# Construir el modelo RNN con arquitectura LSTM
model = Sequential()
model.add(Bidirectional(LSTM(128, return_sequences=True), input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(64, return_sequences=True))
model.add(LSTM(32))
model.add(Dense(13, activation='linear'))  # 13 unidades para 13 atributos

# Compilar el modelo con un optimizador Adam y una tasa de aprendizaje de 0.001
optimizer = Adam(learning_rate=0.001)
model.compile(loss='mse', optimizer=optimizer)

# Entrenar el modelo
history = model.fit(X_train, y_train, epochs=100, batch_size=128, validation_data=(X_test, y_test))
model.save('modelo_lstm_climatologico.h5')

# Calcular R2-score y MAE en el conjunto de prueba para ver que tal fue el entrenamiento
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print("R2-score en el conjunto de prueba:", r2)
print("MAE en el conjunto de prueba:", mae)

# Datos de entrada proporcionados por el usuario para predecir el día siguiente
input_data = [17.5, 0, 9, 25, 23, 1, 9, 12, 915, 912, 2023, 6, 11] #input de prueba para ver si funciona
input_data_scaled = scaler.transform(np.array(input_data).reshape(1, -1))
input_sequence = input_data_scaled.reshape(1, n_timesteps, len(input_data))
prediction = model.predict(input_sequence)

# Escalar inversamente las predicciones
predicted_data = scaler.inverse_transform(prediction)

# Obtener los nombres de las columnas
columns = ['tmed', 'prec', 'tmin', 'tmax', 'dir', 'velmedia', 'racha', 'sol', 'presMax', 'presMin', 'year', 'month', 'day']

# Crear un DataFrame con los datos predichos
predicted_df = pd.DataFrame(predicted_data, columns=columns)

# Imprimir los datos predichos para el día siguiente
print("Predicción para el día siguiente:")
predicted_df = predicted_df.drop(columns=['year', 'month', 'day']) #eliminar las columnas que no nos interesa predecir
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:,.1f}'.format #se usa 1 solo decimal
print(predicted_df.to_string(index=False))
