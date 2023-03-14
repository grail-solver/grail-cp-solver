from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import database
from app.routers import user
from app.routers import solver

app = FastAPI(title="Grail Solver")

origins = [
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(user.router,prefix="/auth", tags=["Authentication"])
app.include_router(solver.router,prefix="/solve", tags=["Solver"])
