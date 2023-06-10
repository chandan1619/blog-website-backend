from sqlalchemy import Column, Integer, String , ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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
    author_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('blog_categories.id'))
    comments = relationship('Comment', backref='blog')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    blog_id = Column(Integer, ForeignKey('blogs.id'))

class BlogCategory(Base):
    __tablename__ = 'blog_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    blogs = relationship('Blog', backref='category')