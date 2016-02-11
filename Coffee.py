# -*- coding: utf-8-*-
import re
import subprocess
import requests

WORDS = ["COFFEE"]


def handle(text, mic, profile):

    #subprocess.call("/home/pi/routines/runShell")
    requests.post('https://api.spark.io/v1/devices/[YOUR DEVICE ID]/brew?access_token=[YOUR ACCESS TOKEN]')

    mic.say("OK. Now Brewing.")


def isValid(text):
    """
        Returns True if input is related to the coffee.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bcoffee\b', text, re.IGNORECASE))
