import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
FILE_LOCATION = os.getenv("FILE_LOCATION")
