from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class Station(Base):
    __tablename__ = "station"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    position_y = Column(Integer)
    position_x = Column(Integer)

    __table_args__ = (
        UniqueConstraint("position_x", "position_y", name="uq_station_position_x_y"),
    )

class Line(Base):
    __tablename__ = "line"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    color = Column(String(20), nullable=True)

class Conection(Base):
    __tablename__ = "conection"

    id_station = Column(Integer, ForeignKey("station.id"), primary_key=True)
    id_line = Column(Integer, ForeignKey("line.id"), primary_key=True)