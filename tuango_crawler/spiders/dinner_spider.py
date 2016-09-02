from tuango_crawler import settings
from tuango_crawler.items import DinnerItem

from scrapy import Spider, Request


class DinnerSpider(Spider):
    name = "dinner"
    start_urls = [
        "http://www.dianping.com/search/category/4/10",
    ]

    def __init__(self, database_dir="./data", *args, **kwargs):
        super(DinnerSpider, self).__init__(*args, **kwargs)
        self.database_dir = database_dir

    def parse(self, response):
        next_ref_url = response.xpath("//div[@class='page']/a[@class='next']/@href").extract_first()
        if next_ref_url:
            yield Request(response.urljoin(next_ref_url), callback=self.parse)

        for item_data in response.css('.shop-wrap .shop-list>ul>li'):
            item = DinnerItem()
            item['name'] = item_data.xpath(".//div[@class='tit']/a[@data-hippo-type='shop']/@title").extract_first()
            item['url'] = response.urljoin(item_data.xpath("div[@class='pic']/a/@href").extract_first())
            item['pic_url'] = item_data.xpath("div[@class='pic']/a/img/@data-src").extract_first()
            item['rank'] = int(item_data.xpath(".//div[@class='comment']/span/@class").re('\d+')[0])
            item['popular'] = int(item_data.xpath(".//a[@class='review-num']/b/text()").re('\d+')[0])
            item['price'] = int(item_data.xpath(".//a[@class='mean-price']/b/text()").re('\d+')[0])
            item['tag'] = item_data.xpath(".//div[@class='tag-addr']//span[@class='tag']/text()").extract()[0]
            item['zone'] = item_data.xpath(".//div[@class='tag-addr']//span[@class='tag']/text()").extract()[1]
            item['address'] = item_data.xpath(".//div[@class='tag-addr']//span[@class='addr']/text()").extract_first()
            yield item
