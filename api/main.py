from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import Base, engine, get_db
import os

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas que ainda não existem no banco.
    Base.metadata.create_all(bind=engine)
    yield


router = APIRouter()
app = FastAPI(title="RailForge API", lifespan=lifespan)

if os.getenv("ENVIRONMENT", "dev") == "dev":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def root():
    return {"message": "RailForge API rodando"}


@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()

        return {
            "status": "ok",
            "postgres_version": version,
        }

    except OperationalError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao conectar no banco: {str(e)}",
        )


# ==================== Station ====================

@router.post(
    "/stations",
    response_model=schemas.StationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_station(
    data: schemas.StationCreate,
    db: Session = Depends(get_db),
):
    return crud.create_station(db, data)


@router.get(
    "/stations",
    response_model=list[schemas.StationOut],
)
def list_stations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_stations(db, skip=skip, limit=limit)


@router.get(
    "/stations/by-position",
    response_model=list[schemas.StationOut],
)
def stations_by_position(
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    db: Session = Depends(get_db),
):
    return crud.get_stations_in_range(
        db,
        x_min,
        x_max,
        y_min,
        y_max,
    )


@router.get(
    "/stations/{station_id}",
    response_model=schemas.StationOut,
)
def get_station(
    station_id: int,
    db: Session = Depends(get_db),
):
    station = crud.get_station(db, station_id)

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found",
        )

    return station


@router.patch(
    "/stations/{station_id}",
    response_model=schemas.StationOut,
)
def update_station(
    station_id: int,
    data: schemas.StationUpdate,
    db: Session = Depends(get_db),
):
    station = crud.update_station(db, station_id, data)

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found",
        )

    return station


@router.delete(
    "/stations/{station_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_station(
    station_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_station(db, station_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Station not found",
        )


# ==================== Line ====================

@router.post(
    "/lines",
    response_model=schemas.LineOut,
    status_code=status.HTTP_201_CREATED,
)
def create_line(
    data: schemas.LineCreate,
    db: Session = Depends(get_db),
):
    return crud.create_line(db, data)


@router.get(
    "/lines",
    response_model=list[schemas.LineOut],
)
def list_lines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_lines(db, skip=skip, limit=limit)


@router.get(
    "/lines/{line_id}",
    response_model=schemas.LineOut,
)
def get_line(
    line_id: int,
    db: Session = Depends(get_db),
):
    line = crud.get_line(db, line_id)

    if line is None:
        raise HTTPException(
            status_code=404,
            detail="Line not found",
        )

    return line


@router.patch(
    "/lines/{line_id}",
    response_model=schemas.LineOut,
)
def update_line(
    line_id: int,
    data: schemas.LineUpdate,
    db: Session = Depends(get_db),
):
    line = crud.update_line(db, line_id, data)

    if line is None:
        raise HTTPException(
            status_code=404,
            detail="Line not found",
        )

    return line


@router.delete(
    "/lines/{line_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_line(
    line_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_line(db, line_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Line not found",
        )


# ==================== Conection ====================

@router.post(
    "/conections",
    response_model=schemas.ConectionOut,
    status_code=status.HTTP_201_CREATED,
)
def create_conection(
    data: schemas.ConectionCreate,
    db: Session = Depends(get_db),
):
    return crud.create_conection(db, data)


@router.get(
    "/conections",
    response_model=list[schemas.ConectionOut],
)
def list_conections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_conections(db, skip=skip, limit=limit)


@router.get(
    "/conections/{id_station}/{id_line}",
    response_model=schemas.ConectionOut,
)
def get_conection(
    id_station: int,
    id_line: int,
    db: Session = Depends(get_db),
):
    conection = crud.get_conection(db, id_station, id_line)

    if conection is None:
        raise HTTPException(
            status_code=404,
            detail="Conection not found",
        )

    return conection


@router.delete(
    "/conections/{id_station}/{id_line}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_conection(
    id_station: int,
    id_line: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_conection(db, id_station, id_line)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conection not found",
        )


# Registra todas as rotas do APIRouter no FastAPI.
app.include_router(router)
