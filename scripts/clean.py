import glob
from subprocess import call

for html_file in glob.glob('*.html'):
    if 'clean' not in html_file:
        call(['readability', '-f', html_file])
