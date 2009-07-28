from googlevoice import settings
from googlevoice.util import *

class Voice(object):
    """
    Main voice instance for interacting with the Google Voice service
    Also contains callable methods for each folder (eg inbox,voicemail,sms,etc)
    """
    def __init__(self):
        try:
            from http.cookiejar import LWPCookieJar as CJ
        except ImportError:
            from cookielib import LWPCookieJar as CJ
        install_opener(build_opener(HTTPCookieProcessor(CJ())))
        
        for name in settings.FEEDS:
            setattr(self, name, self.__multiformat(name))
            setattr(self, '%s_html' % name, self.__multiformat(name, 'html'))

    def __do_page(self, page, data=None, headers={}):
        """
        Loads a page out of the settings and pass it on to urllib Request
        """
        if isinstance(data, dict):
            data = urlencode(data)
        if page == 'download':
            return urlopen(Request(getattr(settings, 'DOWNLOAD') + data))
        return urlopen(Request(getattr(settings, page.upper()), data, headers))

    def __do_special_page(self, page, data=None, headers={}):
        """
        Add self.special to request data
        """
        if isinstance(data, dict):
            data.update({'_rnr_se':self.special})
        return self.__do_page(page, data, headers)
    
    def __do_xml_page(self, page):
        """
        Parses XML folder page (eg inbox,voicemail,sms,etc)
        Returns a str tuple (json format, html format)
        """
        return XMLParser(self.__do_special_page('XML_%s' % page).read())()
    
    def __multiformat(self, page, format='json'):
        """
        Uses json/simplejson to load given format from folder page
        Returns wrapped function available at self.
        """
        def inner():
            if format == 'json':
                return load(StringIO(self.__do_xml_page(page)[0]))
            else:
                return self.__do_xml_page(page)[1]
        inner.__doc__ = 'Formatted %s for the %s' % (format, page)
        return inner
        
    @property
    def special(self):
        """
        Returns special identifier for your session (if logged in)
        """
        import re
        if hasattr(self, '_special') and getattr(self, '_special'):
            return self._special
        try:
            regex = bytes("('_rnr_se':) '(.+)'", 'utf8')
        except NameError:
            regex = r"('_rnr_se':) '(.+)'"
        try:
            sp = re.search(regex, urlopen(settings.INBOX).read()).group(2)
        except AttributeError:
            sp = None
        self._special = sp
        return sp
    
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
        
        self.__do_page('LOGIN', {'Email':email,'Passwd':passwd})
        
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
        del self._special 
        assert self.special == None
    
    def call(self, outgoingNumber, forwardingNumber, subscriberNumber=None):
        """
        Make a call to an outgoing number using your forwarding number
        """
        self.__do_special_page('CALL', {
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
        self.__do_special_page('CANCEL', {
            'outgoingNumber':outgoingNumber or 'undefined',
            'forwardingNumber':forwardingNumber or 'undefined',
            'cancelType': 'C2C',
        })

    def send_sms(self, phoneNumber, text):
        """
        Send an SMS message to a given phone number with the given text message
        """
        self.__do_special_page('SMS', {
            'phoneNumber': phoneNumber,
            'text': text,
        })
        
    def download(self, msg, adir='.'):
        """
        Download a voicemail MP3 matching the given msg sha1 hash
        Saves files to adir (default current directory)
        Message hashes can be found in list(self.voicemail()['messages'])
        Returns location of saved file
        """
        from os.path import join
        for c in msg:
            assert c in '0123456789abcdef', 'Message id not a sha1 hash'
        fn = join(adir, '%s.mp3' % msg)
        fo = open(fn, 'wb')
        fo.write(self.__do_page('download', msg).read())
        fo.close()
        return fn
        