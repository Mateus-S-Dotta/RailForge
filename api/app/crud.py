from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


# ================= Station =================

def create_station(db: Session, data: schemas.StationCreate) -> models.Station:
    obj = models.Station(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_station(db: Session, station_id: int) -> models.Station | None:
    result = db.execute(
        select(models.Station).where(models.Station.id == station_id)
    )
    return result.scalar_one_or_none()


def get_stations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Station]:
    result = db.execute(
        select(models.Station)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


def get_stations_in_range(
    db: Session,
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
) -> list[models.Station]:
    result = db.execute(
        select(models.Station).where(
            models.Station.position_x.between(x_min, x_max),
            models.Station.position_y.between(y_min, y_max),
        )
    )
    return result.scalars().all()


def update_station(
    db: Session,
    station_id: int,
    data: schemas.StationUpdate,
) -> models.Station | None:
    obj = get_station(db, station_id)

    if obj is None:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_station(db: Session, station_id: int) -> bool:
    obj = get_station(db, station_id)

    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True


# ================= Line =================

def create_line(db: Session, data: schemas.LineCreate) -> models.Line:
    obj = models.Line(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_line(db: Session, line_id: int) -> models.Line | None:
    result = db.execute(
        select(models.Line).where(models.Line.id == line_id)
    )
    return result.scalar_one_or_none()


def get_lines(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Line]:
    result = db.execute(
        select(models.Line)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


def update_line(
    db: Session,
    line_id: int,
    data: schemas.LineUpdate,
) -> models.Line | None:
    obj = get_line(db, line_id)

    if obj is None:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_line(db: Session, line_id: int) -> bool:
    obj = get_line(db, line_id)

    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True


# ================= Conection =================

def create_conection(
    db: Session,
    data: schemas.ConectionCreate,
) -> models.Conection:
    obj = models.Conection(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_conection(
    db: Session,
    id_station: int,
    id_line: int,
) -> models.Conection | None:
    result = db.execute(
        select(models.Conection).where(
            models.Conection.id_station == id_station,
            models.Conection.id_line == id_line,
        )
    )
    return result.scalar_one_or_none()


def get_conections(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Conection]:
    result = db.execute(
        select(models.Conection)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


def delete_conection(
    db: Session,
    id_station: int,
    id_line: int,
) -> bool:
    obj = get_conection(db, id_station, id_line)

    if obj is None:
        return False

    db.delete(obj)
    db.commit()
    return True
