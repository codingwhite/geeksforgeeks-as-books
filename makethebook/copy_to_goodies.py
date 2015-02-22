import glob
from subprocess import call
for book_format in ['mobi', 'epub']:
    for book in glob.glob("./*/*."+book_format):
        print "coping " + book + " to ../goodies/"
        call("cp " + book + " ../goodies/", shell=True)
