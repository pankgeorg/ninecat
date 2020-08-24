"""Import settings from environment"""
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URI = os.getenv("DATABASE_URI")
MAPSKEY = os.getenv("MAPSKEY")
OPENWEATHERKEY = os.getenv("OPENWEATHERKEY")
ENVIRONMENT = os.getenv("ENV")
LOG_LEVEL = os.getenv("LOG_LEVEL")
LOG_FILE = f"ninecat_data.{datetime.now().date()}.log"
