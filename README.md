# Windows Lockscreen Image Finder
This is a script that finds the current stack of the daily-changing Windows lockscreen images from the file system and copies them to a directory.

### Prerequisites
- Windows 10+ operating system
- Python 3.x

### Usage
To run the script use the following command: <code>python3 lockscreenImageFinder.py</code> or <code>python3 lockscreenImageFinder.py save_dir</code> if you want to specify a custom save directory for the images.

#### Optional arguments
- save_dir: path to custom save directory, to change the save directory from the default, which is the Desktop 
- "-h" or "--help": to print help message

**Note**: This script assumes that the system language is English, and therefore the desktop is named "Desktop". If your system language is not English however, you can make the script usable by a little change in the code:
Simply change "Desktop" at line 65 of lockscreen_image_finder.py to be the translation of Desktop in your own system language.
<code>save_path = os.path.join(os.environ['USERPROFILE'], "Desktop") # TODO Simply change "Desktop" to its translation in your system language </code>

#### Example
<code>save_path = os.path.join(os.environ['USERPROFILE'], "Masaüstü") # "Desktop" changed to "Masaüstü" for Turkish system language</code>
