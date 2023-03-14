from typing import List
from pydantic import BaseModel

from app.db.tables import OptType


class OptimizationIn(BaseModel):
    exp: List
    type: str


class Optimization(BaseModel):
    id: int
    exp: List
    type: str
