"""Subsystem #5: make the inverted index."""

import sys
import time
import pickle
from math import log10
# modules I've written:
import morphosyntactic
import vector_space
import save_and_load

def make_index(tagged=True, time_it=False):
    """
    make_index(tagged=True, time_it=False): Make and return the inverted index.
    (using the vector_space and, if tagged=False, the morphosyntactic module)

    If 'time_it' == True, time the whole thing and return a tuple 
    (index, time_passed).
    """
    if time_it:
        time_start = time.time()
    # Call vector_space's functions on each of the files 'tagged/0.txt' - 
    # 'tagged/999.txt'.
    index = {}
    for id in xrange(1000):
        # Check if the files need to be tagged:
        if tagged:
            # The files have already been tagged. (called from main())
            print 'Processing document ' + str(id) + ' ... ',
            # 'id' is of course the current document's id
            filename = 'tagged/' + str(id) + '.txt'
            text = vector_space.remove_stopwords_from_file(filename)
        else:
            # The files in 'tokenized/' need to be tagged. 
            # (called from search_engine.py)
            print 'Tagging tokenized/' + str(id) + '.txt ... ',
            text = morphosyntactic.tag_file('tokenized/' + str(id) + '.txt')
            print '   done!'
            print 'Processing ... ',
            text = vector_space.remove_stopwords(text)
        d = vector_space.make_dict_of_lemmas(text)
        # 'd' contains the tf(term, id) for every term 'term' in 'id'
        for term, tf in d.iteritems():
            # index[term] is now a dictionary
            index.setdefault(term, {})
            index[term][id] = tf
            # we'll multiply by "term's" idf later
        print '   done!'
    print 'Postprocessing index ... ',
    # if gposttl couldn't tag and lemmatize some word it would output <unknown>
    # so delete key <unknown> from the dictionary
    try:
        del(index['<unknown>'])
    except KeyError:
        pass
    # so far we've only calculated each term's tf for every document
    # multiply by each term's idf to get the real weight
    for term, weight in index.iteritems():
        for id in weight.iterkeys():
            # multiply by idf(term) --- idf(term) = log10(1000.0 / len(weight))
            weight[id] *= log10(1000.0 / len(weight))
    print '   done!'
    # stop timing (if time_it == True):
    if time_it:
        time_passed = time.time() - time_start
        return index, time_passed
    else:
        return index

def main():
    """
    Tag files tokenized/0.txt - tokenized/999.txt, use them to make the 
    inverted index and save it on disk. (using save_and_load.py)

    preprocessor.py must have already been called
    """
    d = make_index(tagged=False)
    print 'Saving index file as \'index.xml\' ... ',
    with open('index.xml', 'w') as f:
        save_and_load.save_index(d, f)
    print '   done!'
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)

