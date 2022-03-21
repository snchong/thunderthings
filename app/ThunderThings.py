#!/usr/bin/env python3


import os
import sys
import traceback
from os.path import expanduser
import thunderthingscomm

launched_from_app = (os.getenv('APPLAUNCHED') == "Y")



# Some useful messages
install_success_msg = """\
We successfully installed files to allow the ThunderThings add-on to communicate with Things! 

You do not need to run this application again, but it does need to be present on your system \
for ThunderThings to work.\
"""

already_install_msg = """\
We have already installed files to allow the ThunderThings add-on to communicate with Things! 

You do not need to run this application again, but it does need to be present on your system \
for ThunderThings to work.\
"""

install_user_not_sys_msg = """\
We successfuly installed the user file but could not install the system file to allow \
the ThunderThings add-on to communicate with Things.


If ThunderThings does not work, you should open the Terminal application and \
run \"sudo {apploc} --install\" to install the system file.
"""

about_to_escalate_msg = """\
We will try to install the system-level file to allow \
the ThunderThings add-on to communicate with Things. Please approve \
the administrator privilege request that will appear soon.
"""



def installFiles():
    # Get this file's location
    loc = os.path.realpath(__file__)
    loc = loc.replace("/Resources/ThunderThings.py", "/MacOS/Thunderthings")

    # JSON string

    js = """{{
    "name": "thunderthings",
    "description": "Script to provide a native messaging interface with Things",
    "path": "{commloc}",
    "type": "stdio",
    "allowed_extensions": [ "thunderthings@gajong.com" ]
}}"""
    
    js = js.format(commloc=loc)

    def checkFile(dir, filename, str):
        try:
            filename = dir+filename
            if os.path.exists(filename):
                # File exists, see if it is correct
                f = open(filename, "r")
                contents = f.read()
                f.close()
                if contents == str:
                    # No need to change anything
                    return True
        except PermissionError:
            pass
        return False
    
    def writeToFile(dir, filename, str):
        try:
            os.makedirs(dir, exist_ok=True)
            f = open(dir+filename, "w+")
            f.write(str)
            f.close()
            return True
        except PermissionError:
            # failed to open to write
            pass
        return False

        
        

    userdir = expanduser("~")+"/Library/Application Support/Mozilla/NativeMessagingHosts/"
    sysdir = "/Library/Application Support/Mozilla/NativeMessagingHosts/"
    filename = "thunderthings.json"


    if checkFile(userdir, filename, js) and checkFile(sysdir, filename, js):
        message(already_install_msg)
        sys.exit(0)
        
    if not writeToFile(userdir, filename, js):
        message("Could not write to file " + userfile +". Unable to install.")
        sys.exit(1)
        
    if writeToFile(sysdir, filename, js):
        if not (sys.argv and "--sudo" in sys.argv):
            message(install_success_msg)
        sys.exit(0)

    # we didn't write the sysfile
    if sys.argv and "--sudo" in sys.argv:
        # We already tried to escalate privileges
        # fail, no need to print error message
        sys.exit(1)
            
    # Try to escalate privileges
    message(about_to_escalate_msg)        
    asc =  "osascript -e 'do shell script \"{apploc} --install --sudo\" with administrator privileges'"
    res = os.system(asc.format(apploc=loc))
    if res == 0:
        # Success!
        message(install_success_msg)
        sys.exit(0)
            
    message(install_user_not_sys_msg.format(apploc=loc))
    sys.exit(1)


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
    try:
        installFiles()
    except Exception as e:
        message("Encountered the following error when executing. "+
                "For help, please copy this message and email to thunderthings@gajong.com.\n\n"+
                traceback.format_exc())

    sys.exit()



# Otherwise, run the native messaging communication protocol
thunderthingscomm.run()
