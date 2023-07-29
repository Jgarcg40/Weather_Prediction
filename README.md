Aplicación que utiliza la arquitectura LSTM para identificar patrones temporales en los datos meteorológicos diarios historicos obtenidos de AEMET. 
A este modelo, una vez entrenado, se le pasarán los datos meteorológicos del día actual y con ellos mostrará una predicción de esos mismos datos para el día siguiente en una interfaz gráfica simple de python.

MANUAL DE EJECUCIÓN

Lo primero será descargar este repositorio, entrar a la carpeta de Train y en el archivo AEMET_API_Historico-Leon.py poner tu API key de AEMET, después ejecuta el main.py, esto hará que se descargue en archivos json todos los datos meteorológicos desde 1963 hasta 2023 para la estación meteorologica de León (se puede cambiar la estación pero hay que tener cuidado con el formato de los datos) y también comenzará a entrenar el modelo.

Una vez finalizado el entrenamiento nos dará una archivo .h5, debemos moverlor a la carpeta "Application with interface" y una vez ahí pondremos de nuevo nuestra API key en el archivo data_Today.py y ejecutar el archivo WeatherPrediction.py, en el cual saldrá una interfaz simple que nos mostrará la predicción de los datos meteorológicos de mañana. Es recomendable ejecutar el programa a las 23:00 de la noche ya que si no extraerá solo la mitad de los datos del día actual o menos, esto es por que la aplicación usa los datos de AEMET del día actual para hacer la predicción.

