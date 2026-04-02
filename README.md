# steam-icons-fix

This script allows you to fix blank icons on your Desktop when reinstalling steam.

## How to run
* Install python
* Install requests (pip install requests)
* Run steam-icons-fix.py in python
* Select your steam install folder (usually C:\Program Files (x86)\Steam)
* Every icon fixed should appear in console

## How it works
* Finds Desktop directory on your machine and set it into Shortcuts_directory
* Get the steam folder directory using tkinter folder picker
* Finds all .url files in Shortcuts_directory
### For every .url file found
* Read it to gather app_id, icon_id using the path stored inside the shortcut (If it was updated on Steam servers the icon fix may fail), build new content for that file replacing the steam path (in case you changed it)
* Makes a request to cdn.cloudflare.steamstatic.com to download the url using app_id and the icon_id found in the .url file.
* Writes the new .ico in the Steam icons cache directory
* Overwrite the .url file with the new content