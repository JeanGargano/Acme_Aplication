from pymongo import MongoClient
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str
    API_KEY: str

    model_config = {
        "env_file": ".env",
        "validate_by_name": True
    }

settings = Settings()

client = MongoClient(settings.mongodb_url)
db = client["Acme_Aplication"]  # Nombre de la base de datos
