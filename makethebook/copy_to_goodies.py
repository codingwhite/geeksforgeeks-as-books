import glob
from subprocess import call
for book_format in ['mobi', 'epub']:
    for book in glob.glob("./*/*1.1."+book_format):
        print "coping " + book + " to ../goodies/"
        call("cp " + book + " ../goodies/", shell=True)
