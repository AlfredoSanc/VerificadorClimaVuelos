import asyncio
import httpx
import time
import logging
from typing import List, Dict, Any

from config import API_KEY

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CONCURRENT_REQUESTS_LIMIT = 10
CACHE_DURATION_SECONDS = 300  #5 minutos

weather_cache: Dict[str, Dict[str, Any]] = {}
semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS_LIMIT)

#Logging del proceso
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def get_weather_for_airport(
    client: httpx.AsyncClient,
    airport: Dict[str, Any]
) -> Dict[str, Any]:
    iata_code = airport['iata_code']
    
    # 1. Revisa el caché
    if iata_code in weather_cache:
        cached_data = weather_cache[iata_code]
        if time.time() - cached_data['timestamp'] < CACHE_DURATION_SECONDS:
            logging.info(f"Cache HIT para {iata_code}")
            return cached_data['data']

    # 2. Limita concurrencia con el semáforo
    async with semaphore:
        logging.info(f"API CALL para {iata_code}")
        params = {
            "lat": airport['latitude'],
            "lon": airport['longitude'],
            "appid": API_KEY,
            "units": "metric",
            "lang": "es"
        }
        
        # 3. Manejo de errores en la petición
        try:
            response = await client.get(API_BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()  # Registro de errores HTTP (4xx o 5xx)
            
            weather_data = response.json()
            processed_data = {
                'iata': iata_code,
                'temperatura': f"{weather_data['main']['temp']}°C",
                'descripcion': weather_data['weather'][0]['description'].capitalize()
            }

            # 4. Guarda en caché
            weather_cache[iata_code] = {
                'timestamp': time.time(),
                'data': processed_data
            }
            return processed_data

        except httpx.HTTPStatusError as e:
            error_msg = f"Error HTTP para {iata_code}: {e.response.status_code}"
            if e.response.status_code == 401:
                error_msg += " (API Key inválida o no configurada)"
            logging.error(error_msg)
            return {'iata': iata_code, 'error': error_msg}
        except httpx.RequestError as e:
            error_msg = f"Error de red para {iata_code}: {e.__class__.__name__}"
            logging.error(error_msg)
            return {'iata': iata_code, 'error': error_msg}
        except Exception as e:
            error_msg = f"Error inesperado para {iata_code}: {e}"
            logging.error(error_msg)
            return {'iata': iata_code, 'error': error_msg}

async def get_weather_for_all_airports(
    airports: List[Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        logging.critical("La API Key de OpenWeatherMap no está configurada. Revisa tu archivo .env")
        return {}

    async with httpx.AsyncClient() as client:
        # Crea una tarea asíncrona para cada aeropuerto
        tasks = [get_weather_for_airport(client, airport) for airport in airports]
        # Ejecuta todas las tareas en paralelo
        results = await asyncio.gather(*tasks)
    
    # Convierte la lista de resultados en un diccionario
    return {result['iata']: result for result in results if result}
