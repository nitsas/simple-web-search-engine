"""
A simple morphosyntactic analyser.

Will call gposttl (works on linux and mac os x).
"""

import os
import sys
import subprocess

def tag_file(filename, to_file=None):
    """
    Tag and lemmatize every word in the tokenized file 'filename'.
    
    If 'to_file' is given redirect gposttl's output to file 'to_file'.
    """
    if to_file is not None:
        # output from gposttl goes to file 'to_file'
        with open(to_file, 'w') as f:
            p = subprocess.Popen(['gposttl', '--silent', filename], 
                                 shell=False, stdout=f, stderr=subprocess.PIPE)
            p.wait()
        return p.returncode
    else:
        # return output from gposttl as a string
        p = subprocess.Popen(['gposttl', '--silent', filename], shell=False, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tagged_text = p.stdout.read()
        p.wait()                # not really needed this time
        return tagged_text.rstrip()

def lemmatize_query(query):
    """
    lemmatize_query(query): 'query' is a string. Lemmatize it using gposttl
    and return a tuple of lemmas.
    """
    p = subprocess.Popen('gposttl --silent << -end- \n' + query + '\n', 
                         shell=True, executable='/bin/bash', 
                         stdout=subprocess.PIPE)
    # -end- is a delimiter but we don't have to use one at the end too
    # I think subprocess sends a Ctrl-D to gposttl when the input string ends
    lemmas = []
    for line in p.stdout.read().splitlines():
        if '<unknown>' in line:
            continue
        else:
            (word, tag, lemma) = line.split()
            lemmas.append(lemma)
    return lemmas

def tag_and_lemmatize_all(verbose=True):
    """
    Tag and lemmatize files 'tokenized/0.txt' - 'tokenized/999.txt'.
    The result of tagging 'tokenized/x.txt' will be saved as 'tagged/x.txt'.
    """
    try:
        os.mkdir('tagged')
    except OSError:
        pass
    for id in xrange(1000):
        if verbose:
            print 'Tagging \'tokenized/' + str(id) + '.txt\' ... ',
        tag_file('tokenized/' + str(id) + '.txt', 'tagged/' + str(id) + '.txt')
        if verbose:
            print '   done!'
    return True

def main():
    """
    Tag and lemmatize files 'tokenized/0.txt' - 'tokenized/999.txt'.
    The result of tagging 'tokenized/x.txt' will be saved as 'tagged/x.txt'.
    
    If a single filename is given as an argument tag and lemmatize the
    file and print output to stdout.
    """
    if len(sys.argv) > 2:
        # more than one argument was given (error!)
        sys.stderr.write('Error: Expected at most one argument, got:\n   ')
        sys.stderr.write(''.join([' ' + arg for arg in sys.argv[1:]]) + '\n')
        return 2
    elif len(sys.argv) == 2:
        # exactly 1 argument was given (it's supposed to be a filename)
        if os.path.isfile(sys.argv[1]):
            tagged_text = tag_file(sys.argv[1])
            print tagged_text
            return 0
        else:
            sys.stderr.write('Error: File ' + sys.argv[1] + \
                             ' does not exist!\n')
            return 1
    else:
        # no arguments were given - tag and lemmatize files
        # 'tokenized/0.txt' - 'tokenized/999.txt'
        tag_and_lemmatize_all()
        return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)

