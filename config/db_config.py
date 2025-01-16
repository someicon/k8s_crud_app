from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DB_HOST: str = "localhost"  # Хост базы данных (по умолчанию localhost)
    DB_PORT: str = 5432  # Порт базы данных (по умолчанию PostgreSQL)
    DB_NAME: str
    DB_USER: str  # Имя пользователя базы данных
    DB_PASSWORD: str  # Пароль пользователя базы данных

    class Config:
        env_file = Path(__file__).resolve().parent.parent / '.env'


settings = Settings()  # Загружаем настройки
