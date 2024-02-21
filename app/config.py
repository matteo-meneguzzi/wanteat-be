from pydantic_settings import BaseSettings

from dotenv import load_dotenv
from os import getenv

load_dotenv()

class CommonSettings(BaseSettings):
    APP_NAME: str = 'Wanteat'
    DEBUG_MODE: bool = False
    
class ServerSettings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    
class DatabaseSettings(BaseSettings):
    DB_URL: str 
    DB_NAME: str 
    
class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass

settings = Settings(
    DB_NAME=getenv("DB_NAME"),
    DB_URL=getenv("DB_URL"),
    HOST=getenv("HOST"),
    PORT=getenv("PORT"),
    DEBUG_MODE=getenv("DEBUG_MODE")
)
