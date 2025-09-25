# Verificador de Clima para Vuelos ✈️ 🌤️


## Módulos principales:


- `main.py`: El punto de entrada y orquestador principal de la aplicación. Controla el flujo de ejecución.
- `data_processor.py`: Se encarga de leer y procesar el archivo dataset.csv para extraer una lista optimizada de aeropuertos únicos.
- `weather_client.py`: Contiene toda la lógica para comunicarse con la API de OpenWeatherMap, incluyendo la concurrencia, el caché y el manejo de errores.
- `config.py`: Gestiona la carga de la configuración desde el archivo .env.


## Características Principales


* **Alto Rendimiento Asíncrono:** Utiliza asyncio y httpx para realizar múltiples llamadas a la API de OpenWeatherMap de manera concurrente, reduciendo drásticamente el tiempo de ejecución.
* **Optimización de Consultas:** Procesa el dataset inicial para obtener una lista de aeropuertos únicos, evitando llamadas redundantes a la API.
* **Control de Concurrencia:** Implementa un Semaphore para limitar el número de peticiones simultáneas, evitando así el bloqueo por "rate limiting" de la API.
* **Caché en Memoria:** Guarda los resultados de la API en un caché temporal (15 minutos) para reutilizar datos y acelerar ejecuciones con datos repetidos dentro de una misma sesión.
* **Configuración Segura:** Gestiona las claves de API de forma segura a través de variables de entorno con un archivo .env.


## Instalación


1. Prerrequisitos
```
Python 3.7 o superior
Pip (gestor de paquetes de Python)
```

2. Instala las dependencias:

```
pip install -r requirements.txt
```

3. Colocar APIKEY en `.env`
```
OPENWEATHER_API_KEY="TU_APIKEY"
```
