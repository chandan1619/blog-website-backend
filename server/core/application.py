from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes import blog, comment, user,search,similarpost

origins = [
    "http://localhost:3000",  # Add the origin URL of your frontend application
    "https://web-dzlx.onrender.com"
]


def create_app():
    app = FastAPI()
    app.include_router(user.router)
    app.include_router(blog.router)
    app.include_router(comment.router)
    app.include_router(search.router)
    app.include_router(similarpost.router)
    app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


    return app
    







