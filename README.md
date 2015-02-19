# geeksforgeeks-in-books

Have you ever wished you can read awesome stuff on [geeksforgeeks.org][1] on you
iPad in epub format? Or mobi format on your Kindle? Well, now you have it. Look
under the goodies and enjoy reading!

Right now we have a book called `Advanced Data Structure` in both epub and mobi
format.


## Tools

Want to create a book from the geeksforgeeks site yourself? No problem. But
you'll need some tools to get started. Apart from `Python 2.7` you also need
those.

### 1. Wget

**Download webpages to local, with images.**  
I'm sure you have this awesome tool installed on your computer but it's really
more awesome than you think. In this project, `wget` has been used to download
images linked in webpages onto local storage and the links in html files will be
replaced accordingly.

### 2. Scrapy

**What to download?**  
[Scrapy][2] is a really good tool to find what you want on a webpage. You just
need to specify the patterns for the link you want and it takes care of
everything.  
Install it with `pip install scrapy`

### 3. Boilerpipy

**Clean 'em**  
So you have the html files locally. But those html files have many other stuff
you don't want. You only want... goodies.
No problem. Check out [boilerpipy][5], forked from [here][6]


### 3. Pandoc
**It's all about conversion.**  
[Pandoc][3] is just super. It can convert files between so many formats. SO
MANY. Sorry, I'm still in awe.

### 4. Kindlegen
**Get your Kindle ready**  
You'll need [kindlegen][4] to generate `mobi` so you can read on your beloved Kindle
or Kindle App. Download it from the link and install.

## Do It Yourself

### 1. Modify crawling rules

Find crawler.py under the subdirectory `geeksforgeeks` and modify the rules.
Specify the directory you want the html files to be downloaded into by modifying
dest in the class.

### 2. Start crawling

Run `scrapy crawl geeksforgeeks` to download html files from geeksforgeeks
server to local. the crawling script calls wget to do the actual downloading.

### 3. Clean html  

Now go into the directory where you have all the html files and run
`python ../scripts/clean.py`.

### 4. Convert html files to one markdown file

Through trials and errors I've found I can get the best resulting epub file by
doing this.

```
pandoc -o advanced-data-structures.md -t strict\_markdown \*\_clean.html
```

### 5. Convert markdown file to epub

```
pandoc -o advanced_data_structure.epub advanced_data_structure_geeksforgeeks.md
--epub-metadata=metadata.xml --toc --toc-depth=2
--epub-stylesheet=../styles/buttondown.css
```

### 6. Get the mobi book

To generate mobi file from epub just use `kindlegen advanced_data_structure.epub`
and a book with the same name in mobi will be generated.

Ummmm, a lot of steps right? Interested in bettering this process? fork this and
contribute!


## Contribute

I've only worked on this project one day since I had the idea. It has huge room to improve. You can contribute in many ways.

### Book

Spot something wrong with the books? Messed up content? Submit an issue and
we'll look into it

### Styles

The style for ipub file is under `styles` subdirectory. Welcome to submit your
style sheet.

### More books

Turn content under other tags into books as well.

### Code

Welcome to contribute code into this project.


## License

The content on Geeksforgeeks is licensed under Creative Commons 
Attribution-NonCommercial-NoDerivs 2.5 India. See the license [here][7]

The code in this project is licensed under Apache License, Version 2.0. See the
license [here][8]



[1]:http://www.geeksforgeeks.org/
[2]:http://scrapy.org/
[3]:http://johnmacfarlane.net/pandoc/
[4]:http://www.amazon.com/gp/feature.html?docId=1000765211
[5]:https://github.com/gnijuohz/boilerpipy
[6]:https://github.com/harshavardhana/boilerpipy
[7]:http://creativecommons.org/licenses/by-nc-nd/2.5/in/deed.en_US
[8]:http://www.apache.org/licenses/LICENSE-2.0
