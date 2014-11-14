INTRO
=====

A **very** simple web search engine written in Python 2.

Originally created for my *Language Technology* course project, at the 
Computer Engineering and Informatics Department, University of Patras, around
2010.

***

USAGE
=====

There are three basic ways to use the software:

- with existing index file, jump to making queries
- create index file from set of downloaded webpages
- crawl first and then create index file

With existing index file, jump to making queries
------------------------------------------------

Prerequisites:

- an index file (default name `index.xml`)
- the url-map (default name `urls.pickle`)

Just run:

    python evaluate_index.py -i <index_file> -u <url_map_file>

Or, if you are using the default file names, just:

    python evaluate_index.py

Caution, this last command will actually start at the crawling step if it
can't find the index and url-map.

`evaluate_index.py` will load the index file and url-map in memory and give 
you a prompt to start issuing search queries.

Create index file from set of downloaded webpages
-------------------------------------------------

Prerequisites:

- a directory containing '.html' files (default `./html/` directory)

Just run:

    python preprocessor.py
    python indexer.py

The preprocessor will clean and tokenize every '.html' file in the given
directory (let's call it `<webpages_dir>`), and store the tokenized webpages 
inside a `./tokenized/` directory; page `<webpages_dir>/x.html` will be 
stored as `./tokenized/x.txt` after the tokenization.

Crawl first and then create index file
--------------------------------------

Prerequisites:

- nothing!

Just run:

    python crawler.py
    python preprocessor.py
    python indexer.py

The crawler will start crawling webpages, starting from a default set of five
*seed* webpages, and saving them inside a `./html/` directory. Each webpage
must pass a set of default requirements to be saved. Some of the default
requirements are:

- page must be cacheable, i.e. no `no-store` attribute in the `cache-control`
    header
- page length must be at least 40000 characters, including html tags
- must be a `text/html` page
- language must be English, i.e. `content-language` must be `en`

The crawler extracts links to visit next, from every page it crawles, but
there are some links it does not follow. Default link requirements are:

- only follow `http://` links, i.e. no `ftp://`, `mailto:` etc links
- only crawl `.com` and `.co.uk` urls (no `.gov` etc urls)
- block `twitter.com`, `facebook.com`, `wikipedia` and `imdb` urls
- only follow urls ending in `.html`, `.htm` or `/`

The crawler will by default crawl until it has exactly 1000 pages (or it runs
out of links).

I might allow the user to change the defaults via command line parameters and
configuration files, in the future, if I find the time. Don't count on it.

After the crawler finishes, the preprocessor and indexer will process all 
`.html` pages inside the `./html/` directory, as described earlier.

After the whole process ends, the user can start querying the index after
running the command:

    python evaluate_index.py

