from typing import List
from pydantic import BaseModel

from app.db.tables import VariableType, DomainType


class VariableIn(BaseModel):
    id: List[str]
    name: List[str]
    type: List[str]
    domain_type: List[str]
    domain_value: List[str]
    problem_id: int


class Variable(BaseModel):
    id: int
    name: List[str]
    type: List[str]
    domain_type: List[str]
    domain_value: List[str]
    problem_id: int
