import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True) # O banco em si
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Uma sessão de conexão. Quando eu for fazer .add, .commit, etc... eu vou ter uma seção conectada ao banco (que é o engine)
Base = declarative_base() 


def get_db():
    """Dependency do FastAPI para injetar uma sessão de banco por request."""
    db = SessionLocal()
    try:
        yield db # O finally é sempre executado. Quem chama não precisa gerenciar fechamentos
    finally:
        db.close()
