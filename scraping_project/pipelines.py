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
        
        exist_category = session.query(Category).filter_by(name=category.name).first()
        if exist_category is not None:  
            article.category = exist_category
        else:
            article.category = category

        if 'author_name' in item:
            for author_name in item['author_name']:
                author = Author(name=author_name)
                exist_author = session.query(Author).filter_by(name=author.name).first()
                if exist_author is not None: 
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
        if exist_article is not None:  
            raise DropItem('Duplicate item found: {}'.format(item['title']))
            session.close()
        else:
            return item
            session.close()