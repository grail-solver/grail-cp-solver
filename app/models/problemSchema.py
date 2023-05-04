from pydantic import BaseModel
from typing import List
from app.models.variableSchema import VariableIn
from app.models.constraintSchema import ConstraintIn
from app.models.optimizationSchema import OptimizationIn

class ProblemIn(BaseModel):
    content: str
    user_id: int


class Problem(BaseModel):
    id: int
    content: float
    user_id: int

# class DataIn(BaseModel):
#     variables: List[VariableIn]
#     constraints: List[ConstraintIn]
#     # optimization: List[OptimizationIn]


class DataIn(BaseModel):
    problem: str