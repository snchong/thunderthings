#!/usr/bin/env python3

# This file provides an interface between Thunderbird and Cultured
# Code's Things, by implementing the Mozilla native Messaging
# interface and using Apple Script to tell Things what to do.

# Code is derived from
# https://github.com/mdn/webextensions-examples/blob/master/native-messaging/app/ping_pong.py

import sys
import json
import struct
import subprocess
import urllib.parse



# Python 3.x version
# Read a message from stdin and decode it.
def getMessage(debug=False):
    if debug:
        # just take a string from the stidin
        message = sys.stdin.read()
        print(message)
    else:
        rawLength = sys.stdin.buffer.read(4)
        if len(rawLength) == 0:
            sys.exit(0)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.buffer.read(messageLength).decode('utf-8')

    return json.loads(message)

# Encode a message for transmission,
# given its content.
def encodeMessage(messageContent):
    encodedContent = json.dumps(messageContent).encode('utf-8')
    encodedLength = struct.pack('@I', len(encodedContent))
    return {'length': encodedLength, 'content': encodedContent}

# Send an encoded message to stdout
def sendMessage(encodedMessage):
    sys.stdout.buffer.write(encodedMessage['length'])
    sys.stdout.buffer.write(encodedMessage['content'])
    sys.stdout.buffer.flush()

def createTask(subj, msgId, notes):
    s = '''\
set theURL to "{url}"
set theMessage to "[url=" & theURL & "]Email[/url]"
tell application id "com.culturedcode.ThingsMac"
    show quick entry panel with properties {{name:"{subj}", notes:theMessage & "\n" }}
end tell
'''
    s = s.format(subj=subj, url="mid://"+urllib.parse.quote("<"+str(msgId)+">"))


    process = subprocess.Popen(["osascript"], stdin=subprocess.PIPE)
    process.communicate(s.encode('utf-8'))
        
while True:
    msg = getMessage()
    createTask(msg['subj'], msg['msgId'], msg['notes'])
    
