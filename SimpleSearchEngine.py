"""A simple engine to query the index."""

import time
import operator
import pickle

import crawler
import preprocessor
import morphosyntactic
import indexer
import save_and_load

class NoIndexError(Exception):
    """
    Exception produced when the search engine's index hasn't been initialized.
    """
    
    def __init__(self):
        pass
    
    def __str__(self):
        return 'The search engine\'s index has not been initialized.'

class NoUrlMapError(Exception):
    """
    Exception produced when the search engine's id-to-url map (urls) hasn't 
    been initialized.
    """
    
    def __init__(self):
        pass
    
    def __str__(self):
        return 'The search engine\'s id-to-url map has not been initialized.'

class SimpleSearchEngine:
    """A simple engine to query the index."""
    
    def __init__(self, index=None, urls=None):
        """
        __init__(self, index=None, urls=None): Create a new SearchEngine.
        'index' can be an existing index
        'urls' can be a list mapping page ids to urls
        """
        self._index = index
        self._urls = urls
    
    def query(self, input):
        """
        query(input): 'input' is a string. Clean, tokenize and lemmatize it, 
        make the query and print the results.
        """
        # clean input:
        query = preprocessor.clean_query(input)
        lemmas = morphosyntactic.lemmatize_query(query)
        # make the query:
        results = self.simple_query(lemmas)
        return results
    
    def simple_query(self, lemmas):
        """
        simple_query(self, lemmas): Make a query to the index. 'lemmas' is 
        a list of lemmas to search for.
        
        simple_query() returns a list of (url, weight) tuples sorted by weight
        in descending order.
        """
        if self._index == None:
            raise NoIndexError
        if self._urls == None:
            raise NoUrlMapError
        if len(lemmas) == 0:
            return []
        # a dict mapping urls to importance according to the query:
        results = {}
        for lemma in lemmas:
            try:
                for id, weight in self._index[lemma].iteritems():
                    # increase the page's importance by 'weight':
                    results[self._urls[id]] = results.get(self._urls[id], 
                                                          0.0) + weight
            except KeyError:
                # 'lemma' was not in the index
                continue
        # sort by weight (descending order) and return
        return sorted(results.iteritems(), key=operator.itemgetter(1), 
                      reverse=True)
    
    def evaluate(self, queries, repeat=1):
        """
        evaluate(self, queries, repeat=1): Run a series of queries 'repeat' 
        times and return the average time. 'queries' is a list of lists 
        containing strings. 
        
        Each list is a query and each string (inside the lists) is a lemma 
        to search for.
        """
        start = time.clock()
        for i in xrange(repeat):
            for query in queries:
                self.simple_query(query)
        stop = time.clock()
        return (stop - start) / (len(queries) * repeat)
    
    def load_index_and_urls(self, index_file=None, urls_file=None):
        """
        load_index(self, index_file=None, urls_file=None): Load the index
        and urls from files.
        """
        if index_file is None:
            index_file = 'index.xml'
        with open(index_file, 'r') as f:
            self._index = save_and_load.load_index(f)
        if urls_file is None:
            urls_file = 'urls.pickle'
        with open(urls_file, 'r') as f:
            self._urls = pickle.load(f)
    
    def set_index_and_urls(self, index, urls):
        """
        set_index_and_urls(self, index, urls): Use an existing index
        and url map.
        """
        self._index = index
        self._urls = urls
    
    def make_index_and_urls(self):
        """
        make_index_and_urls(self): Make an index and a url-map from scratch.
        """
        c = crawler.Crawler()
        c.crawl()
        self._urls = c.get_page_urls()
        preprocessor.clean_and_tokenize_all()
        self._index = indexer.make_index(tagged=False)

