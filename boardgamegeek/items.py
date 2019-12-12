# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoardgamegeekItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bg_id = scrapy.Field()
    rank = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()
    weight = scrapy.Field()
    minplayers = scrapy.Field()
    maxplayers = scrapy.Field()
    minplaytime = scrapy.Field()
    maxplaytime = scrapy.Field()
