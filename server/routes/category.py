from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from server import SessionLocal
from server.database.models.user import User
from server.database.models.blog import Blog, BlogCategory, Tag
from sqlalchemy import select
from starlette.responses import JSONResponse
from sqlalchemy.orm import joinedload

router = APIRouter()

class BlogCategoryRes(BaseModel):
    name : str

class BlogCategoryList(BlogCategoryRes):
    id : int


@router.post('/category', response_model= BlogCategoryList)
def create_Category(category: BlogCategoryRes):
    session = SessionLocal()
    cat = category.dict()
    cat_db = BlogCategory(**cat)
    session.add(cat_db)
    session.commit()
    session.refresh(cat_db)
    response = BlogCategoryList(id=cat_db.id, **cat)
    return response

@router.get('/categories', response_model= List[BlogCategoryList])
def get_categories():
    session = SessionLocal()
    categories = session.query(BlogCategory).all()

    # Create an instance of BlogCategoryList and set the categories as data
    response = []
    for category in categories:
        category_data = BlogCategoryList(id=category.id, name=category.name)
        response.append(category_data)

    return response