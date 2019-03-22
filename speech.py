"""
The speak module.

Created on 22.11.2018

@author: Ruslan Dolovanyuk

"""

import logging
import sys
import time

import win32com.client

import Tolk


class Speech:
    """The speak class for speak voice."""

    def __init__(self, config):
        """Initialize speech class."""
        self.log = logging.getLogger()
        self.log.info('def ' + self.__init__.__name__ + ': ' + self.__init__.__doc__)

        self.config = config

        self.svs_flags_async = 1
        self.speaker = win32com.client.Dispatch("Sapi.SpVoice")
        self.voices = self.speaker.GetVoices()
        self.voices_ids = [voice.Id for voice in self.voices]
        self.voices_names = [voice.GetDescription() for voice in self.voices]

        self.sapi = self.config.getboolean('speech', 'sapi')
        self.set_voice(self.config.getint('speech', 'voice'))
        self.speaker.Rate = self.config.getint('speech', 'rate')
        self.speaker.Volume = self.config.getint('speech', 'volume')

        self.error = False
        Tolk.load()
        self.name = Tolk.detect_screen_reader()
        if not self.name:
            self.error = True
            print('Not find supported screen reader')
        if not Tolk.has_speech():
            self.error = True
            print('Screen reader nottsupport speak text')

        self.set_speak_out()

    def finish(self):
        """Unload Tolk."""
        self.log.info('def ' + self.finish.__name__ + ': ' + self.finish.__doc__)

        Tolk.unload()

    def set_voice(self, index):
        """Set voice for speak."""
        self.log.info('def ' + self.set_voice.__name__ + ': ' + self.set_voice.__doc__)

        try:
            self.speaker.Voice = self.voices[index]
        except:  # pylint: disable=W0702
            print('error: do not set voice')

    def set_speak_out(self):
        """Set speak out: tolk or sapi."""
        self.log.info('def ' + self.set_speak_out.__name__ + ': ' + self.set_speak_out.__doc__)

        if self.error and self.sapi:
            self.speak = self.speak_sapi
        else:
            self.speak = self.speak_tolk

    def speak_tolk(self, phrase):
        """Speak phrase with tolk."""
        self.log.info('def ' + self.speak_tolk.__name__ + ': ' + self.speak_tolk.__doc__)
        self.log.info('phrase: ' + phrase)

        Tolk.output(phrase)

    def speak_sapi(self, phrase):
        """Speak phrase in sapi voice."""
        self.log.info('def ' + self.speak_sapi.__name__ + ': ' + self.speak_sapi.__doc__)
        self.log.info('phrase: ' + phrase)

        self.speaker.skip("Sentence", sys.maxsize)
        self.speaker.Speak(phrase, self.svs_flags_async)
        time.sleep(0.1)
