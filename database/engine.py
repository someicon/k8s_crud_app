from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db_config import settings

user = settings.DB_USER
password = settings.DB_PASSWORD
host = settings.DB_HOST
port = settings.DB_PORT
db = settings.DB_NAME


DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

# отключает ограничение на подключение только в одном потоке
engine = create_engine(DB_URL, echo=True)

# создание сессии
sessionlocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
