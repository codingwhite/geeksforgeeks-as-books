"""
We really didn't use much of Scrapy's capability. We are using it here to merely do the multi-page processing which can be done without it.

"""
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from subprocess import call
import os
import codecs

class GFGSpider(CrawlSpider):
    name = 'leetcode'
    allowed_domains = ['leetcode.com']
    rules = (Rule (LinkExtractor(restrict_xpaths=('//div[@class="alignleft"]/a',))
        , follow= True),
        Rule(LinkExtractor(restrict_xpaths=('//h1[@class="posttitle"]/a',)), callback='parse_item'),
    )
    start_urls = ["http://leetcode.com/"]
    dest = "/Users/jing/Awesome/github/geeksforgeeks-books/leetcode-book/"

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        #item = GeeksforgeeksItem()
        #item['url'] = response.url
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)
        with open(self.dest + 'metadata.xml', 'w') as metadata:
            metadata.write('<dc:title>Leetcode Articles</dc:title>\n<dc:language>en-US</dc:language>\n<dc:date opf:event="publication">2015-2-19</dc:date>\n<dc:rights>All right belongs to leetcode.com</dc:rights>')
        """
        call(['wget', '-O', self.dest + response.url.split('/')[-2] + ".html", response.url])
        """
        with codecs.open(self.dest + response.url.split('/')[-1], 'w', 'utf-8') as file_handle:
            file_handle.write(response.body_as_unicode())
        #return item
