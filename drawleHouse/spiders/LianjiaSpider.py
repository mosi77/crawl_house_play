from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from drawleHouse.items import DrawlehouseItem


class MininovaSpider(CrawlSpider):

    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://sh.lianjia.com/ershoufang/?utm_source=baidu&utm_medium=pinzhuan&utm_content=Title&utm_campaign=Main']
    rules = [Rule(LinkExtractor(allow=['http://sh.lianjia.com/ershoufang/sh\d+.html']), 'parse_torrent')]

    def parse_torrent(self, response):
        torrent = DrawlehouseItem()
        torrent['url'] = response.url
        torrent['name'] = response.xpath("//span[@class='item-cell maininfo-estate-address']/text()").extract()
        # torrent['description'] = response.xpath("//div[@id='description']").extract()
        # torrent['size'] = response.xpath("//div[@id='specifications']/p[2]/text()[2]").extract()
        return torrent
        # print(response)


