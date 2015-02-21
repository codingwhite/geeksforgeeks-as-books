# geeksforgeeks as books

![Read books](http://rlv.zcache.com/funny_i_need_more_books_gift_postcards-r02cd503cbd784d0e934c3af02da0fea3_vgbaq_8byvr_512.jpg)

Have you ever wished you can read the awesome stuff on [geeksforgeeks.org][1] on you
iPad in epub format? Or mobi format on your Kindle? Well, now you have it. Look under the directory `goodies` and enjoy reading!

![On Kindle App](https://s-media-cache-ak0.pinimg.com/originals/2b/86/53/2b8653eff7aaa191a80263de32c29651.jpg)

![On Ipad](https://s-media-cache-ak0.pinimg.com/originals/1d/28/d3/1d28d3e3148d2c91d22e837ace64c0ce.jpg)


## Tools

Want to create a book from the geeksforgeeks site yourself? No problem. But you'll need some tools to get started. Apart from `Python 2.7` you also need those.


### 2. Scrapy

[Scrapy][2] is used to download webpages from `geeksforgeeks`. It makes it super easy to do so with it's rules.

Install it with `pip install scrapy`

### 2. Boilerpipy

So you have the html files locally. But those html files have many other stuff you don't want. You only want... goodies.
No problem. Check out [boilerpipy][6], it removes all the unnecessary stuff. It has the functionality of Pocket or Readability you might be familiar with.


### 3. Pandoc

[Pandoc][3] is just super. It's used here to convert html files to markdown files. And from html files or markdown files to epub files.

### 4. Kindlegen

You'll need [kindlegen][4] to generate `mobi` so you can read on your beloved Kindle or Kindle App. Download it and install.

You just need to use `kindlegen awesome.epub` and it'll give you a file called `awesome.mobi`.

## How To

### 1. Crawling with Scrpay
Go to the `geeksforgeeks` subdirectory and run `scrapy crawl geeksforgeeks -a category=category -a name=name`

For example `scrapy crawl geeksforgeeks -a category=tag -a name=pattern-searching` will crawl from the page `http://www.geeksforgeeks.org/tag/pattern-searching/`. On geeksforgeeks, things can be organized by `tag` or `category`. Scrapy will do the rest for you.


### 2. Generate a book  

Now go into the `makethebook` subdirectory where you should be able to find a directory called `pattern-searching`. Now run `python generate_book.py pattern-searching`. It will first clean the html files, concatenate them into one, then use `pandoc` to create an epub file from the markdown file. In the end a mobi file is created using `kindlegen`.

Yay! Done!

## To Do

### Fix the encoding
The encoding isn't well handled yet. You'll spot some gibberish(mostly ‘ and ’) once in a while. While it won't affect your understanding much, it's quite annoying.

## Contribute

I've only worked on this project for a few days since I had the idea. It has huge room to improve. It's the first time I used `Scrapy` and `pandoc`.  

You can contribute in many ways. Besides contributing code to this project. You are more than welcome to contribute in the following ways.

### Book

Every tag or category on `geeksforgeeks` can be turned into a book. So you are welcome to add more books.

### Styles and Cover Images

The style for ipub file is under `styles` subdirectory. Welcome to submit your style sheets.

You can also make cover images for the books so `pandoc` can use when generating an epub file. Right now they don't have any.

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
