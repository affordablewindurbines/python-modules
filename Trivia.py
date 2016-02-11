import re
import json
import urllib2
from urllib import urlopen

WORDS           = ["TRIVIA"]
JSON_URL        = "http://jservice.io/api/random"

def handle(text, mic, profile):

        mic.say("Let's find you a question.")

        jsonurl = urlopen(JSON_URL)

        try:
                infos = json.loads(jsonurl.read())
        except ValueError, e:
                pass
                mic.say("Hmm, there are no trivia available now. Please try again.")
        else:
                pass
                def remove_tags(text):
                        return re.sub('<[^<]+?>', '', text)

                category        = infos[0]["category"]["title"]
                question        = infos[0]["question"]
                answer          = remove_tags(infos[0]["answer"])

                def checkAnswer(text):
                        if text == answer:
                                mic.say("You are correct. It is " + answer + ".")
                        else:
                                mic.say("You are incorrect. It is " + answer + ".")

				mic.say(profile["first_name"] + ".")
                mic.say("The category is " + category + ".")
                mic.say(question)
                checkAnswer(mic.activeListen())

def isValid(text):
        return bool(re.search(r'\btrivia\b', text, re.IGNORECASE))
