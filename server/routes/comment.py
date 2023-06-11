from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..routes import SessionLocal
from typing import List, Optional
from sqlalchemy import select
from datetime import datetime

from server.database.models.user import Comment, User

router = APIRouter()


class CommentSchema(BaseModel):
    content: str
    user_id : int
    blog_id: int

class CreateComment(CommentSchema):
    id: int

    class Config:
        orm_mode = True

class CommentResponse(BaseModel):
    id: int
    content: str
    date_added: Optional[datetime] = None
    name : str
    

@router.post('/post/{id}/comment', response_model= Optional[CreateComment])
def comment(comment : CommentSchema):
    session = SessionLocal()
    data = comment.dict()
    blog_comment = Comment(**comment.dict())
    session.add(blog_comment)
    session.commit()
    session.refresh(blog_comment)
    return blog_comment

@router.get("/post/{blog_id}/comment", response_model= List[CommentResponse])
def get_comments(blog_id : int):
    session = SessionLocal()
    query = select(Comment.id, Comment.content, Comment.date_added, User.name)\
    .join(User, Comment.user_id == User.id)\
    .filter(Comment.blog_id == blog_id)
    result = session.execute(query)
    comments = result.fetchall()
    
    comment_responses = []
    for comment in comments:
        comment_response = CommentResponse(
            id=comment.id,
            content=comment.content,
            date_added=comment.date_added,
            name=comment.name
        )
        comment_responses.append(comment_response)

    return comment_responses



