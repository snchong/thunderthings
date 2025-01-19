# thunderthings

Integration between Thunderbird and Cultured Code's Things on macOS.

This Thunderbird add-on provides a mechanism to create a Things to-do that contains a link to an email message. When the link in the to-do is clicked, Thunderbird will open and display the message (requires Thunderbird version 91.8 or later for message links to work on macOS).

ThunderThings consists of two components: a Thunderbird add-on and a macOS application that must be installed on the system and run once (to install some files). The Thunderbird add-on communicates with the app to create to-dos using [Things' Quick Entry](https://culturedcode.com/things/support/articles/2249437/) interface.

Please note that I have no affiliation or connection to Cultured Code other than being a user of their software.


## Installation

You must install two components.

1. ThunderThings add-on. In Thunderbird, go to Tools > Add-ons and Themes and search for "ThunderThings". 

2. ThunderThings macOS application. Download the zip file from https://github.com/snchong/thunderthings/releases/latest and open it. Move the ThunderThings application to the `/Applications` directory on your computer and run it.  
  
    When the application is run, it installs files that allows the Thunderbird add-on to communicate with the ThunderThings app, which is what opens the Things' Quick Entry interface. In more detail, it installs a manifest file as required by [Mozilla's native messaging](https://wiki.mozilla.org/WebExtensions/Native_Messaging) in the directory `~/Library/Application Support/Mozilla/NativeMessagingHosts/` and in the directory `/Library/Application Support/Mozilla/NativeMessagingHosts/`. (Installation in the latter directory is required to get it to work on some machines, as the manifest file in the user directory does not seem to be used.)

    **Note:** Some users have reported that macOS is quarantining `ThunderThings.app`, which prevents the user from running the application. If you encounter this, you will need to clear the quarantine bit by opening the terminal and executing `xattr -c /Applications/ThunderThings.app`, which clears the quarantine bit. If you are concerned about the security of the app, you can download the code from this repo, inspect it (it's pretty straightforward), and build it yourself, by running `make` in the `app` directory.


## Usage

When a message is selected (or window/tab that shows a single message is active), you can activate ThunderThings by 

1. clicking the "Add to Things" button in the toolbar; 
2. selecting "Add to Things" in the context menu; or 
3. pressing ctrl-shift-A.


You can also put link to a message on the clipboard by

1. selecting "Copy as Link" in the context menu; or 
3. pressing alt-command-C.

There are currently no configurable options.


## Feedback or suggestions

Contact thunderthings@gajong.com.