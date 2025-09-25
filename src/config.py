import os
from dotenv import load_dotenv

# Carga el APIKEY desde el archivo .env que está en la raíz del proyecto.
from dotenv import find_dotenv
load_dotenv(find_dotenv())

API_KEY = os.getenv("OPENWEATHER_API_KEY")
