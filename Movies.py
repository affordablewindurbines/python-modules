# -*- coding: utf-8-*-
import re
from imdb import IMDb

WORDS = ["MOVIE", "MOVIES", "YES"]

def format_names(people):
    del people[5:] # Max of 5 people listed
    ret = ''
    for person in people:
        ret += '%s.  ' %person.get('name')
    return ret.strip('. ')

def yes(text):
    return bool(re.search(r'\b(yes)\b', text, re.IGNORECASE))

def isValid(text):
    """
        Returns True if the text is related to Jasper's status.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(movie|movies)\b', text, re.IGNORECASE))

def handle(text, mic, profile):
    mic.say('What movie?')
    movie_name = mic.activeListen()
    mic.say('Searching top five results for.  %s' %movie_name)
    ia = IMDb()
    movie_query = ia.search_movie(movie_name)
    del movie_query[5:]
    for movie in movie_query:
        mic.say('Did you mean %s (%s)?' %(movie.get('title'), movie.get('year')))
        response = mic.activeListen()
        if yes(response):
            ia.update(movie)
            movie_info = '%s (%s).  ' %(movie.get('title'), movie.get('year'))
            if movie.get('rating'): movie_info += 'Rating.  %s out of 10.  ' %movie.get('rating')
            if movie.get('runtimes'): movie_info += 'Runtime.  %s minutes.  ' %movie.get('runtimes')[0]
            if movie.get('genres'): movie_info += 'Genres.  %s.  ' %'.  '.join(movie.get('genres'))
            if movie.get('plot outline'): movie_info += 'Plot.  %s  ' %movie.get('plot outline')
            if movie.get('director'): movie_info += 'Directors.  %s.  ' %format_names(movie.get('director'))
            if movie.get('producer'): movie_info += 'Producers.  %s.  ' %format_names(movie.get('producer'))
            if movie.get('cast'): movie_info += 'Cast.  %s.  ' %format_names(movie.get('cast'))
            mic.say(movie_info)
            return
    mic.say('Unable to find information on the requested movie')
