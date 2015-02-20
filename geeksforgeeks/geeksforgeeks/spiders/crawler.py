"""
We really didn't use much of Scrapy's capability. We are using it here to merely do the multi-page processing which can be done without it.

And we download a webpage twice. First by Scrapy then wget. Not ideal.
"""
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from geeksforgeeks.items import GeeksforgeeksItem
from subprocess import call
import os
import codecs

class GFGSpider(CrawlSpider):
    name = 'geeksforgeeks'
    allowed_domains = ['geeksforgeeks.org']
    rules = (Rule (LinkExtractor(restrict_xpaths=('//a[@class="nextpostslink"]',))
        , follow= True),
        Rule(LinkExtractor(restrict_xpaths=('//h2[@class="post-title"]/a',)), callback='parse_item'),
    )
    def __init__(self, category='tag', name='dynamic-programming', *args, **kwargs):
        super(GFGSpider, self).__init__(*args, **kwargs)
        self.dest = "../makethebook/" + name + "/"
        self.start_urls = ['http://www.geeksforgeeks.org/' + category + '/' + name]
        self.doc_name = name

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        #item = GeeksforgeeksItem()
        #item['url'] = response.url
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)
        with open(self.dest + 'metadata.xml', 'w') as metadata:
            metadata.write('<dc:title>'+" ".join(self.doc_name.title().split('-'))+'</dc:title>\n<dc:language>en-US</dc:language>\n<dc:date opf:event="publication">2015-2-19</dc:date>\n<dc:rights>Creative Commons Attribution-NonCommercial-NoDerivs 2.5 India (CC BY-NC-ND 2.5 IN)</dc:rights>')
        """
        call(['wget', '-O', self.dest + response.url.split('/')[-2] + ".html", response.url])
        """
        with codecs.open(self.dest + response.url.split('/')[-2] + ".html", 'w', 'utf-8') as file_handle:
            file_handle.write(response.body_as_unicode())
        #return item
