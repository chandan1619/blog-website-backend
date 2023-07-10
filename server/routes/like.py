
from server.database.models.blog import  Blog
from server import SessionLocal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LikeResponse(BaseModel):
    message : str
    likeCount : int

@router.post('/blogs/{blog_id}/like', response_model= LikeResponse)
def increment_like_count(blog_id: int, increment_by: int = 1):
    db = SessionLocal()
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='Blog not found')

    if blog.likes is None:
        blog.likes = increment_by
    else:
        blog.likes += increment_by
    db.commit()

    return {'message': 'Like count updated successfully', 'likeCount' : blog.likes}