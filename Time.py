import datetime
import re
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["TIME"]


def handle(text, mic, profile):

    tz = getTimezone(profile)
    now = datetime.datetime.now(tz=tz)
    service = DateService()
    response = service.convertTime(now)
    mic.say("It is %s right now." % response)


def isValid(text):
    return bool(re.search(r'\btime\b', text, re.IGNORECASE))
