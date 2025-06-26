from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # например: "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем все таблицы в базе данных (если еще не созданы)
def init_db():
    from .models import Base
    Base.metadata.create_all(bind=engine)
