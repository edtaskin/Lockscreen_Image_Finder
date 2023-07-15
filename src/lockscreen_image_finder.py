from getpass import getpass
import sys, os, shutil, getpass
from PIL import Image
import re
import locale, ctypes
import json

save_path = None
image_count = 0

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

    print(f"FINISHED: {image_count} images found and copied to target location {save_path}.\n")

def assert_save_path():
    try:
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
    except (OSError, IOError) as e:
        print("ERROR: Given path is not valid. Try another path or use the default path by not specifying a directory.")
        sys.exit()

def get_system_lang():
    windll = ctypes.windll.kernel32
    print(locale.windows_locale[windll.GetUserDefaultUILanguage()]) #TODO DEL
    return locale.windows_locale[windll.GetUserDefaultUILanguage()]

def get_desktop_path(lang):
    print(os.path.exists(r"..\translations.json")) # TODO
    with open(r"..\translations.json", "r", encoding="utf-8") as file:
        translations = json.load(file)
    print(translations.get(lang))
    return os.path.join(os.path.join(os.environ['USERPROFILE']), translations.get(lang))

if len(sys.argv) == 1:
    lang = get_system_lang()
    save_path = get_desktop_path(lang)
    getImages()
else:
    if sys.argv[1] == "--help":
        print("Usage: python3 lockscreen-image-finder.py [DIRECTORY] (optional)")
    elif re.search(r"([a-zA-Z]:\\)?(?:[\w]+\\)+[\w]+", sys.argv[1]):
        save_path = sys.argv[1]
        assert_save_path()
        getImages()
    else:
        print("Invalid option.\nTry 'python3 lockscreen-image-finder.py --help' for more information.")

