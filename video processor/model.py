from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Car(BaseModel):
    id: int
    speed: int
    lane: int


class Way1(BaseModel):
    cars: List[Car]


class Model(BaseModel):
    way_1: Way1 = Field(..., alias='way 1')
    timestamp: str
    camera_id: int

    def __init__(__pydantic_self__, **data) -> None:
        super().__init__(**data)