from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, UploadFile, File
from ..routes import SessionLocal
from server.database.models.user import Blog
from typing import List
import os
import uuid
from starlette.responses import JSONResponse
from fastapi.responses import FileResponse
from typing import Optional




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


@router.get('/blogs', response_model=List[BlogList])
def get_blogs():
    session = SessionLocal()
    blogs = session.query(Blog).all()
    return blogs

@router.get('/blogs/{blog_id}', response_model=BlogList)
def get_blog(blog_id: int):
    session = SessionLocal()
    blog = session.query(Blog).get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail='Blog not found')
    return blog

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
    base_url = "http://localhost:8000"  # Change this to your server's base URL
    file_url = f"{base_url}/images/{unique_filename}"

    print(file_url)

    # Return the file URL in the response
    return JSONResponse({"file_url": file_url})


@router.get("/images/{image_name}")
async def get_image(image_name: str):
    folder_path = "images"
    print(f"{folder_path}/{image_name}")
    return FileResponse(f"{folder_path}/{image_name}")