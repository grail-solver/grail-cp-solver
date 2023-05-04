import json
from fastapi import APIRouter, HTTPException, status
from app.solver.solver import solve
from app.models.problemSchema import DataIn

from app.xtractor.core import helper

router = APIRouter()


@router.post("/resolve", status_code=status.HTTP_200_OK)
async def get_solutions(entry:DataIn):
    response = get_problem_formulation(entry.problem)
    if(response['status'] == "success"):
        print(response)
        data = response['data']
        # try:
        solutions, variables, ct = solve(data['variables'], data['constraints'], [])
        if type(solutions) == str:
            return {"message" : "No solutions founded!"}
        elif type(solutions) == list:
            if len(solutions) == 0:
                return {"message" : "No solutions founded!"}
            else:
                model_data = {
                    'v': variables,
                    'ct': ct
                }
                return {'message' : "OK", 'solutions': solutions, 'model_data': model_data, 'opt':[]}
        # except Exception as e:
        #     print(f"An exception has occurred: {e}")
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The formulation of the problem does not follow the expected protocol!")
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=data['error'])

def get_problem_formulation(problem_description:str):
    try:
        problem_formulation = helper.grail_extractor(problem_description)
        return{
            "status":"success",
            "data":problem_formulation
        }
    except Exception as e:
        return{
            "status":"failed",
            "data":None,
            "error":e
        }



