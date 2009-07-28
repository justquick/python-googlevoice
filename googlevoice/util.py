import xml.parsers.expat
try:
    from urllib2 import build_opener,install_opener, \
        HTTPCookieProcessor,Request,urlopen
    from urllib import urlencode,urlretrieve
except ImportError:
    from urllib.request import urlretrieve,build_opener,install_opener, \
        HTTPCookieProcessor,Request,urlopen
    from urllib.parse import urlencode
try:
    from io import StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
try:
    from json import load
except ImportError:
    from simplejson import load
try:
    input = raw_input
except NameError:
    pass

class LoginError(Exception): pass
class ParsingError(Exception): pass

class XMLParser(dict):
    """
    XML Parser helper that can dig json and html out of the feeds
    """
    attr = None
    def start_element(self, name, attrs):
        if name in ('json','html'):
            self.attr = name
    def end_element(self, name): self.attr = None
    def char_data(self, data):
        if self.attr and data:
            self[self.attr] += data

    def __init__(self, data):
        dict.__init__(self, {'json':'','html':''})
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        try:
            p.Parse(data, 1)
        except:
            raise ParsingError

    def __call__(self):
        return self['json'],self['html']