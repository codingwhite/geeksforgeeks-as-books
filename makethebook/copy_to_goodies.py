import sys
import glob
from subprocess import call

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "this program takes one argument"
        sys.exit()
    version = sys.argv[1]
    for book_format in ['mobi', 'epub']:
        for book in glob.glob("./*/*" + version + "." + book_format):
            print "coping " + book + " to ../goodies/geeksforgeeks/"
            call("cp " + book + " ../goodies/geeksforgeeks/", shell=True)
