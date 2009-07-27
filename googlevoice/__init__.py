import os
import re

try:
    from urllib2 import build_opener,install_opener,HTTPCookieProcessor,Request,urlopen
    from urllib import urlencode,urlretrieve
except ImportError:
    from urllib.request import urlretrieve,build_opener,install_opener,HTTPCookieProcessor,Request,urlopen
    from urllib.parse import urlencode
try:
    from io import StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO


from googlevoice import settings
from googlevoice.util import *

class Voice(object):
    """
    Main voice instance for interacting with the Google Voice service
    """
    def __init__(self):
        self.jar = LWPCookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.jar))
        install_opener(self.opener)
        
        for name in settings.FEEDS:
            setattr(self, name, self._multiformat(name))
            setattr(self, '%s_html' % name, self._multiformat(name, 'html'))

    def _do_page(self, page, data=None, headers={}):
        if isinstance(data, dict):
            data = urlencode(data)
        if page == 'download':
            return urlopen(Request(getattr(settings, 'DOWNLOAD') + data))
        return urlopen(Request(getattr(settings, page.upper()), data, headers))

    def _do_special_page(self, page, data=None, headers={}):
        if isinstance(data, dict):
            data.update({'_rnr_se':self.special})
        return self._do_page(page, data, headers)
    
    def _do_xml_page(self, page):
        return XMLParser(self._do_special_page('XML_%s' % page).read()).grab()
    
    def _multiformat(self, page, format='json'):
        def inner():
            if format == 'json':
                return load(StringIO(self._do_xml_page(page)[0]))
            else:
                return self._do_xml_page(page)[1]
        inner.__doc__ = 'Formatted %s for the %s feed' % (format, page)
        return inner
        
    @property
    def special(self):
        """
        Returns special identifier for your session (if logged in)
        """
        try:
            regex = bytes("('_rnr_se':) '(.+)'", 'utf8')
        except NameError:
            regex = r"('_rnr_se':) '(.+)'"
        try:
            return re.search(regex, urlopen(settings.INBOX).read()).group(2)
        except AttributeError:
            return None
    
    def login(self, email=None, passwd=None):
        """
        Login to the service using your Google Voice account
        Credentials will be propmpted for if not given
        """
        if email is None:
            email = input('Email address: ')
        
        if passwd is None:
            from getpass import getpass
            passwd = getpass()
        
        self._do_page('LOGIN',
            {'Email':email,'Passwd':passwd},
            {'Content-Type':'application/x-www-form-urlencoded'}
        )
        
        del email,passwd
        
        try:
            assert self.special
        except (AssertionError, AttributeError):
            raise LoginError
        
    def logout(self):
        """
        Logs out an instance and makes sure it does not still have a session
        """
        urlopen(settings.LOGOUT)
        assert self.special == None
    
    def call(self, outgoingNumber, forwardingNumber, subscriberNumber=None):
        """
        Make a call to an outgoing number using your forwarding number
        """
        self._do_special_page('CALL', {
            'outgoingNumber':outgoingNumber,
            'forwardingNumber':forwardingNumber,
            'subscriberNumber':subscriberNumber or 'undefined',
            'remember':'0',
        })
    __call__ = call
    
    def cancel(self, outgoingNumber=None, forwardingNumber=None):
        """
        Cancels a call matching outgoing and forwarding numbers (if given)
        Will raise an error if no matching call is being placed
        """
        self._do_special_page('CANCEL', {
            'outgoingNumber':outgoingNumber or 'undefined',
            'forwardingNumber':forwardingNumber or 'undefined',
            'cancelType': 'C2C',
        })

    def sms(self, phoneNumber, text):
        """
        Send an SMS message to a given phone number with the given text message
        """
        self._do_special_page('SMS', {
            'phoneNumber': phoneNumber,
            'text': text,
        })
        
    def download(self, msg, adir='.'):
        """
        Download a voicemail MP3 matching the given msg sha1 hash
        Saves files to adir (default current directory)
        ( Message hashes can be found in self.voicemail()['messages'].keys() )
        """
        fo = open(os.path.join(adir, '%s.mp3' % msg), 'wb')
        fo.write(self._do_page('download', msg).read())
        fo.close()
        