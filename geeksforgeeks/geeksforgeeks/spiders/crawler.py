import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from geeksforgeeks.items import GeeksforgeeksItem
from subprocess import call

class GFGSpider(CrawlSpider):
    name = 'geeksforgeeks'
    dest = "../../../advance-data-structures"
    allowed_domains = ['geeksforgeeks.org']
    start_urls = ['http://www.geeksforgeeks.org/tag/advance-data-structures/']

    rules = (Rule (LinkExtractor(restrict_xpaths=('//a[@class="nextpostslink"]',))
        , follow= True),
        Rule(LinkExtractor(restrict_xpaths=('//h2[@class="post-title"]/a',)), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        #item = GeeksforgeeksItem()
        #item['url'] = response.url
        call(['wget', '-N', '-O', self.dest + response.url.split('/')[-2] + ".html", response.url])
        #return item
