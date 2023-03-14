from fastapi import APIRouter, HTTPException, status
import httpx
from typing import List
from app.solver.solver import solve
from app.models.problemSchema import DataIn
router = APIRouter()


# For user sign up
@router.post("/solver/all", status_code=status.HTTP_200_OK)
async def register(data:DataIn):
    try:
        solutions = solve(data.variables, data.constraints, data.optimization)
        if type(solutions) == str:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="No solutions found")
        elif type(solutions) == list:
            if len(solutions) == 0:
                raise HTTPException(status_code=status.HTTP_200_OK, detail="No solutions found")
            else:
                return {"message" : "OK", 'solutions': solutions}
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_problem_formulation():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://your-node-api-url.com/api-endpoint")
        response.raise_for_status()
        return response.json()

