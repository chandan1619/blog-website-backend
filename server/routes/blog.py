import os
import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from server import SessionLocal
from server.database.models.user import Blog, User
from sqlalchemy import select
from starlette.responses import JSONResponse

router = APIRouter()

class BlogBase(BaseModel):
    image: str
    title: str
    description: str
    content: str

class BlogCreate(BaseModel):
    image: str
    title: str
    description: str
    content: str
    author_id: int

class BlogUpdate(BaseModel):
    image: Optional[str]
    title: str
    description: str
    content: str

class BlogList(BlogBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

class BlogListResponse(BlogBase):
    id:int
    name:str
    author_id:int
    date_added: Optional[datetime] = None

    class Config:
        orm_mode = True

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
    


@router.get('/blogs', response_model=List[BlogListResponse])
def get_blogs():
    session = SessionLocal()
    query = select(Blog.id, Blog.content, Blog.title, Blog.description, Blog.image,User.name, Blog.author_id, Blog.date_added)\
    .join(User, Blog.author_id == User.id)
    result = session.execute(query)
    blogs = result.all()

    blog_list = []

    for blog in blogs:
        blog_response = BlogListResponse(
            id= blog.id,
            content= blog.content,
            description = blog.description,
            title = blog.title,
            name = blog.name,
            image = blog.image,
            author_id = blog.author_id,
            date_added = blog.date_added
        )
        blog_list.append(blog_response)
    return blog_list

@router.get('/blogs/{blog_id}', response_model=BlogListResponse)
def get_blog(blog_id: int):
    session = SessionLocal()
    query = select(Blog.id, Blog.content, Blog.title, Blog.description, Blog.image,User.name, Blog.author_id, Blog.date_added)\
    .join(User, Blog.author_id == User.id)\
    .filter(Blog.id == blog_id)
    result = session.execute(query)
    blogs = result.first()
    if not blogs:
        raise HTTPException(status_code=404, detail='Blog not found')
    
    
    blog_response = BlogListResponse(
            id= blogs.id,
            content= blogs.content,
            description = blogs.description,
            title = blogs.title,
            name = blogs.name,
            image = blogs.image,
            author_id = blogs.author_id,
            date_added = blogs.date_added
    )
    return blog_response
    

@router.post('/blogs', response_model=BlogList)
def create_blog(blog: BlogCreate):
    session = SessionLocal()
    print(blog)
    data = blog.dict()
    print(data)
    db_blog = Blog(**blog.dict())
    print(db_blog)
    session.add(db_blog)
    session.commit()
    session.refresh(db_blog)
    return db_blog

@router.put('/blogs/{blog_id}', response_model=BlogList)
def update_blog(blog_id: int, blog: BlogUpdate):
    session = SessionLocal()
    db_blog = session.query(Blog).get(blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail='Blog not found')
    
    if blog.image is None:
        # Preserve the old value of the image field
        blog.image = db_blog.image
    for field, value in blog:
        setattr(db_blog, field, value)
    session.commit()
    session.refresh(db_blog)
    return db_blog

@router.delete('/blogs/{blog_id}')
def delete_blog(blog_id: int):
    session = SessionLocal()
    db_blog = session.query(Blog).get(blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail='Blog not found')
    session.delete(db_blog)
    session.commit()
    return {'message': 'Blog deleted successfully'}


@router.post('/blog/upload')
async def upload_file(file: UploadFile = File(...)):
    # Create the "images" folder if it doesn't exist
    folder_path = "images"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Generate a unique filename for the uploaded file
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"image_{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(folder_path, unique_filename)

    # Save the file to the desired location
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    # Create the URL for the uploaded file
    base_url = "https://with-docker-api.onrender.com"  # Change this to your server's base URL
    file_url = f"{base_url}/images/{unique_filename}"

    print(file_url)

    # Return the file URL in the response
    return JSONResponse({"file_url": file_url})


@router.get("/images/{image_name}")
async def get_image(image_name: str):
    folder_path = "images"
    print(f"{folder_path}/{image_name}")
    return FileResponse(f"{folder_path}/{image_name}")