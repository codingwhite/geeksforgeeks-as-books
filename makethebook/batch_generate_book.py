import os
import glob
import sys

from generate_book import generate

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "this program takes one argument"
        sys.exit()
    version = sys.argv[1]
    for dir_name in glob.glob('*'):
        if os.path.isdir(dir_name):
            generate(dir_name, version)
