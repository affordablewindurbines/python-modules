# -*- coding: utf-8-*-
import re
import psutil
import platform
import datetime

WORDS = ["STATUS"]

def isValid(text):
    """
        Returns True if the text is related to Jasper's status.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(status)\b', text, re.IGNORECASE))

def handle(text, mic, profile):
    os, name, version, _, _, _ = platform.uname()
    version = version.split('-')[0]
    cores = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory()[2]
    disk_percent = psutil.disk_usage('/')[3]
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    running_since = boot_time.strftime("%A %d. %B %Y")
    response = "I am currently running on %s version %s.  " %(os, version)
    response += "This system is named %s and has %s CPU cores.  " %(name, cores)
    response += "Current CPU utilization is %s percent.  " %cpu_percent
    response += "Current memory utilization is %s percent." %memory_percent
    mic.say(response)
