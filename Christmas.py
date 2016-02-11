# -*- coding: utf-8-*-
import re
import subprocess

WORDS = ["CHRISTMAS"]

def handle(text, mic, profile):
    """
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
	
    mic.say("Merry Christmas.")
    subprocess.call("omxplayer ~/TheFirstNoel.mp3",shell=True)


def isValid(text):
    """
        Returns True if input is related to the beep.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bchristmas\b', text, re.IGNORECASE))
