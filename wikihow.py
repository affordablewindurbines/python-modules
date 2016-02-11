from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup
import urllib2
import gtk
import webkit


class renderWikihow():
    def __init__(self, ):
        self.url = ''

    def getContent(self, url=''):
        url = url.replace(" ", "-")

        page = urllib2.urlopen(url)

        soup = BeautifulSoup(page.read())
        edits = soup.findAll(attrs={"class": "editsection"})
        for e in edits:
            e.clear()
        edits = soup.findAll(attrs={"class": "ad_label"})
        for e in edits:
            e.clear()
        edits = soup.findAll(attrs={"class": "step_num"})
        for e in edits:
            e.clear()


        images = soup.findAll("a")
        for a in images:
            a['class'] = 'thumbnail'

        igre = soup.find(id = "ingredients")
        arts = soup.findAll(attrs={"class":"steps"})
        data = {"ingr" : igre , "steps" : arts}
        return data

    def renderContent(self, content = []):
        head = """<html>
                    <head>
                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
                            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
                        <title>Hello</title>
                    </head>
                    <body>"""

        footer = """</body>
                </html>
                """

        body = ''
        if content.has_key("ingr"):
            body = body + str(content["ingr"])
        if content.has_key("steps"):
           #body = body + str(content["steps"])
            for c in content["steps"]:
                body = body + str(c)


        page = head + str(body)+ footer

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(320, 240)
        window.maximize()
        window.connect("destroy", lambda w: gtk.main_quit())
        scroll = gtk.ScrolledWindow()
        web = webkit.WebView()
        window.add(scroll)
        scroll.add(web)
        web.load_string(page, 'text/html', 'UTF-8','/')
        window.show_all()
        gtk.main()
