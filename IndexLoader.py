"""
A simple XML parser. Parses the XML file we saved the index in
and loads the index on memory.
"""

from xml.sax.handler import ContentHandler

class IndexLoader(ContentHandler):
    """
    A simple XML parser. Parses the XML file we saved the index in
    and loads the index on memory.
    """
    
    def __init__(self):
        self._in_lemma = None
        self.index = {}
    
    def startElement(self, elem, attrs):
        if elem == 'lemma':
            self._in_lemma = attrs.get('name')
            self.index[self._in_lemma] = {}
        elif elem == 'document':
            id, weight = int(attrs.get('id')), float(attrs.get('weight'))
            self.index[self._in_lemma][id] = weight
    
    def get_index(self):
        return self.index

