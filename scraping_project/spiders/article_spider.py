import json
import scrapy


class ArticleSpider(scrapy.Spider):
    name = 'article'
    start_page = 'https://hbr.org{}'
    api = 'https://hbr.org/service/components/list/the-latest/{}/8?format=json&id=page.list.coronavirus.insight-center'
    start_urls = [api.format(0)]
    download_delay = 1.5 
    
    def parse(self, response):
        self.logger.info('start scraping articles')
        data = json.loads(response.text)
        for article in data.get('entry', []):
            yield {
                'author': article.get('author', {}),
                'title': article.get('title'),
                'category': article.get('category', {}).get('term'),
                'published': article.get('published'),
            }
            
            self.logger.info('get article url')
            article_url = article['link']['href']
            yield scrapy.Request(url=self.start_page.format(article_url), callback=self.parse_author)
            
        if data['page']['hasNext']:
            next_page = data['page']['number'] + 1
            yield scrapy.Request(url=self.api.format(next_page), callback=self.parse)
            
    def parse_author(self, response):
        yield {
            'author_name': response.css('.font-tighten-most::text').getall(),
            'author_bio': response.css('p.mbn.description-text.space-for-headshot::text').getall(),
        }