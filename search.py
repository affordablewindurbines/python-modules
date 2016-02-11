__author__ = 'nexhero'
from render.wikia import wikia
from render.wikia import domain
import webbrowser
import re
import wit
import json

WORDS = ["SEARCH"]
PRIORITY = 1

def search_text(_text):
    wit.init()
    result = wit.text_query(_text, 'VAVQDA6WFDRZBY7W62HER5QTDTEHOOR2')
    j = json.loads(result)
    #print j
    #print json.dumps(j, sort_keys=True, indent = 4 ,  separators = (',',': '))
    wit.close()
    return j['outcomes'][0]['entities']


def handle(text, mic, profile):
    query = search_text(text.lower())
    wi = wikia()

    js = wi.wikis(query['wikia_domain'][0]['value'])
    j = wi.top_wikis(j = js)
    domain_wikia =  j['domain']
    d = domain(domain_wikia)
    jd = d.searchList(query=query['wikia_query'][0]['value'])
    url = jd['items'][0]['url']
    webbrowser.open(url)

    #print jd
def isValid(text):
    return bool(re.search(r'\bsearch\b', text, re.IGNORECASE))
