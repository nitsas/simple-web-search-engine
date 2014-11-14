"""A simple crawler."""

import os
import sys
import urllib2
import urlparse
import socket      # to catch any socket.timeout exceptions read() might throw
import sys         # to get the sys.stdout handle
import pickle
# modules I've written:
from html_parser import SimpleHTMLParser

PAGE_SIZE = 40000


class OutOfUrlsError(Exception):
    """Custom exception raised when the set of urls to crawl is empty."""
    def __init__(self):
        pass
    def __str__(self):
        return 'The set of urls to crawl is empty!'

class Crawler:
    """A simple crawler."""
    
    def __init__(self, num_pages=None, min_page_size=None, seeds=None):
        """Initialize an object."""
        self._to_crawl = set([])        # urls to crawl
        self._crawled = set([])         # urls of crawled pages
        self._url = []                  # urls of saved pages
        # number of pages to download:
        if num_pages is not None:
            self._num_pages = num_pages
        else:
            self._num_pages = 1000
        # minimum page size (in characters)
        if min_page_size is not None:
            self._min_page_size = min_page_size
        else:
            self._min_page_size = 40000
        # initial crawl frontier
        if seeds is not None:
            self._seeds = set(seeds)
        else:
            self._seeds = \
                    set(['http://www.brighthub.com/',
                         'http://www.physicscentral.com/',
                         'http://www.candlelightstories.com/',
                         'http://www.anandtech.com/',
                         'http://www.cnet.com/'])
    
    def reset(self):
        self.__init__()
    
    def crawl(self):
        """
        Find and save 'self._num_pages' html pages, each at least 
        'self._min_page_size' characters long.
        
        seeds (list): start crawling from these urls
        """
        # open './log.txt'
        try:
            log = open('./log.txt', 'w')
        except Exception:
            print "Couldn't open log.txt. All output will go to the screen."
            log = sys.stdout
        # set the crawler's seeds
        self._to_crawl = set(self._seeds)
        # make a directory to save the pages in
        os.mkdir('./html')
        # create a parser (to get each page's links)
        parser = SimpleHTMLParser()
        
        # start gathering pages
        try:
            while len(self._url) < self._num_pages:
                try:
                    crawling = self._to_crawl.pop()
                    print >>log, crawling
                except KeyError as e:
                    # out of urls
                    raise OutOfUrlsError
                
                url = urlparse.urlsplit(crawling)
                try:
                    page_handle = urllib2.urlopen(crawling, timeout=2)
                except:
                    print >>log, '    exception while opening!'
                    continue
                if page_handle.getcode() > 399:
                    # got an HTTP error code, continue to the next link
                    print >>log, '    got HTTP error code!'
                    continue
                
                # check url in case there was a redirection and we ended up on
                # a forbidden page
                if is_no_go_link(urlparse.urlsplit(page_handle.geturl())):
                    print >>log, '    redirected to forbidden page!'
                    continue
                
                # add 'crawling' to the set of all crawled urls
                self._crawled.add(crawling)
                # add page_handle.geturl() too in case we were redirected
                self._crawled.add(page_handle.geturl())
                
                # read page text
                try:
                    page_html = page_handle.read()
                except socket.timeout:
                    print >>log, '    socket timeout!'
                    continue
                except Exception:
                    print >>log, '    problem during page_handle.read()!'
                    continue
                # parse the page
                parser.reset()
                try:
                    parser.parse(page_html)
                except Exception as e:
                    print >>log, '    parser exception!   ---   ' + str(e)
                    continue
                
                # extract hyperlinks
                extract_new_links(url, parser.get_hyperlinks(), self._to_crawl,
                                  self._crawled)
                
                # do the checks (at least 'self._min_page_size' chars, english, etc.)
                ok = self._check_page(page_handle, len(page_html))
                if ok:
                    # give the page an id and save it
                    # the page's position in the _url list will be it's id
                    self._url.append(crawling)
                    save_page(page_html, len(self._url) - 1)
                    # print the number of pages gathered so far
                    print str(len(self._url)) + ' pages'
                else:
                    print >>log, '    page not ok!'
                page_handle.close()
        except KeyboardInterrupt:
            # remember that the while loop was in this try-except block
            # did this to close the log file if an ctrl-c was pressed
            if log is not sys.stdout:
                log.close()
            return False
        # if everything went well close the log file and exit True
        if log is not sys.stdout:
            log.close()
        return True
    
    def get_crawl_frontier(self):
        """Get the crawl frontier - links about to be crawled."""
        return self._to_crawl
    
    def get_crawled_links(self):
        """Get all the crawled links."""
        return self._crawled
    
    def get_page_urls(self):
        """Get the list mapping ids to page urls."""
        return self._url
    
    def get_seeds(self):
        """Get the seeds - the links to start crawling from."""
        return self._seeds
    
    def set_seeds(self, seeds):
        """Set a list of seeds - links to start crawling from."""
        self._seeds = seeds
        return True

    def dump_ids_and_urls(self):
        """
        Export self._url as 'urls.pickle' using pickle. Also create a text 
        file, 'ids_and_urls.txt', mapping page ids to urls.
        """
        with open('urls.pickle', 'w') as f:
            pickle.dump(self._url, f)
        with open('ids_and_urls.txt', 'w') as f:
            for id, url in enumerate(self._url):
                f.write('%-5s %s\n' % (id, url))
    
    def _check_page(self, page_handle, page_length):
        """
        Return True if the downloaded page is at least 'self._min_page_size' 
        characters long, pure html, in english and can be stored, 
        False otherwise.
        
        page_handle: the handle urllib2.urlopen() returns
        page_length: the page's length in characters
        """
        # are we allowed to store the page?
        try:
            if 'no-store' in page_handle.headers.dict['cache-control']:
                return False
        except KeyError:
            pass
        # is the page over self._min_page_size characters long?
        if page_length < self._min_page_size:
            return False
        # is the page pure html?
        if page_handle.info().type != 'text/html':
            return False
        # is the page in english?
        try:
            if page_handle.info().dict['content-language'][0:2] != 'en':
                return False
        except KeyError:
            pass
        return True    

def save_page(page_html, page_id):
    """
    Save the downloaded page on the local file ./html/'page_id'.html.

    page_html (string) : the page's html
    page_id      (int) : the id we gave the page
    """
    with open('./html/' + str(page_id) + '.html', 'w') as f:
        f.write(page_html)
    return True

def extract_new_links(url, links, to_crawl, crawled):
    """
    Add all links in 'links' (except those in 'crawled') into 'to_crawl'.
    Before adding a link check if it's acceptable.
    
    url (like a list) : the current page's split url
    links      (list) : a list of the extracted links
    to_crawl    (set) : links not yet crawled
    crawled     (set) : links already crawled
    """
    for link in links:
        # print >>log, 'found link: ' + link
        try:
            linkurl = urlparse.urlsplit(link.lower())
        except Exception:
            continue
        if is_no_go_link(linkurl):
            continue
        elif not linkurl[1]:
            if link.startswith('/'):
                link = 'http://' + url[1] + link
            else:
                link = 'http://' + url[1] + '/' + link
        elif not linkurl[0]:
            link = 'http://' + link
        if link not in crawled:
            to_crawl.add(link)
    return True

def is_no_go_link(linkurl):
    """
    Return True if the link must be avoided (e.g. a 'mailto:' or '.gov' link).

    linkurl (like list) : the split link
    """
    # block links starting with 'ftp://', 'mailto:' etc.
    if linkurl[0] and not linkurl[0] == 'http':
        return True
    # block anchor urls
    if not linkurl[1] and not linkurl[2]:
        return True
    # block domains other than '.com'
    if linkurl[1]:
        if not linkurl[1].endswith('.com') and \
           not linkurl[1].endswith('.co.uk'):
            return True
        # block '.gov' domains (if anyone passed the previous tests)
        if '.gov' in linkurl[1]:
            return True
        # block wikipedia, twitter and facebook
        if 'twitter.com' in linkurl[1] or \
           'facebook.com' in linkurl[1] or \
           'wikipedia' in linkurl[1] or \
           'imdb' in linkurl[1]:
            return True
    # only allow html pages
    if linkurl[2]:
        if not linkurl[2].endswith('.html') and \
           not linkurl[2].endswith('.htm') and \
           not linkurl[2].endswith('/'):
            return True
    return False

def main():
    """Download 1000 html pages into './html/'."""
    c = Crawler()
    status = c.crawl()
    c.dump_ids_and_urls()
    return status

if __name__ == '__main__':
    status = main()
    sys.exit(status)

