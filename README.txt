I am running this on windows so if your a mac user you may need to make some changes but here are the instructions to get this to work for you.

Download Chrome Web Driver, unzip and place chromedriver.exe in C:\WebDriver\
https://googlechromelabs.github.io/chrome-for-testing/
win64 version - https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.159/win64/chromedriver-win64.zip


Instally Visual Studio Code
https://code.visualstudio.com/

Install Python inside Visual Studio Code - Extensions Tab
https://marketplace.visualstudio.com/items?itemName=ms-python.python

can also install Python Extension Pack (may not be necessary)
https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack


Once VS Code is setup with python in Explorer Tab Create ud_webscraping.py file in whatever folder you want to start it from i.e. C:\Users\{username}\{path_to_py_folder}\
and download my script - ud_web_scrape.py - to a folder of your choice


Next you will need to change a few lines of code so it will work on your machine

```
# --- CONFIGURATION ---
USERNAME = "my username"  # Replace with your UD username/email
PASSWORD = "my password"  # Replace with your UD password
CHROME_DRIVER_PATH = r'C:\WebDriver\chromedriver.exe' # Replace with your driver path
output_dir = r"C:\Users\{username}\Desktop\NFL\scrape" # Replace with your windows username

```


next install pip in the terminal
```
python -m pip install --upgrade pip
```

then run this to install the required dependencies
```
pip install selenium
```
if pip isn't found try and run
```
pip3 install selenium
```

now you should be able to start the script

in the terminal type
```
cd C:\Users\{username}\{path_to_py_folder}\
```

```
python ud_webscraping.py
```

or

```
python3 ud_webscraping.py
```

If you have multiple lobbies rerun the script with the number of the lobby after i.e. 1 or nothing for first lobby, 2 for second, etc 

python ud_webscraping.py 2
or
python3 ud_webscraping.py 2


Wait for the script to finish running and then you will have a csv with the contest name in the NFL\scrape\ folder set in the configuration path 

Please note the script will double your team so you will likely have to delete rows 2-11 when you process it as it is just reading every team visible right now
