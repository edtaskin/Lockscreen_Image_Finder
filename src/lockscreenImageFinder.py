from getpass import getpass
from re import ASCII
import sys, pickle, os, shutil, ctypes, getpass
from pathlib import Path
from PIL import Image

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
        print("FIRST USE CONFIG: Where to store the found images?")
        save_path = input("Write 'desktop' for desktop or give a specific path to save found images: ")
        # if save_path == "desktop":
        #     save_path = rf"C:\Users\{getpass.getuser()}\Desktop"
        with open(filename, "wb") as f:
            pickle.dump(save_path, f)


def getImages():
    global image_count
    image_count = 0 
    print("save_path: %s"%save_path)

    src_path = rf"C:\Users\{getpass.getuser()}\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
    os.chdir(src_path)

    destination_path = os.path.join(save_path, "LockscreenWallpapers")

    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    for file in os.listdir(src_path):
        with Image.open(file) as img:
            width, height = img.size
        if width == 1920 and height == 1080:
            image_count += 1
            shutil.copy2(file, destination_path)

    os.chdir(destination_path)

    image_index = 0 
    for file in os.listdir():
        image_index += 1
        if "wallpaper" not in os.path.basename(file):
            while True:
                try:
                    os.rename(file, f"wallpaper{image_index}.jpg")
                    break;
                except FileExistsError:
                    image_index += 1

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

print("Welcome to Windows Lockscreen Image Finder!")
print("Write '-start' to execute the program or '-commands' to see the commands list.")

background_num = 1
while True:
    command = input("Enter a command: ")
    if command == "-start":
        if (save_path == None or os.getcwd() != os.path.abspath(save_path) + r"\LockscreenWallpapers"):
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

