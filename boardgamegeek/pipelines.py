# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class BoardgamegeekPipeline(object):
    def process_item(self, item, spider):
		if item['bg_id'] not in spider.found_ids: 
			spider.found_ids.add(item['bg_id'])
			return item
		else:
		 	raise DropItem('Duplicate item %s' % item)
