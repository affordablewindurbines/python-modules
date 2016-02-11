# -*- coding: utf-8-*-
import re
import subprocess

WORDS = ["BEEP"]

def handle(text, mic, profile):
	
    mic.say("OK.")
    subprocess.call("/home/pi/routines/sudoBeeper",shell=True)

def isValid(text):
    """
        Returns True if input is related to the beep.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bbeep\b', text, re.IGNORECASE))
