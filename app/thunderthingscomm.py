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

def createTask(d):
    str = ""
    for k in d:
        if str:
            str += ","
        str = str + k + ":\""+d[k]+"\""
        
    s = '''\
tell application id "com.culturedcode.ThingsMac"
    show quick entry panel with properties {{ {propmap} }}
end tell
'''
    s = s.format(propmap = str)

    process = subprocess.Popen(["osascript"], stdin=subprocess.PIPE)
    process.communicate(s.encode('utf-8'))

def run():
    while True:
        createTask(getMessage())
    
if __name__ == '__main__':
    run()