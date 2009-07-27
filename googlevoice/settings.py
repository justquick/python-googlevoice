LOGIN = 'https://www.google.com/accounts/ServiceLoginAuth?service=grandcentral'
FEEDS = ('inbox','starred','all','spam','trash','voicemail','sms','recorded','placed','recieved','missed')

BASE = 'https://www.google.com/voice/'
LOGOUT = BASE+'account/signout'
INBOX = BASE+'#inbox'

CALL = BASE+'call/connect/'
CANCEL = BASE+'call/cancel/'
SMS = BASE+'sms/send/'
DOWNLOAD = BASE+'media/send_voicemail/'

XML_BASE = BASE+'inbox/recent/'
XML_INBOX = XML_BASE+'inbox/'
XML_STARRED = XML_BASE+'starred/'
XML_ALL = XML_BASE+'add/'
XML_SPAM = XML_BASE+'spam/'
XML_TRASH = XML_BASE+'trash/'
XML_VOICEMAIL = XML_BASE+'voicemail/'
XML_SMS = XML_BASE+'sms/'
XML_RECORDED = XML_BASE+'recorded/'
XML_PLACED = XML_BASE+'placed/'
XML_RECIEVED = XML_BASE+'recieved/'
XML_MISSED = XML_BASE+'missed/'
