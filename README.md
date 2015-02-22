# Geeksforgeeks As Books

![Read books](http://rlv.zcache.com/funny_i_need_more_books_gift_postcards-r02cd503cbd784d0e934c3af02da0fea3_vgbaq_8byvr_512.jpg)

Have you ever wished you could read the awesome stuff on [geeksforgeeks.org][1] on your
iPad? Or on your Kindle/Kindle App? Well, now you have it. Look under the directory `goodies` and do the world some good with your algorithmic prowess ;)

Here's how the books look like in the iBooks App and Kindle App on my iPad. Kindle hasn't been tested.

![On Ipad](https://s-media-cache-ak0.pinimg.com/originals/1d/28/d3/1d28d3e3148d2c91d22e837ace64c0ce.jpg)

![On Kindle App](https://s-media-cache-ak0.pinimg.com/originals/2b/86/53/2b8653eff7aaa191a80263de32c29651.jpg)

## Books

Right now we have those books under `goodies`

- **Tree** Source: [here](http://www.geeksforgeeks.org/category/tree/)
- **Graph** Source: [here](http://www.geeksforgeeks.org/category/graph/)
- **Array** Source: [here](http://www.geeksforgeeks.org/category/c-arrays/)
- **Recursion** Source: [here](http://www.geeksforgeeks.org/tag/recursion/)
- **Backtracking** Source: [here](http://www.geeksforgeeks.org/tag/backtracking/)
- **Linked List** Source: [here](http://www.geeksforgeeks.org/category/linked-list/)
- **Math Problems** Source: [here](http://www.geeksforgeeks.org/tag/MathematicalAlgo/)
- **Greedy Algorithm** Source: [here](http://www.geeksforgeeks.org/tag/Greedy-Algorithm/)
- **Pattern Matching** Source: [here](http://www.geeksforgeeks.org/tag/pattern-searching/)
- **Divide and Conquer** Source: [here](http://www.geeksforgeeks.org/tag/divide-and-conquer/)
- **Dynamic Programming** Source: [here](http://www.geeksforgeeks.org/tag/dynamic-programming/)
- **Advanced Data Structure** Source: [here](http://www.geeksforgeeks.org/tag/advance-data-structures/)



## Tools

Want to create a book from the `geeksforgeeks` site yourself? No problem. But you'll need some tools to get started. Apart from `Python 2` you also need those.


### 1. Scrapy

[Scrapy][2] is used to download webpages from `geeksforgeeks`. It makes it super easy to do so with its rules.

Install it with `pip install scrapy`

### 2. Boilerpipy

So you have the html files locally. But those html files have many other stuff you don't want. You only want... goodies.
No problem. Check out [boilerpipy][6], it can remove all the unnecessary stuff like header and comments, leaving you with only the article itself. It has the functionality of Pocket or Readability you might be familiar with.


### 3. Pandoc

[Pandoc][3] is just super. It's used here to convert html files or markdown files to epub files. But it can do so **much** more. It's also super easy to generate `pdf` versions of the books if you want. You should definitely check it out.

### 4. Kindlegen

You'll need [kindlegen][4] to generate `mobi` files so you can read on your beloved Kindle or Kindle App. Download it from Amazon site and install.

You just need to use `kindlegen awesome.epub` and it'll give you a file called `awesome.mobi`. Awesome, right?

## How To

### 1. Crawling with Scrpay
Go to the `geeksforgeeks` subdirectory and run commands *like* `scrapy crawl geeksforgeeks -a category=category -a name=name`.

For example, running `scrapy crawl geeksforgeeks -a category=tag -a name=pattern-searching` will crawl from the page `http://www.geeksforgeeks.org/tag/pattern-searching/`. category and name are two arguments our spider takes. On geeksforgeeks, things can be organized by `tag` or `category`. Specify the category/tag and the name, Scrapy will do the rest for you.


### 2. Generate a book  

Following the example in 1, now go into the `makethebook` subdirectory and you should be able to find a directory called `pattern-searching`. Now run `python generate_book.py pattern-searching`. It will first clean the html files, concatenate the cleaned files into one, then use `pandoc` to create an epub file from the markdown file. In the end a mobi file is created using `kindlegen`.

Yay! Done!

## To Do

### Fix the encoding

The encoding isn't well handled yet. You'll spot some gibberish(mostly caused by ‘ and ’) once in a while. While it won't affect your understanding much, it's quite annoying.

## Contribute

I've only worked on this project for a few days since I had the idea. It has huge room to improve. It's the first time I used `Scrapy` and `pandoc`.  

You can contribute in many ways. Besides contributing code to this project. You are more than welcome to contribute in the following ways.

### Book

Every tag or category on `geeksforgeeks` can be turned into a book. So you are welcome to add more books.

### Styles and Cover Images

The style for generating `epub` books is under `styles` subdirectory. Welcome to submit your style sheets.

You can also make/submit cover images for the books so `pandoc` can use them when generating `epub` files. Right now they don't have any.

## License

The content on Geeksforgeeks is licensed under Creative Commons
Attribution-NonCommercial-NoDerivs 2.5 India. See the license [here][7]

The code in this project is licensed under Apache License, Version 2.0. See the
license [here][8]

## Authors

Jing Zhou, gnijuohz at gmail.com


[1]:http://www.geeksforgeeks.org/
[2]:http://scrapy.org/
[3]:http://johnmacfarlane.net/pandoc/
[4]:http://www.amazon.com/gp/feature.html?docId=1000765211
[5]:https://github.com/gnijuohz/boilerpipy
[6]:https://github.com/harshavardhana/boilerpipy
[7]:http://creativecommons.org/licenses/by-nc-nd/2.5/in/deed.en_US
[8]:http://www.apache.org/licenses/LICENSE-2.0
