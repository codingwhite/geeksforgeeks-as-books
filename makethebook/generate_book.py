"""
generate a book
"""

import sys
from subprocess import call
import glob

from clean import clean_html_files


def generate(book):
    print "cleaning html files...might take a while.."
    #clean_html_files(book)
    cleaned_html = sorted(glob.glob(book + "*_cleaned.html"))
    md_file = book + book[:-1] + ".md"
    epub_file = book + book[:-1] + ".epub"

    print "generating a md file..."
    call(['pandoc', '-o', md_file, "-t", "markdown_strict"] + cleaned_html)
    print "generating an epub file...might take a while..."
    call(['pandoc', '-o', epub_file, md_file, '--epub-metadata='+book+'metadata.xml', "--toc", "--toc-depth=2", "--epub-stylesheet=../styles/buttondown.css", "-f", "html-native_divs"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "this program takes one argument"
        sys.exit()
    book = sys.argv[1]
    if book[-1] != "/":
        book = book + "/"
    generate(book)
