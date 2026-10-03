from datetime import datetime
from typing import Optional, List
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
    color: Optional[str] = None  # corrigido: color é nullable no model


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
    sequence: int


class ConectionCreate(ConectionBase):
    pass


class ConectionOut(ConectionBase):
    model_config = ConfigDict(from_attributes=True)


# ---------- Map (compostos, só leitura) ----------
class LineStationOut(BaseModel):
    """Estação dentro do contexto de uma linha, já na ordem certa (sequence)."""
    station_id: int
    name: str
    position_x: int
    position_y: int
    sequence: int

    model_config = ConfigDict(from_attributes=True)


class LineMapOut(LineBase):
    """Linha com suas estações ordenadas, usada só no /map."""
    id: int
    stations: List[LineStationOut]

    model_config = ConfigDict(from_attributes=True)


class MapResponse(BaseModel):
    stations: List[StationOut]
    lines: List[LineMapOut]