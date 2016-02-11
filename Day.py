# -*- coding: utf-8-*-
import re
import time

WORDS = ["DAY"]


def handle(text, mic, profile):
    day = time.strftime("%A")
    mic.say("Today is %s " % day)


def isValid(text):
    return bool(re.search(r'\bday\b', text, re.IGNORECASE))
