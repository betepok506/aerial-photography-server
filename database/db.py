import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", 'postgres')
DATABASE_URI = os.getenv('DATABASE_URI', 'localhost:6500')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@{DATABASE_URI}/{POSTGRES_PASSWORD}"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()