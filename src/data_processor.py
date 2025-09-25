import pandas as pd
from typing import List, Dict, Any

def get_unique_airports(file_path: str) -> List[Dict[str, Any]]:
    try:
        df = pd.read_csv(file_path)

        # Extrae aeropuertos de origen y renombra las columnas para unificarlas
        origins = df[['origin_iata_code', 'origin_latitude', 'origin_longitude']].copy()
        origins.rename(columns={
            'origin_iata_code': 'iata_code',
            'origin_latitude': 'latitude',
            'origin_longitude': 'longitude'
        }, inplace=True)

        # Extrae los aeropuertos de destino y renombra las columnas
        destinations = df[['destination_iata_code', 'destination_latitude', 'destination_longitude']].copy()
        destinations.rename(columns={
            'destination_iata_code': 'iata_code',
            'destination_latitude': 'latitude',
            'destination_longitude': 'longitude'
        }, inplace=True)

        # Combina ambos, elimina los duplicados y registros sin IATA
        all_airports = pd.concat([origins, destinations], ignore_index=True)
        all_airports.dropna(subset=['iata_code'], inplace=True)
        unique_airports = all_airports.drop_duplicates(subset=['iata_code'])

        # DataFrame a diccionario
        return unique_airports.to_dict('records')

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
        return []
    except Exception as e:
        print(f"Ocurrió un error inesperado al procesar el archivo: {e}")
        return []
