from urllib2 import Request, urlopen, URLError
import json
from pprint import pprint

key = ''


def get_def(text,key):
    request = Request('https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key='+key+'&lang=en-en&text='+text)
    try:
        response = urlopen(request)
        data = json.load(response)
        word_type = data["def"][0]["pos"]
        defs = data["def"][0]["tr"]
        for text in defs:
            print text["text"]
    except URLError, e:
        print 'Unable to get translation', e

get_def('insect', key)
