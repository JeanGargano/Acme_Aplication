from pydantic_settings import BaseSettings
from pymongo import MongoClient

class Settings(BaseSettings):
    mongodb_url: str

    class Config:

        env_file = ".env"

settings = Settings()

client = MongoClient(settings.mongodb_url)
db = client["Acme_Aplication"]