"""A simple HTML parser based on sgmllib's SGMLParser."""

from sgmllib import SGMLParser

class SimpleHTMLParser(SGMLParser):
    """A simple HTML parser based on sgmllib's SGMLParser."""
    
    def __init__(self):
        SGMLParser.__init__(self)
        self.hyperlinks = []
    
    def reset(self):
        SGMLParser.reset(self)
        self.hyperlinks = []
    
    def parse(self, text):
        self.feed(text)
        self.close()
    
    def unknown_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.hyperlinks.append(value)
    
    def unknown_endtag(self, tag):
        pass
    
    def handle_charref(self, ref):
        pass
    
    def handle_entityref(self, ref):
        pass
    
    def handle_data(self, text):
        pass
    
    def handle_comment(self, text):
        pass
    
    def handle_pi(self, text):
        pass
    
    def handle_decl(self, text):
        pass
    
    def get_hyperlinks(self):
        return self.hyperlinks
    
    def get_clean_text(self):
        return self.clean_text


