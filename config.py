import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_2GIS: str = os.getenv('API_KEY_2GIS')
HOST: str = os.getenv('HOST', default='0.0.0.0')
PORT: int = int(os.getenv('PORT', default=8000))
