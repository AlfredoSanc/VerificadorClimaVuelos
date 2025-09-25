import asyncio
import pandas as pd
import time
from data_processor import get_unique_airports
from weather_client import get_weather_for_all_airports

DATASET_FILE = 'dataset.csv'

def display_results(flights_df: pd.DataFrame, weather_data: dict):
    print("\n" + "="*80)
    print("              RESULTADOS DEL CLIMA PARA CADA VUELO")
    print("="*80 + "\n")

    # Mapea los datos del clima a los vuelos de origen y destino
    flights_df['origin_weather'] = flights_df['origin_iata_code'].map(weather_data)
    flights_df['destination_weather'] = flights_df['destination_iata_code'].map(weather_data)

    for index, row in flights_df.iterrows():
        origin_code = row['origin_iata_code']
        dest_code = row['destination_iata_code']
        airline = row['airline']
        flight_num = row['flight_num']

        # Formatea la información del clima para mostrarla
        origin_weather_info = weather_data.get(origin_code, {'error': 'No disponible'})
        dest_weather_info = weather_data.get(dest_code, {'error': 'No disponible'})

        origin_temp = origin_weather_info.get('temperatura', 'N/A')
        origin_desc = origin_weather_info.get('descripcion', origin_weather_info.get('error', 'N/A'))

        dest_temp = dest_weather_info.get('temperatura', 'N/A')
        dest_desc = dest_weather_info.get('descripcion', dest_weather_info.get('error', 'N/A'))

        # Imprime la línea de resultado
        print(f"✈️  Vuelo {airline} {flight_num}: {origin_code} -> {dest_code}")
        print(f"    - Origen ({origin_code}): {origin_temp}, {origin_desc}")
        print(f"    - Destino ({dest_code}): {dest_temp}, {dest_desc}")
        print("-" * 50)

async def main():
    start_time = time.time()
    
    # 1. Lee y procesa el dataset para obtener aeropuertos únicos
    print(f"1. Procesando el archivo de datos '{DATASET_FILE}'...")
    unique_airports = get_unique_airports(DATASET_FILE)
    if not unique_airports:
        print("No se encontraron aeropuertos para procesar. Terminando ejecución.")
        return
        
    print(f"   -> Se encontraron {len(unique_airports)} aeropuertos únicos.")

    # 2. Obtiene el clima para todos los aeropuertos de forma concurrente
    print("\n2. Obteniendo información del clima...")
    weather_results = await get_weather_for_all_airports(unique_airports)
    if not weather_results:
        print("No se pudo obtener la información del clima. Terminando ejecución.")
        return

    # 3. Carga el dataset original para mostrar los resultados
    try:
        flights_df = pd.read_csv(DATASET_FILE)
    except FileNotFoundError:
        print(f"Error al volver a cargar '{DATASET_FILE}' para mostrar resultados.")
        return
        
    # 4. Muestra los resultados finales
    display_results(flights_df, weather_results)
    end_time = time.time()
    print("\n" + "="*50)
    print(f"Proceso completado en {end_time - start_time:.2f} segundos.")
    print("="*50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())