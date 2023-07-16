from getpass import getpass
import sys, os, shutil, getpass
from PIL import Image
import re
import argparse

save_path = None
image_count = 0

def getImages():
    global image_count
    image_count = 0 
    print("save_path: %s"%save_path)

    src_path = rf"C:\Users\{getpass.getuser()}\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
    os.chdir(src_path)
    print(f"src path: {src_path}")
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

    print(f"FINISHED: {image_count} images found and copied to target location {save_path}.\n")

def assert_save_path():
    try:
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
    except (OSError, IOError) as e:
        print("ERROR: Given path is not valid. Try another path or use the default path by not specifying a directory.")
        sys.exit()

def print_help():
    print("""
usage: python3 path_to_lockscreen_image_finder.py [-h] [save_dir]

Copies the current Windows lockscreen wallpaper stack from the file system to the specified directory or to Desktop by default.

optional arguments:
-h, --help  show help message and exit
save_dir    save the found images to this directory instead of the default one
          """)

if len(sys.argv) == 1:
    save_path = os.path.join(os.environ['USERPROFILE'], "Desktop") # TODO Simply change "Desktop" to its translation in your system language
    getImages()
else:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print_help()
    elif re.search(r"([a-zA-Z]:\\)?(?:[\w]+\\)+[\w]+", sys.argv[1]):
        save_path = sys.argv[1]
        if save_path[-len(r"\LockscreenWallpapers"):] == r"\LockscreenWallpapers":
            save_path = save_path[:-len(r"\LockscreenWallpapers")]
        assert_save_path()
        getImages()
    else:
        print("Invalid option.\nTry 'python3 lockscreen-image-finder.py --help' for more information.")

