from getpass import getpass
from re import ASCII
import sys, pickle, os, shutil, ctypes, getpass
from pathlib import Path
from PIL import Image

ASCII_ART = """

 __          ___           _                     _                _                                   _____                              ______ _           _            
 \ \        / (_)         | |                   | |              | |                                 |_   _|                            |  ____(_)         | |           
  \ \  /\  / / _ _ __   __| | _____      _____  | |     ___   ___| | _____  ___ _ __ ___  ___ _ __     | |  _ __ ___   __ _  __ _  ___  | |__   _ _ __   __| | ___ _ __  
   \ \/  \/ / | | '_ \ / _` |/ _ \ \ /\ / / __| | |    / _ \ / __| |/ / __|/ __| '__/ _ \/ _ \ '_ \    | | | '_ ` _ \ / _` |/ _` |/ _ \ |  __| | | '_ \ / _` |/ _ \ '__| 
    \  /\  /  | | | | | (_| | (_) \ V  V /\__ \ | |___| (_) | (__|   <\__ \ (__| | |  __/  __/ | | |  _| |_| | | | | | (_| | (_| |  __/ | |    | | | | | (_| |  __/ |    
     \/  \/   |_|_| |_|\__,_|\___/ \_/\_/ |___/ |______\___/ \___|_|\_\___/\___|_|  \___|\___|_| |_| |_____|_| |_| |_|\__,_|\__, |\___| |_|    |_|_| |_|\__,_|\___|_|    
                                                                                                                             __/ |                                       
                                                                                                                            |___/                                        

"""
save_path = None
filename = "path.pickle"
image_count = 0

COMMANDS = """-start: to execute the program\n
-change: to change the save directory\n
-setBackground: to set image as background (If it is not the intended image use -setBackground again to set the next image as background.)\n
-commands: to display commands list\n
-exit: to terminate the program"""

def start():
    global save_path
    try:
        with open(filename, "rb") as f:
            save_path = pickle.load(f)
    except (OSError, IOError) as e:
        f = open(filename, "wb")
        f.close()

    if not save_path:
        print("Where to store the finded images?")
        save_path = input("Write 'desktop' for desktop or give a specific path to save finded images: ")
        if save_path == "desktop":
            print("here")
            save_path = rf"C:\Users\{getpass.getuser()}\Desktop"
        with open(filename, "wb") as f:
            pickle.dump(save_path, f)

#TODO Exception handling
def getImages():
    global image_count
    print("save_path: %s"%save_path)

    src_path = rf"C:\Users\{getpass.getuser()}\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
    os.chdir(src_path)

    destination_path = os.path.join(save_path, "LockscreenWallpapers")

    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    for file in os.listdir(src_path):
        shutil.copy2(file, destination_path)

    os.chdir(destination_path)

    image_count = 0
    for file in os.listdir():
        with Image.open(file) as img:
                width, height = img.size
        if width != 1920 or height != 1080:
            os.remove(file)
        else:
            image_count += 1
            os.rename(file, f"wallpaper{image_count}.jpg")

    print(f"FINISHED: {image_count} images found and copied to target location.\n")


def changeSavePath():
    global save_path
    new_path = input("Enter the new destination path for the images: ")
    save_path = new_path
    try:
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
    except (OSError, IOError) as e:
        print("ERROR: Given path is not accepted, try another path.")
        changeSavePath()


def setBackground(num):
    assert os.getcwd() == os.path.abspath(save_path) + r"\LockscreenWallpapers"
    for file in os.listdir():
        if Path(os.path.abspath(file)).stem == f"wallpaper{num}":
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(file), 0)
    print(f"FINISHED: Wallpaper {num} is set as background.\n")


print(ASCII_ART)
print("Welcome to Windows Lockscreen Wallpaper Finder!")
print("Write '-start' to execute the program or '-commands' to see the commands list.")

background_num = 1
while True:
    command = input("Enter a command: ")
    if command == "-start":
        start()
        getImages()
    elif command == "-change":
        changeSavePath()
    elif command == "-commands":
        print(COMMANDS)
    elif command == "-setBackground":
        if background_num > image_count:
            print("ERROR: No more images left to set as background.")
        else:    
            setBackground(background_num)
            background_num += 1
    elif command == "-exit":
        break

