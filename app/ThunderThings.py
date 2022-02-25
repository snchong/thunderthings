#!/usr/bin/env python3


import os
import sys
from os.path import expanduser
import thunderthingscomm

launched_from_app = (os.getenv('APPLAUNCHED') == "Y")

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
        if os.access(filename, os.W_OK):
            f = open(filename, "w")
            f.write(str)
            f.close()
            return True
        elif os.path.exists(filename) and os.access(filename, os.R_OK):
            # We can't write to the file
            # but we can read, so lets see if the file is correct
            f = open(filename, "r")
            contents = f.read()
            f.close()
            return contents == str
            
        else:
            return False

    userfile = expanduser("~")+"/Library/Application Support/Mozilla/NativeMessagingHosts/thunderthings.json"
    sysfile = "/Library/Application Support/Mozilla/NativeMessagingHosts/thunderthings.json"
    if not writeToFile(userfile, js):
        message("Could not write to file " + userfile +". Unable to install.")
        sys.exit(1)
    if not writeToFile(sysfile, js):
        message("""\
Installed the user file but could not install the system file to allow \
the ThunderThings add-on to communicate with Things.


If ThunderThings does not work, you should open the Terminal application and \
run \"sudo {apploc} --install\" to install the system file.
""".format(apploc=loc))
        sys.exit(1)
    
    message("Successfully installed files to allow the ThunderThings add-on to communicate with Things! " +
            "You do not need to run this application again, but it does need to be present on your system " +
            "for ThunderThings to work.")
    sys.exit(0)


def message(msg, gui=None):
    if gui or (gui is None and launched_from_app):
        asc =  "osascript -e 'display dialog \"{msg}\" buttons \"OK\" with title \"ThunderThings\"'"
        msg = msg.replace('"', '\\"').replace("\n", "\\n")
        os.system(asc.format(msg=msg))
    else:
        print(msg)

           

# If we are launched from the app or given the command line arg "--install"
# then try to install the files
if launched_from_app or (sys.argv and "--install" in sys.argv):
    installFiles()
    sys.exit()



# Otherwise, run the native messaging communication protocol
thunderthingscomm.run()
