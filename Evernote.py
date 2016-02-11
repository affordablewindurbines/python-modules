# coding=utf-8
import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

import sys
import time
import re

# Written by Jason van Eunen - jasonvaneunen.com


WORDS = ["NOTE"]

PRIORITY = 1


def handle(text, mic, profile):

        auth_token = profile["EVERNOTE_TOKEN"]

        client = EvernoteClient(token=auth_token, sandbox=False)
        user_store = client.get_user_store()
        note_store = client.get_note_store()

        if bool(re.search(r'\Note\b', text, re.IGNORECASE)):
                writeNote(text, mic, note_store)

def writeNote(text, mic, note_store):
        note = Types.Note()						# Creates a new note
        note.title = "Jasper Note"

        mic.say("What would you like me to write down?")
        theNote = mic.activeListen()					# Listens to the input and stores it

        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM ' \
    '"http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>Note:<br/>'
        note.content += ('%s' % theNote)
        note.content += '</en-note>'

        created_note = note_store.createNote(note)			# Stores the new note in Evernote
        mic.say("I successfully wrote down your note.")

def isValid(text):
        return bool(re.search(r'\Note\b', text, re.IGNORECASE))
