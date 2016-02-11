# -*- coding: utf-8-*-
import re
import json
import wit

from simplemediawiki import MediaWiki
from fuzzywuzzy import fuzz
import webbrowser
import client.modules.render.wikihow as renderWH

WORDS = ["HOW TO"]

def getRequest(_text):
    wit.init()
    result = wit.text_query(_text.lower(), 'VAVQDA6WFDRZBY7W62HER5QTDTEHOOR2')
    j = json.loads(result)
    data = j['outcomes'][0]['entities']['how_to_text'][0]
    wit.close()
#check if exist the value
    if data.has_key('value'):
        return data['value']
    else:
        return None

def handle(text, mic, profile):
    baseurl= "http://www.wikihow.com/"
    wiki = MediaWiki('http://www.wikihow.com/api.php')
    #wiki.login("inexhero@gmail.com", "david1234")
    params = {'action':'query','list':'search','srsearch':text,'srprop':'redirecttitle','limit':'1', 'format':'json'}

    response = wiki.call(params)
    #r = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

    flag = 0
    flag_title = "none"
    pos= response['query']['search']
    query = getRequest(text)
    wiki.logout()
#Getting the article with the best score
    for key in pos:
        val = fuzz.ratio(key['title'],query)
        print(str(val) + "% " + key['title'])
        if val > flag:
            flag = val
            flag_title = key['title']
    if flag !=0:
        answer = flag_title
        mic.say(answer)

        #rWH = renderWH.renderWikihow()
        #url = baseurl + answer
        #print url
        #url_ = rWH.getContent(str(url))
        #rWH.renderContent(url_)
        webbrowser.open(baseurl + flag_title)
    else:
        mic.say("I could not find anything bro!")

def isValid(text):
    return bool(re.search(r'\bhow to\b', text, re.IGNORECASE))
