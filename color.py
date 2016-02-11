# -*- coding: utf-8-*-
import re
import subprocess

WORDS = ["GREEN", "BLUE", "RED"]

def handle(text, mic, profile):

    if "red" in text.lower():
        mic.say("OK! I will set the led to red!")
        subprocess.call("/home/pi/curl/led.sh RED", shell=True)

    elif "green" in text.lower():
        mic.say("OK! I will set the led to green!")
        subprocess.call("/home/pi/curl/led.sh GREEN", shell=True)

    elif "blue" in text.lower():
        mic.say("OK! I will set the led to blue!")
        subprocess.call("/home/pi/curl/led.sh BLUE", shell=True)

def isValid(text):
    return bool(re.search(r'\bgreen|blue|red\b', text, re.IGNORECASE)
