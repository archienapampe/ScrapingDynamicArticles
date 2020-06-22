from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Text, Date)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)
    

author_article = Table('author_article', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('article_id', Integer, ForeignKey('article.id'))
)


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    title = Column('title', Text())
    published = Column('published', Date)
    category_id = Column(Integer, ForeignKey('category.id'))
    authors = relationship('Author', secondary='author_article', lazy='dynamic', backref="article") 
          

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    articles = relationship('Article', secondary='author_article', lazy='dynamic', backref="author") 
          
   
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True)
    articles = relationship('Article', backref='category')  