# -*- coding: utf-8-*-
import re
from PyDictionary import PyDictionary

WORDS = ["DEFINE","DEFINITION"]

def handle(text, mic, profile):

    lst = text.split()

    text = lst[len(lst)-1]
    if(text):
        dictionary=PyDictionary() 
        mean = dictionary.meaning(text)
        if not mean:
            mic.say("I'm sorry I couldn't find the meaning of the word "+text)
            return
        mic.say(text)
        for keys in mean:
            mic.say(keys)
            lst = mean[keys]
            for l in lst:
                mic.say(l)

def isValid(text):
    return bool(re.search(r'\bdefine|definition\b', text, re.IGNORECASE))
