# Requires requests to be installed (can be installed with pip)

import json
import os
import requests
import tkinter as tk
from tkinter import filedialog

user_path = os.environ['UserProfile']
if not user_path:
    print("UserProfile environment variable invalid, please specify the Shorcuts directory manually")
    exit(1)

Shortcuts_directory = f"{user_path}\\Desktop\\" # Where the script will search for .url files

steam_icons_relative_path = "\\steam\games\\" # Relative to selected steam folder

search_app_id_prefix = "URL=steam://rungameid/" # In URL file which prefix before app_id
iconfile_prefix = "IconFile=" # At which line is ico path in the URL file



URL_Files = {}

def DownloadAndFixIcon(steam_dir, app_id):
    icon_id = URL_Files[app_id]["icon_id"]
    
    output_ico_file = steam_dir + steam_icons_relative_path + icon_id + ".ico"
    icon_url = f"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{app_id}/{icon_id}.ico"
    #print(icon_url)
    response = requests.get(icon_url)
    if response.status_code == 200:
        ico_written = False
        with open(output_ico_file, "wb") as file:
            file.write(response.content)
            ico_written = True
            
        if ico_written:
            url_written = False
            with open(URL_Files[app_id]["path"], "w") as f2:
                f2.write(URL_Files[app_id]["changed_content"])
                url_written = True
                
            if url_written:
                print(f"{URL_Files[app_id]['filename']} ({app_id}) Icon fixed successfully.")
            else:
                print(f"{URL_Files[app_id]['filename']} ({app_id}) URL failed to update (that worked if you didn't change steam directory since).")
        else:
            print(f"{URL_Files[app_id]['filename']} ({app_id}) Icon failed to write.")
            
        
    else:
        print(f"Failed to download icon. Status code: {response.status_code}")

def ReadURLFile(steam_dir, path):
    filename = path.split("\\")
    filename = filename[len(filename)-1]
    
    url_file_content = None
    changed_content = []
    with open(path) as f:
        url_file_content = f.read()
    
    if not url_file_content:
        print(f"Could not open file {path}")
        return
        
    app_id = None
    icon_file_name = None
    icon_id = None
    for line in url_file_content.split("\n"):
        changed_line = line
        if line.startswith(f"{search_app_id_prefix}"):
            app_id = line[len(search_app_id_prefix):]
        elif line.startswith(f"{iconfile_prefix}"):
            ic_split = line.split("\\")
            icon_file_name = ic_split[len(ic_split)-1]
            icon_id = icon_file_name.split(".")
            icon_id = icon_id[len(icon_id)-2]
            # steam_dir may have changed location now, set it to the specified path
            changed_line = f"{iconfile_prefix}{steam_dir}{steam_icons_relative_path}{icon_file_name}"
            
        changed_content.append(changed_line)
            
    changed_content = "\n".join(changed_content)

    # Check if everything was found (validate that it is an expected Steam shortcut)
    if app_id and icon_file_name and icon_id:
        URL_Files[app_id] = {
            "path": path,
            "icon_file_name": icon_file_name,
            "icon_id": icon_id,
            "changed_content": changed_content,
            "filename": filename
        }
        
        return app_id

def main():
    if not (os.path.isdir(Shortcuts_directory)):
        print("Invalid shortcuts folder?")
        return
    
    steam_dir = filedialog.askdirectory(title="Select Main Steam directory (Usually C:\Program Files (x86)\Steam)")
    if not (steam_dir):
        print("Invalid steam folder")
        return
    
    steam_dir = steam_dir.replace("/", "\\") # windows URL files use \ so I may do the same...
    if not (os.path.isdir(steam_dir)):
        print("Invalid steam folder (2)")
        return
    
    for v in os.listdir(Shortcuts_directory):
        if v.endswith(".url"):
            url_path = f"{Shortcuts_directory}{v}"
            app_id = ReadURLFile(steam_dir, url_path)
            if app_id:
                #print(URL_Files[app_id])
                DownloadAndFixIcon(steam_dir, app_id)
    

if __name__ == "__main__":
    main()