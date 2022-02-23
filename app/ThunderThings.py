#!/usr/bin/env python3


import os
from os.path import expanduser
import thunderthingscomm

def installFiles():
    # Get this file's location
    loc = os.path.realpath(__file__)

    # JSON string

    js = """{{
    "name": "thunderthings",
    "description": "Script to provide a native messaging interface with Things",
    "path": "{commloc}",
    "type": "stdio",
    "allowed_extensions": [ "thunderthings@gajong.com" ]
}}"""
    
    js = js.format(commloc=loc)

    def writeToFile(filename, str):
        f = open(filename, "w")
        f.write(str)
        f.close()

    writeToFile(expanduser("~")+"/Library/Application Support/Mozilla/NativeMessagingHosts/thunderthings.json", js)
    writeToFile("/Library/Application Support/Mozilla/NativeMessagingHosts/thunderthings.json", js)


def message(msg):
    asc =  "osascript -e 'Tell application \"System Events\" to display dialog \"{msg}\" buttons \"OK\" with title \"ThunderThings\"'"
    os.system(asc.format(msg=msg))

           
launched_from_app = (os.getenv('APPLAUNCHED') == "Y")

if launched_from_app:
    installFiles()
    # XXX confirmation message
    message("Installed")
    exit()

# XXX if files not installed, try to install them.


thunderthingscomm.run()
    