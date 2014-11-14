"""Subsystem #7: evaluate the index (evaluate_index.py)."""

import os
import sys
import getopt

import SimpleSearchEngine

def loop(searcher):
    """
    loop(searcher): Display a prompt through which a user can make a query.
    
    Loop until the user presses Ctrl-D.
    'searcher' is a SimpleSearchEngine instance.
    """
    # loop until Ctrl-D is pressed
    while True:
        # get input
        try:
            input = raw_input('Search for lemmas (type Ctrl-D to exit):\n>')
        except EOFError:
            print
            break
        # check if we're running on linux or windows
        if os.name != 'nt':
            # we're on linux (or mac)
            # clean input, make query and print results
            results = searcher.query(input)
        else:
            # we're on windows (cannot clean input -> need TreeTagger)
            # just do a simple query (split the input into words first)
            results = searcher.simple_query(input.split())
        # print results:
        if len(results):
            print 'Results:'
            for url, weight in results:
                print '  ' + url + '    ' + str(weight)
        else:
            print 'Sorry, no files match the query.. Please try again'
        print 

def evaluate(searcher, queries=None, repeat=100):
    """
    evaluate(searcher, queries=None, repeat): Run a series of queries 
    on the index 'repeat' times and return the average query time.

    'searcher' is a SimpleSearchEngine instance (contains the index)
    'queries' is a list of lists containing strings (the queries)
    'repeat' is an integer (number of times to run the queries)
    """
    if queries == None:
        # default: ten 1-word, four 2-word and one 3-word queries
        queries = [['whitney'], ['something'], ['cpu'], ['mobile'], ['web'],
                   ['algorithm'], ['not-a-word'], ['job'], ['record'],
                   ['linux'], ['whale', 'sea'], ['whatever', 'happen'],
                   ['mobile', 'job'], ['coffee', 'sleep'],
                   ['economy', 'market', 'capital']]
    avg_time = searcher.evaluate(queries, repeat)
    return avg_time

def _print_help():
    """
    Show the command line user info about expected command line arguments etc.
    """
    print 'Index evaluation. (evaluate_index.py)\n'
    print 'usage: evaluate_index.py [arguments]\n'
    print 'Arguments: '
    print '   -h or --help                      display this help message'
    print '   -i <file> or --index=<file>       load index from file <file>'
    print '   -u <file> or --urls=<file>        load url-map from file <file>'
    print '   -m or --makeindex                 make index file from scratch '
    print '                                     (overrides -i and -u)'

def main(argv):
    """
    main(args): Let the user make queries to the index. 
    'argv' is a list of command line arguments (sys.argv[1:])
    
    If --help or -h was specified display help.
    If --index=filename or -i filename was specified load the index 
    from file 'filename'.
    If --urls=filename or -u filename was specified load the url-map
    from file 'filename'.
    If --makeindex or -m  was specified create the index and url-map 
    from scratch. 
    If no argument was given for the index or url-map they will be loaded 
    from 'index.xml' and 'urls.pickle' respectively.
    """
    # parse command line arguments:
    try:
        opts, args = getopt.getopt(argv, 'hi:u:m', ['help', 'index=', 
                                                    'urls=', 'makeindex'])
    except getopt.GetoptError:
        # print help
        _print_help()
        return 2
    # initialize variables:
    index_file = 'index.xml'
    urls_file = 'urls.pickle'
    make_index = False
    # check command line arguments:
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            _print_help()
            return 0
        elif opt in ('-i', '--index'):
            index_file = arg
            continue
        elif opt in ('-u', '--urls'):
            urls_file = arg
            continue
        elif opt in ('-m', '--makeindex'):
            make_index = True
    # main:
    searcher = SimpleSearchEngine.SimpleSearchEngine()
    if make_index:
        print 'An index will be created from scratch. (CTRL-C to exit)' 
        print 'Please be patient, this will take a while..'
        searcher.make_index_and_urls()
    else:
        print 'Loading index and url-map..'
        searcher.load_index_and_urls(index_file, urls_file)
    loop(searcher)
    return 0

if __name__ == '__main__':
    status = main(sys.argv[1:])
    sys.exit(status)

