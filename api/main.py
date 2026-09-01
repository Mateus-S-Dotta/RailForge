from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, status, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, Base, get_db
from app import crud, schemas



@asynccontextmanager
async def lifespan(app: FastAPI):
    # cria as tabelas que ainda não existem no banco
    Base.metadata.create_all(bind=engine)
    yield



router = APIRouter()
app = FastAPI(title="RailForge API", lifespan=lifespan)



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


# ==================== Station ====================
@router.post("/stations", response_model=schemas.StationOut, status_code=status.HTTP_201_CREATED)
async def create_station(data: schemas.StationCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_station(db, data)


@router.get("/stations", response_model=list[schemas.StationOut])
async def list_stations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_stations(db, skip=skip, limit=limit)


@router.get("/stations/by-position", response_model=list[schemas.StationOut])
async def stations_by_position(
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_stations_in_range(db, x_min, x_max, y_min, y_max)


@router.get("/stations/{station_id}", response_model=schemas.StationOut)
async def get_station(station_id: int, db: AsyncSession = Depends(get_db)):
    station = await crud.get_station(db, station_id)
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return station


@router.patch("/stations/{station_id}", response_model=schemas.StationOut)
async def update_station(
    station_id: int, data: schemas.StationUpdate, db: AsyncSession = Depends(get_db)
):
    station = await crud.update_station(db, station_id, data)
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return station


@router.delete("/stations/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_station(station_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_station(db, station_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Station not found")


# ==================== Line ====================
@router.post("/lines", response_model=schemas.LineOut, status_code=status.HTTP_201_CREATED)
async def create_line(data: schemas.LineCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_line(db, data)


@router.get("/lines", response_model=list[schemas.LineOut])
async def list_lines(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_lines(db, skip=skip, limit=limit)


@router.get("/lines/{line_id}", response_model=schemas.LineOut)
async def get_line(line_id: int, db: AsyncSession = Depends(get_db)):
    line = await crud.get_line(db, line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return line


@router.patch("/lines/{line_id}", response_model=schemas.LineOut)
async def update_line(line_id: int, data: schemas.LineUpdate, db: AsyncSession = Depends(get_db)):
    line = await crud.update_line(db, line_id, data)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return line


@router.delete("/lines/{line_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_line(line_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_line(db, line_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Line not found")


# ==================== Conection ====================
@router.post("/conections", response_model=schemas.ConectionOut, status_code=status.HTTP_201_CREATED)
async def create_conection(data: schemas.ConectionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_conection(db, data)


@router.get("/conections", response_model=list[schemas.ConectionOut])
async def list_conections(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_conections(db, skip=skip, limit=limit)


@router.get("/conections/{id_station}/{id_line}", response_model=schemas.ConectionOut)
async def get_conection(id_station: int, id_line: int, db: AsyncSession = Depends(get_db)):
    conection = await crud.get_conection(db, id_station, id_line)
    if conection is None:
        raise HTTPException(status_code=404, detail="Conection not found")
    return conection


@router.delete("/conections/{id_station}/{id_line}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conection(id_station: int, id_line: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_conection(db, id_station, id_line)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conection not found")