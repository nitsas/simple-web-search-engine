"""Subsystem #6: save and load the index."""

from xml.sax import make_parser
from xml.sax.handler import feature_namespaces

import IndexLoader


def save_index(index, file):
    """
    save_index(index, file): Save the index as an xml file.
    
    'file' is an open file object.
    """
    file.write('<inverted_index>\n')
    for lemma, weights in index.iteritems():
        file.write('\t<lemma name="' + lemma + '">\n')
        for id, weight in weights.iteritems():
            file.write('\t\t<document id="' + str(id) + '" weight="' + \
                       str(weight) + '"/>\n')
        file.write('\t</lemma>\n')
    file.write('</inverted_index>')

def load_index(file):
    """
    load_index(file): Load the index from an xml file (using xml.sax).

    'file' is an open file object.
    """
    # create a parser:
    parser = make_parser()
    # tell the parser we are not interested in XML namespaces:
    parser.setFeature(feature_namespaces, 0)
    # create a handler (type IndexLoader):
    handler = IndexLoader.IndexLoader()
    # tell the parser to use our handler:
    parser.setContentHandler(handler)
    # now parse 'index.xml':
    parser.parse(file)
    # return the index:
    return handler.get_index()

