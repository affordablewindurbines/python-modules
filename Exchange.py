# -*- coding: utf-8-*-
import re
import json
import urllib2
from urllib import urlopen

WORDS = ["CURRENCY", "EXCHANGE"]
API_URL = "http://rate-exchange.appspot.com/currency?"
FIRST_CURR = ""
FIRST_CURR_ACTUAL = ""
SECOND_CURR = ""
SECOND_CURR_ACTUAL = ""

def handle(text, mic, profile):
    def setFirstCurrency(text):
        global FIRST_CURR_ACTUAL
        FIRST_CURR_ACTUAL = text


    def setSecondCurrency(text):
        global SECOND_CURR_ACTUAL
        SECOND_CURR_ACTUAL = text


    def convertToCode():
        global FIRST_CURR
        global FIRST_CURR_ACTUAL
        global SECOND_CURR
        global SECOND_CURR_ACTUAL
        code_list = {"YEN" : "JPY", "DOLLARS" : "USD"}

        for key, value in code_list.iteritems():
                if key == FIRST_CURR_ACTUAL:
                        FIRST_CURR = value
                    if key == SECOND_CURR_ACTUAL:
                        SECOND_CURR = value

        if FIRST_CURR != "" and SECOND_CURR != "":
            return True
        else:
            return False


    mic.say("First currency?")
    setFirstCurrency(mic.activeListen())

    mic.say("Second currency?")
    setSecondCurrency(mic.activeListen())

    if convertToCode():
        mic.say("Getting exchange rate of " + FIRST_CURR_ACTUAL + " against " + SECOND_CURR_ACTUAL + ".")
        jsonurl = urlopen(API_URL + "from=" + FIRST_CURR + "&to=" + SECOND_CURR)

        try:
            rate = json.loads(jsonurl.read())
        except ValueError, e:
            pass # invalid json
            mic.say("An error occured. Maybe the API is offline?")
        else:
            pass # valid json
            mic.say("Okay, here is the exchange rate.")
            mic.say("It is approximately " + str(round(rate["rate"], -1)) + " " + SECOND_CURR_ACTUAL + " for 1 " + FIRST_CURR_ACTUAL + ".")
    else:
        mic.say("One or both currencies are not understood. Please try again.")

def isValid(text):
    return bool(re.search(r'\bcurrency|exchange\b', text, re.IGNORECASE))
