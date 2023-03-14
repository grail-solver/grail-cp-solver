from pydantic import BaseModel


class StatIn(BaseModel):
    mark: float
    comment: str
    problem_id: int


class Stat(BaseModel):
    id: int
    mark: float
    comment: str
    problem_id: int
