from googlevoice import Voice
from googlevoice.util import input
from pprint import pprint

voice = Voice()
voice.login()

pprint(getattr(voice,input('Folder to browse: '))())