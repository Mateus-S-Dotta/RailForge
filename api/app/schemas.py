from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# ---------- Station ----------
class StationBase(BaseModel):
    name: str
    position_y: int
    position_x: int
    description: Optional[str] = None


class StationCreate(StationBase):
    pass


class StationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    position_y: Optional[int] = None
    position_x: Optional[int] = None


class StationOut(StationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Line ----------
class LineBase(BaseModel):
    name: str
    color: str


class LineCreate(LineBase):
    pass


class LineUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


class LineOut(LineBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Conection ----------
class ConectionBase(BaseModel):
    id_station: int
    id_line: int


class ConectionCreate(ConectionBase):
    pass


class ConectionOut(ConectionBase):
    model_config = ConfigDict(from_attributes=True)
