import re
from client import jasperpath
from subprocess import call

WORDS = ["REMOTE", "START", "BOOT"]

def doRstart():
    call(["sudo", "wakeonlan", "10:BF:48:4C:55:C9"])

def doRstart():
    call(["sudo", "wakeonlan", "10:BF:48:4C:55:C9"])

def handle(text, mic, profile):
    if "REMOTE BOOT" in text.lower():
        mic.say("Booting. Back in a mo.")
        doRstart()
    elif "REMOTE START" in text.lower():
        mic.say("Starting. Back in a mo.")
        doRstart()
    else:
        mic.say("Me no comprenday")

def isValid(text):
    return bool(re.search(r'\b(remote|start|boot)\b', text, re.IGNORECASE))
