import scrapy
from scrapy.loader import ItemLoader

from scraping_project.items import ArticleItem


class ArticleSpider(scrapy.Spider):
    # parsing site page - https://hbr.org/insight-center/coronavirus
    name = 'article'
    api = 'https://hbr.org/service/components/list/the-latest/{}/8?format=json&id=page.list.coronavirus.insight-center'
    start_page = 'https://hbr.org{}'
    start_urls = [api.format(0)]
    download_delay = 1.5 
    
    def parse(self, response):
        self.logger.info('start scraping articles')
        data = response.json()
        for article in data.get('entry', []):
            loader = ItemLoader(item=ArticleItem(), selector=article)
            loader.add_value(field_name='title', value=article.get('title'))
            loader.add_value(field_name='category', value=article.get('category', {}).get('term'))
            loader.add_value(field_name='published', value=article.get('published'))
            article_item = loader.load_item()
            
            article_url = article['link']['href']
            yield scrapy.Request(url=self.start_page.format(article_url),
                                  callback=self.parse_author, meta={'article_item': article_item})
            
        if data['page']['hasNext']:
            next_page = data['page']['number'] + 1
            yield scrapy.Request(url=self.api.format(next_page), callback=self.parse)
            
    def parse_author(self, response):
        article_item = response.meta['article_item']
        loader = ItemLoader(item=article_item, response=response)
        loader.add_css(field_name='author_name', css='.font-tighten-most::text')
        yield loader.load_item()