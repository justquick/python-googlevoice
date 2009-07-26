Python Google Voice
=============

Exposing the Google Voice API to the Python language
----------------------------------------------------

Allows you to place calls, send sms, download voicemail, check the vaious folders of your Google Voice Account

Bladdsa
-------------------------------

1. Download the code from GitHub:

        git clone git://github.com/asdf asdfl

1. Edit `settings.py` and add  `paypal.standard.ipn` to your `INSTALLED_APPS` and `PAYPAL_RECEIVER_EMAIL`:

        # settings.py
        ...
        INSTALLED_APPS = (... 'paypal.standard.ipn', ...)
        ...
        PAYPAL_RECEIVER_EMAIL = "yourpaypalemail@example.com"
