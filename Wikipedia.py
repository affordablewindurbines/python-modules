# -*- coding: utf-8-*-
import re
import wikipedia

# Written 

WORDS = ["WIKI", "WIKIPEDIA"]

PRIORITY = 1

def handle(text, mic, profile):

		"""
        	Responds to user-input, typically speech text, by relaying the
        	entry from Wikipedia.

        	Arguments:
        	text -- user-input, typically transcribed speech
        	mic -- used to interact with the user (for both input and output)
        	profile -- contains information related to the user (e.g., phone
                   number)
    	"""

        mic.say("Okay, what would you like me to look up?")

        def sayDefinition(text):
            mic.say(mic.say(wikipedia.summary(text, sentences=2)))

        sayDefinition(mic.activeListen())


def isValid(text):
        return bool(re.search(r'\bwiki|wikipedia\b', text, re.IGNORECASE))
