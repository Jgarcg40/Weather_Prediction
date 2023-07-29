import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import data_Today #import de la clase data_today

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Para ignorar los mensajes de nivel INFO

# Cargar el modelo desde el archivo .h5
model = load_model('modelo_lstm_climatologico.h5')

# Función para obtener la predicción y mostrarla en la interfaz
def obtener_prediccion():
    fecha_actual = datetime.now()  # Obtener día de hoy para pasar al modelo
    year = fecha_actual.year
    month = fecha_actual.month
    day = fecha_actual.day

    # Datos de entrada proporcionados por aemet
    input_data = [data_Today.tmed(), data_Today.prec(), data_Today.tmin(), data_Today.tmax(), data_Today.dir(), data_Today.velmedia(), data_Today.racha(), data_Today.sol(), data_Today.presMax(), data_Today.presMin(), year, month, day]

    scaler = MinMaxScaler()
    input_data_scaled = scaler.fit_transform(np.array(input_data).reshape(1, -1))
    n_timesteps = 1

    input_sequence = input_data_scaled.reshape(1, n_timesteps, len(input_data))
    prediction = model.predict(input_sequence)
    predicted_data = scaler.inverse_transform(prediction)

    columns = ['tmed', 'precip', 'tmin', 'tmax', 'direcviento', 'velmedia', 'rachamax', 'solH', 'presMax', 'presMin', 'year', 'month', 'day']

    predicted_df = pd.DataFrame(predicted_data, columns=columns)
    predicted_df = predicted_df.drop(columns=['year', 'month', 'day', 'solH'])
    pd.set_option('display.max_columns', None)
    pd.options.display.float_format = '{:,.1f}'.format

    # Mostrar la predicción en la interfaz
    resultado_text.delete(1.0, tk.END)  # Limpiar el contenido anterior
    resultado_text.insert(tk.END, "Predicción para el día siguiente:\n")
    resultado_text.insert(tk.END, predicted_df.to_string(index=False))

# Crear la ventana principal
root = tk.Tk()
root.title("Predicción del día de mañana")

# Etiqueta
fecha_actual_etiqueta = datetime.now()
fecha_manana = fecha_actual_etiqueta + timedelta(days=1)
etiqueta = ttk.Label(root, text="Pulsa el botón para ver la predicción de los datos meteorológicos del día de mañana " + fecha_manana.strftime("%d/%m/%Y"))
etiqueta.pack(pady=10)

# Botón
boton_prediccion = ttk.Button(root, text="Ver Predicción", command=obtener_prediccion)
boton_prediccion.pack(pady=5)

# Cuadro de texto para mostrar el resultado
resultado_text = tk.Text(root)  #
resultado_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


root.mainloop()