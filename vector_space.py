"""
Subsystem #4: from webpages to the vector space model.

Remove stop words from a tagged text and count every lemma's frequency.
"""

import os
import sys
import pickle

_CLOSED_CLASS_CATEGORIES = ['CD', 'CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT',
                            'POS', 'PP', 'PP$', 'PRP', 'PRP$', 'RP', 'TO',
                            'UH', 'WDT', 'WP', 'WP$', 'WRB']
_OPEN_CLASS_CATEGORIES = ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'NN', 'NNS',
                          'NP', 'NPS', 'FW', 'VV', 'VVD', 'VVG', 'VVN', 'VVP',
                          'VVZ', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'VH',
                          'VHD', 'VHG', 'VHN', 'VHP', 'VHZ']
_IS_CLOSED_CLASS = dict([(tag, True) for tag in _CLOSED_CLASS_CATEGORIES])
_IS_CLOSED_CLASS.update([(tag, False) for tag in _OPEN_CLASS_CATEGORIES])

def remove_stopwords(text):
    """
    Remove words with a closed class category PoS tag and return the rest 
    as a string.

    'text' is a string with lines of the form:
    word tag lemma
    (the lemma is optional)
    Lines with a closed class category tag are removed.
    """
    output = ''
    for line in text.splitlines():
        try:
            (word, tag, lemma) = line.split()
        except ValueError:
            # found a wrongly formatted line - ignore it
            continue
        if not _IS_CLOSED_CLASS[tag]:
            output += line + '\n'
    return output

def remove_stopwords_from_file(filename):
    """
    Remove words with a closed class category PoS tag and return what's left 
    as a string.

    File 'filename' is a file with lines of the form:
    word tag lemma
    (the lemma is optional)
    Lines with a closed class category tag are removed.
    """
    output = ''
    with open(filename, 'r') as f:
        for line in f:
            try:
                (word, tag, lemma) = line.split()
            except ValueError:
                # found a wrongly formatted line - ignore it
                continue
            if not _IS_CLOSED_CLASS[tag]:
                output += line + '\n'
    return output

def make_dict_of_lemmas(text):
    """
    Return a dictionary with one entry for every lemma in 'text'.
    key = lemma, value = lemma's frequency (tf)

    'text' is a string with lines of the form:
    word tag lemma
    """
    d = {}
    word_count = 0
    for line in text.splitlines():
        try:
            (word, tag, lemma) = line.split()
        except ValueError:
            # found a wrongly formatted line - ignore it
            continue
        d[lemma] = d.get(lemma, 0) + 1
        word_count += 1
    # now d[w] is w's term count - divide by 'word_count' 
    # to get the term frequency
    for lemma, term_count in d.iteritems():
        d[lemma] = term_count / float(word_count)
    return d

def main():
    """
    Remove stopwords and make a dictionary of lemma frequencies for files 
    'tagged/0.txt' - 'tagged/999.txt'. The dictionary for file 'tagged/x.txt'
    will be saved as 'vector_space/x.pickle' using the pickle module.

    If there were any arguments assume they are filenames and do all the above
    for them.
    """
    try:
        os.mkdir('vector_space')
    except OSError:
        pass
    if len(sys.argv) == 1:
        # no arguments - take care of files 'tagged/0.txt' - 'tagged/999.txt'
        for id in xrange(1000):
            print 'Processing \'tagged/' + str(id) + '.txt\' ... ',
            text = remove_stopwords_from_file('tagged/' + str(id) + '.txt')
            d = make_dict_of_lemmas(text)
            with open('vector_space/' + str(id) + '.pickle', 'w') as f:
                pickle.dump(d, f)
            print '   done!'
        return 0
    else:
        # sys.argv[1:] is a list of filenames
        for filename in sys.argv[1:]:
            try:
                print 'Processing \'' + filename + '\' ... ',
                text = remove_stopwords_from_file(filename)
                d = make_dict_of_lemmas(text)
                with open('vector_space/' + os.path.split(filename)[1] + \
                         '.pickle', 'w') as f:
                    pickle.dump(d, f)
                print '   done!'
            except IOError:
                # file 'filename' didn't exist
                print '   not a file!'
                continue
        return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)

