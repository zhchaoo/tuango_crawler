from tuango_crawler import settings
from tuango_crawler.items import DinnerItem

from scrapy import Spider, Request

class DinnerSpider(Spider):
    name = "dinner"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dianping.com/search/category/4/10",
    ]

    def __init__(self, source=None, database_dir="../repo/databases/", *args, **kwargs):
        super(DinnerSpider, self).__init__(*args, **kwargs)
        #self.allowed_domains = settings.ALLOWED_DOMAINS[source]
        #self.start_urls = settings.START_URLS[source]
        settings.MARKET_NAME = source
        settings.DATABASE_DIR = database_dir

    def parse(self, response):
        for href in response.css("section[id^='cat-list-section'] div.cat-item a::attr('href')"):
            url = response.urljoin(href.extract())
            yield Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = DinnerItem()
            item['name'] = sel.xpath('a/text()').extract()
            item['location'] = sel.xpath('a/@href').extract()
            item['price'] = sel.xpath('text()').extract()
            yield item


    def parse_articles_follow_next_page(self, response):
        for article in response.xpath("//article"):
            item = DinnerItem()
            yield item

        next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield Request(url, self.parse_articles_follow_next_page)
