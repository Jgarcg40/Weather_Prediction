# Predicción Meteorológica con LSTM (Realizado en 2023)

Aplicación que utiliza la arquitectura LSTM (Long Short-Term Memory) para identificar patrones temporales en datos meteorológicos históricos obtenidos a través de la API de AEMET (Agencia Estatal de Meteorología). El modelo, una vez entrenado, recibe los datos meteorológicos del día actual y genera una predicción para el día siguiente, mostrándola en una interfaz gráfica simple.

## Características

- Extracción de datos históricos desde 1963 hasta la actualidad de la API de AEMET
- Entrenamiento de modelo LSTM para reconocer patrones climáticos
- Predicción de variables meteorológicas como temperatura, precipitación, viento, etc.
- Interfaz gráfica simple para visualizar las predicciones

## Estructura del Proyecto

El proyecto está dividido en dos secciones principales:

- **Train**: Contiene los scripts para la descarga de datos históricos y el entrenamiento del modelo
- **Application with interface**: Contiene la aplicación con interfaz gráfica que utiliza el modelo entrenado

## Requisitos

- Python 3.6 o superior
- Acceso a internet
- API key de AEMET (puede obtenerse en https://opendata.aemet.es/)
- Bibliotecas: TensorFlow, Keras, Pandas, NumPy, Scikit-learn, Tkinter

## Manual de Instalación y Uso

### 1. Descarga y Configuración

1. Clona o descarga este repositorio
2. Navega hasta la carpeta del proyecto
3. Instala las dependencias necesarias:
   ```
   pip install tensorflow keras pandas numpy scikit-learn aemet-api
   ```

### 2. Entrenamiento del Modelo

1. Abre el archivo `Train/AEMET_API_Historico-Leon.py` y añade tu API key de AEMET en la variable `api_key`
2. Ejecuta el script principal de entrenamiento:
   ```
   cd Train
   python main.py
   ```
   Este proceso realizará:
   - Descarga de datos meteorológicos históricos desde 1963 hasta el presente para la estación meteorológica de León
   - Procesamiento de datos y entrenamiento del modelo LSTM
   - Generación del archivo `modelo_lstm_climatologico.h5` con el modelo entrenado

### 3. Ejecutar la Aplicación de Predicción

1. Copia el archivo `modelo_lstm_climatologico.h5` generado en el paso anterior a la carpeta "Application with interface"
2. Abre el archivo `Application with interface/data_Today.py` y añade tu API key de AEMET en la variable `api_key`
3. Ejecuta la aplicación:
   ```
   cd "Application with interface"
   python WeatherPrediction.py
   ```
4. Haz clic en el botón "Ver Predicción" para obtener la predicción del día siguiente

## Notas Importantes

- Para obtener resultados óptimos, se recomienda ejecutar la aplicación después de las 23:00, cuando AEMET ya ha registrado todos los datos del día actual
- La aplicación está configurada para la estación meteorológica de León (código 2661). Si deseas usar otra estación, deberás modificar:
  - En `Train/AEMET_API_Historico-Leon.py`: Modificar el diccionario `estacion` (líneas 10-13) con el nombre e indicativo de tu estación
  - En `Application with interface/data_Today.py`: Cambiar el código de estación en la URL de la solicitud (línea 15)
  - Puedes consultar los códigos de estaciones disponibles en: https://opendata.aemet.es/centrodedescargas/productosAEMET
- El modelo necesita ser reentrenado periódicamente para mantener su precisión

## Limitaciones

- La precisión de las predicciones depende de la calidad y completitud de los datos proporcionados por AEMET
- El modelo está optimizado para patrones climáticos específicos de León; su uso en otras regiones puede requerir ajustes

