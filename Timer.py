# -*- coding: utf-8-*-
import re
import os

WORDS = ["TIMER"]

def handle(text, mic, profile):

    if 'SET' in text and 'FOR' in text:
        
        lst = text.split()
            
        duration = lst[len(lst)-2]
        duration = duration + ' ' + lst[len(lst)-1]
        
        cmd = '/usr/bin/at '
        cmd = cmd + '"now + '+duration+'" '
        cmd = cmd + '-f /home/pi/jasper/client/modules/timer.sh'

        ret = os.system(cmd);

        if ret == 0:
            mic.say('OK. I have set a timer for '+duration)
        else:
            mic.say("I couldn't set a timer. Please try again")
 
        
def isValid(text):
    return bool(re.search(r'\btimer\b', text, re.IGNORECASE))
