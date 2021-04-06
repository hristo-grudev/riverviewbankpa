import scrapy

from scrapy.loader import ItemLoader

from ..items import RiverviewbankpaItem
from itemloaders.processors import TakeFirst


class RiverviewbankpaSpider(scrapy.Spider):
	name = 'riverviewbankpa'
	start_urls = ['https://riverviewfinancial.q4ir.com/news-market-information/press-releases/default.aspx']

	def parse(self, response):
		post_links = response.xpath('//h4/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2/span/text()').get()
		description = response.xpath('//div[@class="xn-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="module_date-text"]/text()').get()

		item = ItemLoader(item=RiverviewbankpaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
