from fastapi import FastAPI

from app.controllers import ctrl_auth, ctrl_task
from app.database import Base, engine
from app.models import task, token, user


def on_startup():
    Base.metadata.create_all(bind=engine)


app = FastAPI(title="SecureTask API", on_startup=[on_startup])
app.include_router(ctrl_auth.router)
app.include_router(ctrl_task.router_task)


@app.get("/")
async def root():
    return {"message": "Hello World"}
