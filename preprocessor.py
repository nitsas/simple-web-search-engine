"""
Will clean and tokenize a file containing HTML.

If the module is imported just use clean_and_tokenize() to do the job.
"""

import os
import sys
import string
import re
import nltk

_HTML_APOSTROPHE_RE = re.compile('(&rsquo;)|(&apos;)|(&#39;)')
_HTML_OR_URL_ENTITY_RE = re.compile(r'(&[a-zA-Z]+;)|(&#\d+;)|(%[\da-fA-F]{2})')
_HYPHEN_BETWEEN_WORDS_RE = re.compile('(?<=[a-zA-Z])-(?=[a-zA-Z])')
_APOSTROPHE_BETWEEN_WORDS_RE = re.compile('(?<=[a-zA-Z])\'(?=[a-zA-Z])')
_HYPHENS_AND_APOSTROPHES_TRANS = string.maketrans('-\'', '  ')
_TO_HYPHENS_AND_APOSTROPHES_TRANS = string.maketrans('@$', '-\'')
_NON_ASCII_OR_PUNCTUATION_RE = re.compile(r'[^\sa-zA-Z0-9\'-]+')

def clean_and_tokenize(html):
    """Clean and tokenize a text containing HTML."""
    # Remove the HTML tags etc.
    text = nltk.clean_html(html)
    # Remove HTML entities, punctuation, etc.
    text = clean_more(text)
    # Tokenize.
    text = tokenize(text)
    return text

def tokenize(text):
    """Tokenize the input. The output will have only one word per line."""
    return '\n'.join(text.split())

def clean_more(text):
    """
    Remove  punctuation, HTML entities and non-ASCII characters.
    
    A hyphen "-" connecting words won't be replaced. (e.g. multi-colored)
    An apostrophe "'" between words won't be replaced. (e.g. I've)
    """
    # Change HTML apostrophes into '.
    text = _HTML_APOSTROPHE_RE.sub('\'', text)
    # Remove HTML entities (e.g. &nbsp;) or URL encoded characters (e.g. %20).
    text = _HTML_OR_URL_ENTITY_RE.sub(' ', text)
    # Remove non-ASCII chars and all punctuation except hyphens and apostrophes.
    text = _NON_ASCII_OR_PUNCTUATION_RE.sub(' ', text)
    # Change hyphens connecting words into @.
    text = _HYPHEN_BETWEEN_WORDS_RE.sub('@', text)
    # Change apostrophes between words into $.
    text = _APOSTROPHE_BETWEEN_WORDS_RE.sub('$', text)
    # Remove all remaining hyphens and apostrophes.
    text = text.translate(_HYPHENS_AND_APOSTROPHES_TRANS)
    # Change @ into hyphens and $ into apostrophes.
    text = text.translate(_TO_HYPHENS_AND_APOSTROPHES_TRANS)
    return text

def clean_query(query):
    """Remove non-ASCII chars and punctuation (except '-' connecting words)."""
    # Remove non-ASCII chars and all punctuation except hyphens and apostrophes.
    query = _NON_ASCII_OR_PUNCTUATION_RE.sub(' ', query)
    # Change hyphens connecting words into @.
    query = _HYPHEN_BETWEEN_WORDS_RE.sub('@', query)
    # Change apostrophes between words into $.
    query = _APOSTROPHE_BETWEEN_WORDS_RE.sub('$', query)
    # Remove all remaining hyphens and apostrophes.
    query = query.translate(_HYPHENS_AND_APOSTROPHES_TRANS)
    # Change @ into hyphens and $ into apostrophes.
    query = query.translate(_TO_HYPHENS_AND_APOSTROPHES_TRANS)
    return query

def clean_and_tokenize_all():
    """
    Clean and tokenize files 'html/0.html' - 'html/999.html'.
    After file 'html/x.html' is tokenized it will be saved as 
    'tokenized/x.html'.
    """
    # make directory 'tokenized/' if it doesn't already exist
    os.mkdir('tokenized')
    # process files 'html/1.html' - 'html/999.html'
    for id in xrange(1000):
        print 'processing ' + str(id) + '.html ...',
        with open('html/' + str(id) + '.html', 'r') as f:
            html = f.read()
        tokenized_text = clean_and_tokenize(html)
        with open('tokenized/' + str(id) + '.txt', 'w') as f:
            f.write(tokenized_text)
        print '     done!'

def main():
    """
    Clean and tokenize files '0.html' - '999.html' in 'html/'. After file
    'html/x.html' is tokenized it will be saved as 'tokenized/x.html'.
    
    If an argument (filename) was given, clean, tokenize and print its contents.
    """
    if len(sys.argv) > 2:
        # more than 1 argument was given (error!)
        sys.stderr.write('Error: Expected at most one argument, got:\n   ')
        sys.stderr.write(''.join([' ' + arg for arg in sys.argv[1:]]) + '\n')
        return 2
    elif len(sys.argv) == 2:
        # exactly 1 argument was given (assume it's a filename)
        try:
            with open(sys.argv[1], 'r') as f:
                html = f.read()
        except IOError as e:
            sys.stderr.write('Error: ' + str(e) + '\n')
            return 1
        print clean_and_tokenize(html)
        return 0
    else:
        # no arguments were given - clean and tokenize pages 0-999 in './html'
        clean_and_tokenize_all()
        return 0


# The module takes a filename as input, tokenizes and prints its contents. 
if __name__ == '__main__':
    status = main()
    sys.exit(status)

