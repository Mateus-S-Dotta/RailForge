from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models

async def get_stations_in_range(
    db: AsyncSession,
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
) -> list[models.Station]:
    result = await db.execute(
        select(models.Station).where(
            models.Station.position_x.between(x_min, x_max),
            models.Station.position_y.between(y_min, y_max),
        )
    )
    return result.scalars().all()