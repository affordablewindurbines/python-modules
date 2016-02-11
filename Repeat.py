# -*- coding: utf-8-*-
import re

WORDS = ["REPEAT", "AFTER", "ME"]


def handle(text, mic, profile):
    mic.say('OK')

    text = mic.activeListen()
  
    mic.say(text)


def isValid(text):
    return bool(re.search(r'\brepeat after me\b', text, re.IGNORECASE))
