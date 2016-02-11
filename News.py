# -*- coding: utf-8-*-
import re
import feedparser 

WORDS = ["NEWS", "HEADLINES"]

def handle(text, mic, profile):

    if 'INDIA' in text:
        url = 'http://news.google.com/news?pz=1&cf=all&ned=in&hl=en&output=rss'
    elif 'CRICKET' in text:
        url = 'http://www.espncricinfo.com/rss/content/story/feeds/6.xml'
    elif 'TECH' in text:
        url = 'http://www.theregister.co.uk/headlines.atom'
    else:
        url = 'http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&output=rss'

    feed = feedparser.parse(url)
    if not feed:
        mic.say("I'm sorry. I could not get the news for you")
        return

    mic.say("Here is the headline news")
    for post in feed.entries:
        mic.say(post.title)

def isValid(text):
    return bool(re.search(r'\bnews|headlines\b', text, re.IGNORECASE))
