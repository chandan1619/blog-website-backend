from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from server import SessionLocal
from server.database.models.blog import Blog, BlogCategory, Tag
from server.database.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.responses import JSONResponse

router = APIRouter()

class BlogBase(BaseModel):
    title: str
    description: str
    content: str

class BlogCreate(BaseModel):
    title: str
    description: str
    content: str
    category: int
    tags: str
    author_id: int

class BlogUpdate(BaseModel):
    title: str
    description: str
    content: str
    category: int
    tags: str
   

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
       

class BlogListResponse(BaseModel):
    id: int
    title: str
    description: str
    content: str
    category_id: Optional[int] 
    tags: Optional[List[str]]
    name: str
    author_id: int
    date_added: Optional[datetime] = None

    class Config:
        orm_mode = True


@router.get('/blogs', response_model=List[BlogListResponse])
def get_blogs(page: int = Query(1, gt=0), page_size: int = Query(10, gt=0, le=100)):
    session = SessionLocal()
    query = select(Blog.id, Blog.content, Blog.title, Blog.description, User.name, Blog.author_id, Blog.date_added)\
        .join(User, Blog.author_id == User.id)

    # Calculate the offset based on the page number and page size
    offset = (page - 1) * page_size

    # Apply pagination to the query
    query = query.offset(offset).limit(page_size)

    result = session.execute(query)
    blogs = result.all()

    blog_list = []

    for blog in blogs:
        blog_response = BlogListResponse(
            id=blog.id,
            content=blog.content,
            description=blog.description,
            title=blog.title,
            name=blog.name,
            author_id=blog.author_id,
            date_added=blog.date_added,
            category_id=0,
            tags=[]
        )
        blog_list.append(blog_response)
    return blog_list

@router.get('/blogs/{blog_id}', response_model=BlogListResponse)
def get_blog(blog_id: int):
    session = SessionLocal()

    # Fetch the blog with its associated category and tags
    blog = session.query(Blog).options(joinedload(Blog.category), joinedload(Blog.tags)).get(blog_id)

    if not blog:
        raise HTTPException(status_code=404, detail='Blog not found')

    # Extract the category ID and tag names
    category_id = blog.category.id if blog.category else None
    tag_names = [tag.name for tag in blog.tags]

    # Create the response
    blog_response = BlogListResponse(
        id=blog.id,
        title=blog.title,
        description=blog.description,
        content=blog.content,
        category_id=category_id,
        tags=tag_names,
        name=blog.author.name,
        author_id=blog.author.id,
        date_added=blog.date_added
    )

    return blog_response
    
    

@router.post('/blogs', response_model=BlogList)
def create_blog(blog: BlogCreate):
    session = SessionLocal()

    tags = blog.tags.split(',') if blog.tags else []

    tag_instances = []
    for tag_name in tags:
        tag = Tag(name=tag_name)
        session.add(tag)
        session.commit()
        session.refresh(tag)
        tag_instances.append(tag)

    db_blog = Blog(
        title=blog.title,
        description=blog.description,
        content=blog.content,
        date_added=datetime.utcnow(),
        author_id=blog.author_id,
        category_id=blog.category,
        tags=tag_instances,  # Associate the tags with the blog
    )

    session.add(db_blog)
    session.commit()
    session.refresh(db_blog)


    blog_list = BlogList(
            id = db_blog.id,
            title = db_blog.title,
            description = db_blog.description,
            content = db_blog.content,
            category_id = db_blog.category_id,
            date_added = db_blog.date_added,
            author_id = db_blog.author_id
    )

    return blog_list
  




@router.put('/blogs/{blog_id}', response_model=BlogList)
def update_blog(blog_id: int, blog: BlogUpdate):
    session = SessionLocal()
    db_blog = session.query(Blog).get(blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail='Blog not found')
    
    # Update the blog attributes
    db_blog.title = blog.title
    db_blog.description = blog.description
    db_blog.content = blog.content
    db_blog.category_id = blog.category

    # Update tags if provided
    if blog.tags:
        # Split the tags string into a list
        tag_list = blog.tags.split(',')

        # Clear existing tags for the blog
        db_blog.tags.clear()

        # Add new tags
        for tag_name in tag_list:
            tag = Tag(name=tag_name.strip())
            db_blog.tags.append(tag)

    session.commit()
    session.refresh(db_blog)

    response = BlogList(
        id=db_blog.id,
        title=db_blog.title,
        description=db_blog.description,
        content=db_blog.content,
        category_id = db_blog.category_id,
        date_added= db_blog.date_added,
        author_id= db_blog.author_id
    )
    return response


@router.delete('/blogs/{blog_id}')
def delete_blog(blog_id: int):
    session = SessionLocal()
    db_blog = session.query(Blog).get(blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail='Blog not found')
    session.delete(db_blog)
    session.commit()
    return {'message': 'Blog deleted successfully'}


# @router.post('/blog/upload')
# async def upload_file(file: UploadFile = File(...)):
#     # Create the "images" folder if it doesn't exist
#     folder_path = "images"
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)

#     # Generate a unique filename for the uploaded file
#     file_extension = os.path.splitext(file.filename)[1]
#     unique_filename = f"image_{uuid.uuid4().hex}{file_extension}"
#     file_path = os.path.join(folder_path, unique_filename)

#     # Save the file to the desired location
#     with open(file_path, 'wb') as f:
#         f.write(await file.read())

#     # Create the URL for the uploaded file
#     base_url = "https://with-docker-api.onrender.com"  # Change this to your server's base URL
#     file_url = f"{base_url}/images/{unique_filename}"

#     print(file_url)

#     # Return the file URL in the response
#     return JSONResponse({"file_url": file_url})


# @router.get("/images/{image_name}")
# async def get_image(image_name: str):
#     folder_path = "images"
#     print(f"{folder_path}/{image_name}")
#     return FileResponse(f"{folder_path}/{image_name}")



