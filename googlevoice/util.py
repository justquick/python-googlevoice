import xml.parsers.expat


try:
    from http.cookiejar import LWPCookieJar
except ImportError:
    from cookielib import LWPCookieJar
try:
    from json import load
except ImportError:
    from simplejson import load


try:
    input = raw_input
except NameError:
    pass

class LoginError(Exception): pass
    
class XMLParser(dict):
    """
    XML Parser helper that can dig json and html out of the feeds
    """
    attr = None
    def start_element(self, name, attrs):
        if name in ('json','html'):
            self.attr = name
    def end_element(self, name):
        self.attr = None
    def char_data(self, data):
        if self.attr and data:
            self[self.attr] += data

    def __init__(self, data):
        dict.__init__(self, {'json':'','html':''})
        p = xml.parsers.expat.ParserCreate()
        
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        p.Parse(data, 1)

    def grab(self):
        return self['json'],self['html']