import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="RailForge API")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


@app.get("/")
def root():
    return {"message": "RailForge API rodando"}


@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
        return {"status": "ok", "postgres_version": version}
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar no banco: {str(e)}")
