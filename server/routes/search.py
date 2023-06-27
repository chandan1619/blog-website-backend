from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from server import SessionLocal
from server.database.models.blog import Blog, BlogCategory, Tag
from sqlalchemy import select
from starlette.responses import JSONResponse
from sqlalchemy.orm import joinedload

router = APIRouter()

class BlogSchema(BaseModel):
    id:int
    title:str
    description:str
    content:str
    date_added: Optional[datetime] = None

@router.get("/blogs/all/search", response_model = List[BlogSchema])
def search_posts(query: str):
    db = SessionLocal()
    matching_posts = db.query(Blog.id, Blog.title, Blog.description, Blog.content, Blog.date_added).filter(
        (Blog.title.ilike(f"%{query}%")) | (Blog.description.ilike(f"%{query}%")) | (Blog.content.ilike(f"%{query}%"))
    ).all()
    db.close()

    if not matching_posts:
        return []

    blog_list = []

    for blog in matching_posts:
        blog_response = BlogSchema(
            id= blog.id,
            content= blog.content,
            description = blog.description,
            title = blog.title,
            date_added= blog.date_added
        )
        blog_list.append(blog_response)
    return blog_list