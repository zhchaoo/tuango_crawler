# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DinnerItem(Item):
    # define the fields for your item here like:
    name = Field()
    url = Field()
    pic_url = Field()
    price = Field()
    rank = Field()
    popular = Field()
    address = Field()
    zone = Field()
    tag = Field()
