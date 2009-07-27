from googlevoice import Voice
from googlevoice.util import input

voice = Voice()
voice.login()

for msg in list(voice.voicemail()['messages']):
    voice.download(msg)