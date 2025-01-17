import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.db_config import settings

user = settings.DB_USER
password = settings.DB_PASSWORD
host = settings.DB_HOST
port = settings.DB_PORT
db = settings.DB_NAME


# Проверка создана ли БД

conn = psycopg2.connect(
    dbname="postgres",
    user=user,
    password=password,
    host=host,
    port=port,
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db}'")
exists = cursor.fetchone()

if not exists:
    # Создаём базу данных
    cursor.execute(f"CREATE DATABASE {db}")
    print(f"Database {db} created successfully.")
else:
    print(f"Database {db} already exists.")

cursor.close()
conn.close()

# Подключение к бд
DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

# отключает ограничение на подключение только в одном потоке
engine = create_engine(DB_URL, echo=True)

# создание сессии
sessionlocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
