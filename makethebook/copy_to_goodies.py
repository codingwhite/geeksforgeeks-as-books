import glob
from subprocess import call
for book_format in ['mobi', 'epub']:
    for book in glob.glob("./*/*1.2."+book_format):
        print "coping " + book + " to ../goodies/geeksforgeeks/"
        call("cp " + book + " ../goodies/geeksforgeeks/", shell=True)
