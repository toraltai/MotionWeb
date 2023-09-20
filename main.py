from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config.settings import APPS_MODEL
from app.routers import api_router


app = FastAPI()


@app.on_event("startup")
async def start_serv():
    print("server on")

@app.on_event("shutdown")
async def stop_serv():
    print('server off')

@app.get("/")
async def hello():
    return {"Hello":"World"}


app.include_router(api_router, prefix='/api')


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={"models": APPS_MODEL},
    generate_schemas=True,
    add_exception_handlers=True,
)
