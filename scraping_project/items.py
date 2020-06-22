# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from datetime import datetime

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def convert_date(text):
    return datetime.strptime(text, '%B %d, %Y')


class ArticleItem(Item):
    title = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    category = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    published = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    author_name = Field(input_processor=MapCompose(str.strip))