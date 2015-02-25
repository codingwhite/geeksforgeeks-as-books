import glob
from subprocess import call

#!/usr/bin/env python
import sys
import codecs
import os
import logging
import cgi

import HTMLParser
import lxml.html as html
import lxml.etree
from boilerpipy import (Extractor, isvalidhtml)


def insert_content(doc, html_doc, insert_string, insert_type):
    to_insert = html_doc.find('.//'+insert_type)
    doc.append(to_insert)
    return doc

def clean(file_name, directory="."):
    content = open(file_name, "r").read()
    article = Extractor(content, loglevel = logging.INFO).extracted()
    #article = cgi.escape(article).encode('ascii', 'xmlcharrefreplace')
    #return article
    if article is None:
        print "Error processing html file"
        sys.exit(1)
    html_parser = html.HTMLParser(encoding="utf-8")
    html_doc = html.fromstring(content, parser=html_parser)
    head_doc = html_doc.find('head')
    source_url = head_doc.cssselect('link[rel="canonical"]')[0].get('href')

    reconstructed_body = u"<html><body>" + article.replace("<h2", "<h1").replace("</h2>", "</h1>") + u"</body></html>"
    source_header_string = "<h3>Source</h3>"
    source_link = "<p><a href='" + source_url +"' rel='tag'>" + source_url + "</a></p>"
    # further remove useless stuff
    body_doc = html.fromstring(reconstructed_body).find('body')

    try:
        post_content_doc = body_doc.xpath("//div[@class='post-content']")[0]
        post_content_doc.append(lxml.etree.XML(source_header_string))
        post_content_doc.append(lxml.etree.XML(source_link))
    except:
        print file_name

    basename = os.path.basename(file_name)
    cleaned_file = os.path.splitext(basename)[0] + "_cleaned.html"
    #out = html.tostring(head_doc) + html.tostring(body_doc)
    result = html.tostring(body_doc)
    with codecs.open(directory + cleaned_file, 'w', 'utf-8') as cleaned_file_handle:
        cleaned_file_handle.write(result)

def clean_html_files(directory = ""):
    for html_file in glob.glob(directory + '*.html'):
        if 'clean' not in html_file:
            print html_file
            clean(html_file, directory)
            """
            except:
                print "WARNING: failed to clean", html_file
            try:
            """

if __name__ == "__main__":
    clean_html_files("")
