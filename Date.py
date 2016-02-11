# -*- coding: utf-8-*-
import re
import time

WORDS = ["DATE"]


def handle(text, mic, profile):
    date = time.strftime("%A")
    date = date + ' ' + time.strftime("%B")
    date = date + ' ' + time.strftime("%d")
    date = date + ' ' + time.strftime("%Y")
    mic.say("Todays date is %s " % date)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bdate\b', text, re.IGNORECASE))
