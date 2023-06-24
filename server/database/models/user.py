from sqlalchemy import Column, Integer, String , ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship('Blog', backref='author')
    comments = relationship('Comment', backref='user')

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    title = Column(String, index=True)
    description = Column(String)
    content = Column(Text)
    date_added = Column(DateTime, default=datetime.utcnow)  # Add the date_added column
    author_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('blog_categories.id'))
    comments = relationship('Comment', backref='blog', cascade="all, delete")
    tags = relationship('Tag', back_populates='blog', cascade="all, delete")


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    blog_id = Column(Integer, ForeignKey('blogs.id', ondelete="CASCADE"))

    blog = relationship('Blog', back_populates='tags')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    date_added = Column(DateTime, default=datetime.utcnow)  # Add the date_added column
    user_id = Column(Integer, ForeignKey('users.id'))
    blog_id = Column(Integer, ForeignKey('blogs.id'))

class BlogCategory(Base):
    __tablename__ = 'blog_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    blogs = relationship('Blog', backref='category')