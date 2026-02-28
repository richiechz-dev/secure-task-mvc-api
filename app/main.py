from fastapi import FastAPI

from app.controllers import ctrl_auth
from app.database import Base, engine
from app.models import task, token, user


def on_startup():
    Base.metadata.create_all(bind=engine)


app = FastAPI(on_startup=[on_startup])
app.include_router(ctrl_auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
