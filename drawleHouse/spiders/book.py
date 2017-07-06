from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from drawleHouse.items import BookItem


class BookSpider(CrawlSpider):

    name = 'book'
    allowed_domains = ['biqukan.com']
    start_urls = ['http://www.biqukan.com/1_1094/']
    rules = [Rule(LinkExtractor(allow=['/\d+_\d+/\d+.html']), 'parse_torrent')]

    def parse_torrent(self, response):
        torrent = BookItem()
        torrent['url'] = response.url
        torrent['title'] = response.xpath("//div[@class='content']/h1/text()").extract()[0]
        torrent['content'] = response.xpath("//div[@id='content']/text()").extract()[0]

        yield torrent


