#!/usr/bin/env python2.7

import os
import sys
import shutil
import logging
import re
import psutil
import platform
import datetime
import yaml
import argparse
import dbus,jasper
bus = dbus.SessionBus()

proxy = False

def feat(s):
    s = s.replace(" feat "," featuring ")
    s = s.replace(" ft. "," featuring ")
    s = s.replace(" feat. "," featuring ")
    s = s.replace(" ft "," featuring ")
    return s

if bus.name_has_owner('org.gnome.Rhythmbox3'):
    proxy = bus.get_object('org.gnome.Rhythmbox3','/org/mpris/MediaPlayer2')
elif bus.name_has_owner('org.bansheeproject.Banshee'):
    proxy = bus.get_object('org.bansheeproject.Banshee','/org/mpris/MediaPlayer2')
if proxy != False:
    properties_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
    metadata = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
    state = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
    album = ""
    title = ""
    artist = ""
    cover = ""
    for each in metadata:
        if each == "xesam:album":
            album = metadata[each]
        elif each == "xesam:artist":
            artist = metadata[each][0]
        elif each == "xesam:title":
            title = metadata[each]
        elif each == "mpris:artUrl":
            cover = metadata[each]
    lispeak.displayNotification({"title":title,"message":"Artist: "+artist+"\\nAlbum: "+album,"icon":cover,"speech":feat(title)+" by "+feat(artist)})
else:
    jasper.displayNotification("Nothing Playing")
