# -*- coding: utf-8 -*-
import scrapy

from boardgamegeek.items import BoardgamegeekItem

chunks = lambda l, n: [l[x: x+n] for x in xrange(0, len(l), n)]

class TwoPlayersSpider(scrapy.Spider):
    name = 'two_players'
    start_urls = [
    	'https://www.boardgamegeek.com/xmlapi/geeklist/48970', # Best With Two
    	'https://www.boardgamegeek.com/xmlapi/geeklist/48986' # Recommended for Two
    ]
    found_ids = set()

    def parse(self, response):
    	boardgames = response.xpath("//item/@objectid").extract()
    	page = 0
    	for chunk in chunks(boardgames,100):
    		page += 1
	    	bg_ids = ",".join(chunk)
	        yield scrapy.Request("https://www.boardgamegeek.com/xmlapi2/thing?id={}&stats=1".format(bg_ids), self.parse_bg, meta={'page':page})

    def parse_bg(self, response):
    	rank = (response.meta['page']-1)*100
    	for bg in response.xpath('//item[@type="boardgame"]'):
    		rank += 1
    		bg_id = bg.xpath("./@id").extract_first()
    		if bg_id not in self.found_ids:
	    		minplaytime = int(bg.xpath(".//minplaytime/@value").extract_first())
	    		maxplaytime = int(bg.xpath(".//maxplaytime/@value").extract_first())
	    		minplayers = int(bg.xpath(".//minplayers/@value").extract_first())
	    		maxplayers = int(bg.xpath(".//maxplayers/@value").extract_first())
	    		rating = float(bg.xpath(".//statistics/ratings/average/@value").extract_first())
	    		weight = float(bg.xpath(".//statistics/ratings/averageweight/@value").extract_first())

	    		if (minplaytime <= 40 or maxplaytime <= 60) and maxplayers >= 3 and rating >=6.5: 
	    			#not too long and flexible on players number, and good
	    			if weight <=2.5 or minplayers == 1:
	    				# light for the crowd or can be played solo
		    			if not bg.xpath('.//link[@type="boardgamemechanic"][@id="2023"]').extract_first(): 
			    			# not cooperative
			    			if (bg.xpath('.//rank[@type="family"][@name="strategygames"]').extract_first() or 
			    				bg.xpath('.//rank[@type="family"][@name="familygames"]').extract_first() or 
			    				bg.xpath('.//rank[@type="family"][@name="partygames"]').extract_first() or 
			    				bg.xpath('.//rank[@type="family"][@name="thematic"]').extract_first() or 
			    				bg.xpath('.//link[@type="boardgameimplementation"]').extract_first()): 
			    				# in strategy, family, party, or thematic category
			    				# Or it reimplements a game which means it's a good game

						    	i = BoardgamegeekItem()
						    	i["bg_id"] = bg_id
						    	i["rank"] = rank
						    	i["title"] = bg.xpath('.//name[@type="primary"]/@value').extract_first()
						    	i["link"] = "http://www.boardgamegeek.com/boardgame/{}".format(bg_id)
						    	i["rating"] = rating
						    	i["weight"] = weight
						    	i["minplayers"] = minplayers
						    	i["maxplayers"] = maxplayers
						    	i["minplaytime"] = minplaytime
						    	i["maxplaytime"] = maxplaytime

						    	yield i
