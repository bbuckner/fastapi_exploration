from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from . import models
# from .database import engine
from .routers import posts, users, auth, vote

# command to start app on uvicorn server:
# uvicorn <path to file with app instance from current working directory>:<name of variable fastapi instance is stored in> --reload
# example if fastapi_exploration is your current working directory:
# uvicorn app.main:app --reload
# The reload flag reloads on save.

# For production:
# uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}

# This is what creates tables if they dont already exist.
# Dont need this with alembic as it would make the
# database out of sync with the current revision:

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API!!!!"}
