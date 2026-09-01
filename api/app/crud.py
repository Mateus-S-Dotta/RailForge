from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models, schemas

# ================= Station =================
async def create_station(db: AsyncSession, data: schemas.StationCreate) -> models.Station:
    obj = models.Station(**data.model_dump())
    # data.model_dump() = Cria um obj
    # ** desestrutura
    # Ou seja, ele faz models.Station(position_y=data.position_y, ...)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_station(db: AsyncSession, station_id: int) -> models.Station | None:
    result = await db.execute(select(models.Station).where(models.Station.id == station_id))
    return result.scalar_one_or_none()


async def get_stations(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Station]:
    result = await db.execute(select(models.Station).offset(skip).limit(limit))
    return result.scalars().all()


async def update_station(
    db: AsyncSession, station_id: int, data: schemas.StationUpdate
) -> models.Station | None:
    obj = await get_station(db, station_id)
    if obj is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_station(db: AsyncSession, station_id: int) -> bool:
    obj = await get_station(db, station_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.commit()
    return True


# ================= Line =================
async def create_line(db: AsyncSession, data: schemas.LineCreate) -> models.Line:
    obj = models.Line(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_line(db: AsyncSession, line_id: int) -> models.Line | None:
    result = await db.execute(select(models.Line).where(models.Line.id == line_id))
    return result.scalar_one_or_none()


async def get_lines(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Line]:
    result = await db.execute(select(models.Line).offset(skip).limit(limit))
    return result.scalars().all()


async def update_line(db: AsyncSession, line_id: int, data: schemas.LineUpdate) -> models.Line | None:
    obj = await get_line(db, line_id)
    if obj is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_line(db: AsyncSession, line_id: int) -> bool:
    obj = await get_line(db, line_id)
    if obj is None:
        return False
    await db.delete(obj)
    await db.commit()
    return True


# ================= Conection =================
async def create_conection(db: AsyncSession, data: schemas.ConectionCreate) -> models.Conection:
    obj = models.Conection(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_conection(
    db: AsyncSession, id_station: int, id_line: int
) -> models.Conection | None:
    result = await db.execute(
        select(models.Conection).where(
            models.Conection.id_station == id_station,
            models.Conection.id_line == id_line,
        )
    )
    return result.scalar_one_or_none()


async def get_conections(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Conection]:
    result = await db.execute(select(models.Conection).offset(skip).limit(limit))
    return result.scalars().all()


async def delete_conection(db: AsyncSession, id_station: int, id_line: int) -> bool:
    obj = await get_conection(db, id_station, id_line)
    if obj is None:
        return False
    await db.delete(obj)
    await db.commit()
    return True