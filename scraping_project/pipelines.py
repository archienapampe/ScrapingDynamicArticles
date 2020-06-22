# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem

from scraping_project.models import (
    Article, Author, Category, db_connect, create_table)


class SaveArticlePipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        article = Article()
        author = Author()
        category = Category()
        
        article.title = item['title']
        article.published = item['published']
        category.name = item['category']
        
        # check whether the category exists
        exist_category = session.query(Category).filter_by(name=category.name).first()
        if exist_category is not None:  # the current category exists
            article.category = exist_category
        else:
            article.category = category

        # check whether the current article has authors or not
        if 'author_name' in item:
            for author_name in item['author_name']:
                author = Author(name=author_name)
                # check whether the current author already exists in the database
                exist_author = session.query(Author).filter_by(name=author.name).first()
                if exist_author is not None:  # the current author exists
                    author = exist_author
                article.author.append(author)
                
        try:
            session.add(article)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item
    
    
class DuplicatesPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        exist_article = session.query(Article).filter_by(title=item['title']).first()
        if exist_article is not None:  # the current quote exists
            raise DropItem('Duplicate item found: {}'.format(item['title']))
            session.close()
        else:
            return item
            session.close()