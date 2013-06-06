#TF2Idle
TF2Idle is a convenient GUI interface for idling in [Team Fortress 2](http://www.teamfortress.com). It does **not** modify game files or circumvent TF2. You will still need to run a TF2 instance for each copy of TF2 you wish to idle on.

#Links
* [Uservoice forum for feedback, bug reports, and feature requests](https://tf2idle.uservoice.com)
* [Reddit post](http://www.reddit.com/r/tf2/comments/pdtwe/tf2idle_an_easier_way_to_idle/)
* [Facepunch thread](http://www.facepunch.com/threads/1250564)

#Version history
## Version 1.9.6
* Add setting for enabling and disabling low priority Steam process launching
* Update 'Copy GCFs' functionality to copy over Team Fortress 2 folder since SteamPipe move.
* Rewrite drop log backpack threads. All accounts now share a common schema that updates every 12 hours, making adding new accounts to log MUCH quicker and more memory efficient.

## Version 1.9.5
* Add item values to items in drop log using the [backpack.tf IGetPrices API](http://backpack.tf/api)
* Steam and TF2 now starts in low priority mode
* Improved identification of dropped items
* Save account and program settings to config file on every change rather than just on program exit
* Added setting for auto-logging idled accounts
* Fixed some wording on dialogs
* Only show crate series on normal crates
* Fix bug with window size not being saved if close to tray is enabled

## Version 1.9.3
* Better Steam API failure handling
* Completely remove lag on adding multiple accounts to drop log
* Increase max number of account box columns to 20
* Better flexible resizing for account boxes so that more can fit on screen
* Add link to uservoice forum for bug reports, feature requests or feedback in about menu
* Fixed bug with accounts that have spaces in the password
* Fixed bug with multiple values being set with steam install path or groups in accounts view

## Version 1.9.0
* Added new aggregate view for drop log
* Added links to backpack and wiki links for items in drop log viewer
* Added sortable columns in drop log
* Automatically start logging accounts when idled
* Added web viewer port settings
* Added option to use account group to deselect accounts
* Added new icons in menus
* Added setting to change program behaviour to minimize to tray on close
* Fix small bug with web viewer port

## Version 1.6.0
* Added web viewer for drop log on port 5000. Port forwarding will need to be set up for external networks
* Added system tray pop up notifications
* Fixed bug with Sandboxie easy mode pointing to wrong directory for Steam.exe
* Better error logging

## Version 1.5.3
* Fixed program not remembering being maximised on launch
* Fix bug with drop log missing items. It will now log all items dropped between polls

## Version 1.5.1
* Fixed bug with drop log where drop log would fail on finding craft_items
* Added backpack.tf as a backpack viewer
* Changed default backpack viewer to Steam

## Version 1.5.0
* Changed copy gcfs function to instead open dialog after process has finished instead of before
* Added dialog check on app quit
* Added facepunch thread link
* Added scrolling for group selection dialog
* Fixed bug with accounts remaining selected after group selections
* Updated TF2B backpack link
* Fixed issue with using special characters in passwords/usernames/any config file option

## Version 1.3.0
* Added option to launch any program sandboxed for each account
* Added option to define per account launch parameters
* Increased max account delay to 10 minutes
* Drop log now shows crate series
* Removed restriction on what filetype logs can be saved as
* Added alphabetical ordering in groups dialog
* Fixed bug with account launch delay where some accounts would fail to launch
* Fixed Sandboxie errors when deleting the contents of too many sandboxes at once

## Version 1.1.1
* Fixed bug with saving drops to log file
* Changed an icon

## Version 1.1.0
* Added option to add delay between account launches
* Added option to modify drop log output file formatting
* Tweaked update gcf icon
* Added progress icons for gcf updating
* Fixed bug with changing multiple account sandbox names

## Version 1.0.0
* Initial Release

#Compiled exe
## Download the exe from [here](http://code.google.com/p/tf2idle/downloads/list) (formerly the [downloads section](http://github.com/Moussekateer/TF2IdleGUI/downloads)).

## If you wish to compile the program yourself you will need to do the following.
* Download and install the following dependancies: PyQt4, PyCrypto.
* Install [PyInstaller](http://www.pyinstaller.org)
* Clone the repo into a folder somewhere.
* cd into the PyInstaller folder and run 'python pyinstaller.py /path/to/repo/folder/TF2Idle.spec'
* PyInstaller will build the exe and output it in the path/to/pyinstaller/directory/TF2Idle/dist

#Script
## Requirements
* [Python 2.7](http://www.python.org/getit/releases/2.7/) -- Install the 32 bit version (x86)

You will also need to install the following modules.

* [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download) -- Install the 32 bit version (x86)
* [PyCrypto](https://www.dlitz.net/software/pycrypto) -- For config file encryption

##Usage
Run from commandline

    python TF2Idle.py

#API key
You can sign up for your own Steam API key [here](http://steamcommunity.com/dev). Please read through the terms and conditions before you do so.
    
#Idling

Quick tl;dr on how to idle.

## Requirements
* [Sandboxie](http://sandboxie.com)
* The ability to read

## Folder structure

You'll want a seperate Steam installation for each of your idle accounts (they'll share a single steamapps folder, so don't worry about disk space), you can do it with a single secondary Steam install - however some users may face errors doing this.  Never use your main Steam install, else you risk corrupting your game files.

* Copy the Steam folder (minus the steamapps folder) to somewhere else on the hard disk.
* Create a folder inside the Steam folder for each account you have.
* Copy the steamapps folder somewhere (Do not use your main Steam installation's steamapps folder). You can delete all gcfs, gamefolders, and information for games unrelated to TF2.
* Open cmd.exe as an administrator, and for each idle account enter (using my directories as an example): `mklink /d "G:/Sandboxie/Steam/Account1/Steamapps" "G:/Sandboxie/Steam/Steamapps"` where the first parameter is the idle account's Steam install, followed by `/Steamapps`, and the second parameter is your secondary steamapps folder (Again, not your main Steam installations steamapps).

You should now have a folder structure similar to:

```
G:\Sandboxie\Steam:
    Account1
        ...
        Steamapps
        ...
    Account2
        ...
        Steamapps
        ...
    Account3
        ...
        Steamapps
        ...
    Steamapps
```

* This tricks programs into thinking the steamapps folder is present in each of those account folders.

## Sandboxie

The free version of Sandboxie limits you to one sandbox, meaning you can only run two instances of Steam at any one time (one unsandboxed and one sandboxed). To create more sandboxes you will require a license.

Create a sandbox for each of your folders, with whatever name you want to give them - I name mine the same as my folder names (so just Account1, Account2, Account3...).

For each sandbox right click on it and go to sandbox settings. You'll want to set the settings as follows:

* `Restrictions` -> `Drop Rights` -> Untick `Drop rights from Administrators and Power Users groups`
* `Resource Access` -> `File Access` -> `Full Access` -> Add your idle accounts Steam folder, and your steamapps folder.
  * e.g. `G:\Sandboxie\Steam\Account1`
  * `G:\Sandboxie\Steam\Steamapps`

## First launch / what to do after every TF2 update

* Run TF2Idle
* Select 'Update TF2 folder' to copy the TF2 game resources from your main Steamapps folder to your secondary Steamapps folder
* Select 'Empty sandbox' to delete any contents in each sandbox; this prevents errors.
* Start Steam.exe from the secondary directory **unsandboxed** to make sure the VDFs are completely updated.
* You are now ready to idle.