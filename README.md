#TF2Idle
TF2Idle is a convenient GUI interface for idling in [Team Fortress 2](http://www.teamfortress.com). It does **not** modify game files or circumvent TF2. You will still need to run a TF2 instance for each copy of TF2 you wish to idle on.

#Version history
## Version 1.1.0
* Added option to add delay between account launches
* Added option to modify drop log output file formatting
* Tweaked update gcf icon
* Added progress icons for gcf updating
* Fixed bug with changing multiple account sandbox names

## Version 1.0.0
* Initial Release

#Compiled exe
Download the exe from the [downloads section](http://github.com/Moussekateer/TF2IdleGUI/downloads).

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
You can sign up for your own Steam API key from [here](http://steamcommunity.com/dev). Please read through the terms and conditions before you do so.
    
#Idling

Quick tl;dr on how to idle.

## Requirements
* [Sandboxie](http://sandboxie.com)
* The ability to read

## Folder structure

You'll want a seperate Steam installation for each of your idle accounts (they'll share a single steamapps folder, so don't worry about disk space), you can do it with a single secondary Steam install - however some users may face errors doing this.  Never use your main Steam install, else you risk corrupting your game files.

* Copy the Steam folder (minus the steamapps folder) to somewhere else on the hard disk.
* Create a folder inside the Steam folder for each account you have.
* Copy the steamapps folder somewhere (Do not use your main Steam installation's steamapps folder). You can delete all the non-TF2 related gcfs from this folder.
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

* Run TF2Idle.py
* Select 'Update GCFs' to copy the TF2 GCFs from your main Steamapps folder, to your secondary Steamapps folder
* Select 'Empty sandbox' to delete any contents in each sandbox, this prevents errors.
* Start Steam.exe from the secondary directory **unsandboxed** to make sure the GCFs are completely updated.
* You are now ready to idle.