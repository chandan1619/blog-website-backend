from fastapi import FastAPI
from server.routes import user,blog
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",  # Add the origin URL of your frontend application
]


def create_app():
    app = FastAPI()
    app.include_router(user.router)
    app.include_router(blog.router)
    app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


    return app
    







