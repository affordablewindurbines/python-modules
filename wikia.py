__author__ = 'nexhero'
import urllib2
import json
API_V1 = "http://www.wikia.com/api/v1/"
class wikia:
    def __init__(self):
        def_ = "something"

    def wikis(self, query):
        url = API_V1 + "Wikis/ByString?expand=1&string="+ query +"&limit=25&batch=1&includeDomain=true&lang=en"
        res = urllib2.urlopen(url)
        j = res.read()

        j = json.loads(j)
        return j
#        print json.dumps(j, sort_keys=True, indent=4)
    def top_wikis(self, j=[]):
        flag = 0
        f_key = 0
        for key in j['items']:
            if key['wam_score'] > flag:
                f_key = key
                flag = key['wam_score']
        return f_key

class domain:
    def __init__(self, domain_url):
        self.url = "http://"+domain_url + "/api/v1/"


    def searchList(self, query):
        url = self.url + "Search/List?query=" + query +"&limit=1&minArticleQuality=10&batch=1&namespaces=0%2C14"
        print url
        res = urllib2.urlopen(url)
        j = res.read()
        j = json.loads(j)
        return j
