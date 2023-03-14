from typing import List
from pydantic import BaseModel

from app.db.tables import Metric


class ConstraintIn(BaseModel):
    left_part: List
    right_part: List
    metric: str


class Constraint(BaseModel):
    id: int
    left_part: List
    right_part: List
    metric: str
