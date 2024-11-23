from typing import ClassVar
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: ClassVar[int]= 60 * 24 * 2  # 2 days
    REFRESH_TOKEN_EXPIRE_MINUTES: ClassVar[int] = 60 * 24 * 15 # 7 days
    ALGORITHM: ClassVar[str] = "HS256"
    JWT_SECRET_KEY: ClassVar[str] = os.environ['JWT_SECRET_KEY']     # should be kept secret
    JWT_REFRESH_SECRET_KEY: ClassVar[str] = os.environ['JWT_REFRESH_SECRET_KEY']      # should be kept secret
    SUPER_ADMIN_PASSWORD: ClassVar[str] = os.environ['SUPER_ADMIN_PASSWORD']
    FIRST_ADMIN_PASSWORD: ClassVar[str] = os.environ['FIRST_ADMIN_PASSWORD']

    
settings = Settings()

