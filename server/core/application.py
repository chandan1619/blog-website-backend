from fastapi import FastAPI
from server.routes.user import router


def create_app():
    app = FastAPI()
    app.include_router(router)


    return app
    







