from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from server import SessionLocal
from server.database.models.blog import Blog, BlogCategory, Tag
from server.database.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.responses import JSONResponse

router = APIRouter()

class BlogList(BaseModel):
    id: int
    title: str
    description: str
    content: str
    category_id: int
    date_added: datetime
    author_id: int



    class Config:
        orm_mode = True

@router.get('/matchingpost/{id}', response_model=List[BlogList])
def get_matching_blogs(id: int):
    session = SessionLocal()
    
    # Fetch the blog with the provided ID
    blog = session.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # Fetch up to 3 blogs with matching tags
    matching_blogs = session.query(Blog).join(Tag).filter(Tag.name.in_([tag.name for tag in blog.tags])).filter(Blog.id != id).all()

    # Create a list of BlogList instances from the matching blogs
    response = []
    for matching_blog in matching_blogs[0:3]:
        blog_data = BlogList(
            id=matching_blog.id,
            title=matching_blog.title,
            description=matching_blog.description,
            content=matching_blog.content,
            category_id=matching_blog.category_id,
            date_added=matching_blog.date_added,
            author_id=matching_blog.author_id
        )
        response.append(blog_data)

    return response