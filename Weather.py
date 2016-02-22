# -*- coding: utf-8-*-
import re
import datetime
import struct
import urllib
import feedparser
import requests
import logging
import bs4
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["WEATHER", "CURRENT", "TODAY", "TONIGHT", "TOMORROW", "FORECAST"]


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def replaceAcronyms(text):
    """
    Replaces some commonly-used acronyms for an improved verbal weather report.
    """

    def parseDirections(text):
        words = {
            'N': 'north',
            'S': 'south',
            'E': 'east',
            'W': 'west',
        }
        output = [words[w] for w in list(text)]
        return ' '.join(output)
    acronyms = re.findall(r'\b([NESW]+)\b', text)

    for w in acronyms:
        text = text.replace(w, parseDirections(w))

    text = re.sub(r'(\b\d+)F(\b)', '\g<1> Fahrenheit\g<2>', text)
    text = re.sub(r'(\b)mph(\b)', '\g<1>miles per hour\g<2>', text)
    text = re.sub(r'(\b)in\.', '\g<1>inches', text)

    return text


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

def get_locations():
    r = requests.get('http://www.wunderground.com/about/faq/' +
                     'international_cities.asp')
    soup = bs4.BeautifulSoup(r.text)
    data = soup.find(id="inner-content").find('pre').string
    # Data Stucture:
    #  00 25 location
    #  01  1
    #  02  2 region
    #  03  1
    #  04  2 country
    #  05  2
    #  06  4 ID
    #  07  5
    #  08  7 latitude
    #  09  1
    #  10  7 logitude
    #  11  1
    #  12  5 elevation
    #  13  5 wmo_id
    s = struct.Struct("25s1s2s1s2s2s4s5s7s1s7s1s5s5s")
    for line in data.splitlines()[3:]:
        row = s.unpack_from(line)
        info = {'name': row[0].strip(),
                'region': row[2].strip(),
                'country': row[4].strip(),
                'latitude': float(row[8].strip()),
                'logitude': float(row[10].strip()),
                'elevation': int(row[12].strip()),
                'id': row[6].strip(),
                'wmo_id': row[13].strip()}
        yield info


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def get_forecast_by_name(location_name):
    entries = feedparser.parse("http://rss.wunderground.com/auto/rss_full/%s"
                               % urllib.quote(location_name))['entries']
    if entries:
        # We found weather data the easy way
        return entries
    else:
        # We try to get weather data via the list of stations
        for location in get_locations():
            if location['name'] == location_name:
                return get_forecast_by_wmo_id(location['wmo_id'])


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def get_forecast_by_wmo_id(wmo_id):
    return feedparser.parse("http://rss.wunderground.com/auto/" +
                            "rss_full/global/stations/%s.xml"
                            % wmo_id)['entries']


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def handle(text, mic, profile):
    """
    Responds to user-input, typically speech text, with a summary of
    the relevant weather for the requested date (typically, weather
    information will not be available for days beyond tomorrow).

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    logger = logging.getLogger(__name__)
    logger.debug(text)
    logger.debug("location=" + str(profile['location']))
    forecast = None
    if 'location' in profile:
        forecast = get_forecast_by_name(str(profile['location']))

    if not forecast:
        mic.say("I'm sorry, I can't seem to access weather information right now.")
        # mic.say("Please make sure that you've set your location on the dashboard.")
        return

    # tz = getTimezone(profile)
    # logger.debug(tz)

    date_keyword = 'all'
    for word in text.split():
        logger.debug('word='+word)
        if word != "WEATHER" and word in WORDS:
            date_keyword = word.lower()

    matchThese = []
    tz = getTimezone(profile)
    service = DateService(tz=tz)
    today_wkday = datetime.datetime.now(tz=tz).weekday()
    today = service.__daysOfWeek__[today_wkday]
    if date_keyword == 'tomorrow':
        tomorrow_wkday = (today_wkday + 1) % 7
        date_keyword  = service.__daysOfWeek__[tomorrow_wkday]
    
    logger.debug("date_keyword=" + date_keyword)

    if date_keyword != '':
        matchThese.append(date_keyword)

    if date_keyword == 'today':
        matchThese.append('current')
        matchThese.append('rest')
        matchThese.append('this')
        # matchThese.append('tonight')
    
    for entry in matchThese:
        logger.debug('match=' + entry)

    for entry in forecast:
        date_desc = entry['title'].split()[0].strip().lower()
        logger.debug('[' + date_desc + ']: title=' + str(entry['title']))

    # logger.debug(forecast)
    for entry in forecast:
        sayThis = ''
        date_desc = entry['title'].split()[0].strip().lower()
        if (date_desc in matchThese) or (date_keyword == 'all'):
            if date_desc == 'current':
                sayThis = str(entry['title'])
            else:
                sayThis = str(entry['summary'])

        if sayThis != '':
            mic.say(sayThis)
    return


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    logger = logging.getLogger(__name__)
    logger.debug('text=' + text)
    for word in text.split():
        word = word.upper()
        # logger.debug(word)
        if word in WORDS:
            return True
    return False
