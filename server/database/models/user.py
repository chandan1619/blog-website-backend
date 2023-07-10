from sqlalchemy import Column, Integer, String , ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship


from .base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship('Blog', backref='author')
    comments = relationship('Comment', backref='user')

