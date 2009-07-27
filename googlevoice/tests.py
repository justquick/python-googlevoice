from googlevoice import Voice
import unittest
import os

class VoiceTest(unittest.TestCase):
    def test_alogin(self):
        self.voice = Voice()
        self.voice.login()
    
    def test_special(self):
        self.assert_(self.voice.special)
        
    def test_call(self):
        pass#voice.call('2025556411','2025551550')

    def test_sms(self):
        pass#voice.sms('2025551550','ismsu')

    def test_cancel(self):
        pass#self.voice.cancel('2025556411','2025551550')

    def test_inbox(self):
        self.assert_(self.voice.inbox())
    
    def test_download(self):
        for msg,_ in self.voice.voicemail()['messages'].items():
            break
        self.voice.download(msg)
        self.assert_(os.path.isfile('%s.mp3' % msg))
    
    def test_zlogout(self):
        self.voice.logout()
        self.assert_(self.voice.special is None)
        
if __name__ == '__main__':
    unittest.main()