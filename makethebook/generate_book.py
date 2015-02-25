"""
generate a book
"""

import sys
from subprocess import call
import glob

from clean import clean_html_files


def generate(book, version):
    if book[-1] != "/":
        book = book + "/"
    version = "_" + version
    print "cleaning html files,", "this might take a while..."
    clean_html_files(book)
    cleaned_html = sorted(glob.glob(book + "*_cleaned.html"))
    md_file = book + book[:-1] + version + ".md"
    html_file = book + book[:-1] + version + ".html"
    epub_file = book + book[:-1] + version + ".epub"
    print "generating", html_file, "..."
    call("cat " + "../bookcopyright/copyright.html " + " ".join(cleaned_html) + " > " + html_file, shell=True)
    print "generating", epub_file, "this might take a while..."
    call(['pandoc', '-o', epub_file, html_file, '--epub-metadata='+book+'metadata.xml', "--toc", "--toc-depth=2", "--epub-stylesheet=../styles/buttondown.css", "-f", "html-native_divs"])
    print "generating", book + version + book[:-1] + ".mobi", "..."
    call(['kindlegen', epub_file])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "this program takes one argument"
        sys.exit()
    book = sys.argv[1]
    version = sys.argv[2]
    generate(book, version)
