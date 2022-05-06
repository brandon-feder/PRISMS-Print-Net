#!/usr/bin/python3

# TODO: Setup JSON Schema

from cmath import log
import os, sys, json, string
from time import time

'''
This class is str for all purposes, except it has `is_code` variable 
defined which tells `printc()` to color it has code despite being
a string.
'''
class CodeStr(str):
    def __init__(self, s):
        super().__init__()
        self.is_code = True
    
    def __add__(self, other): return CodeStr(super().__add__(other))
    def __radd__(self, other): return CodeStr(other.__add__(self))

# Usefull aliases
abspath = os.path.abspath
cs = CodeStr

'''
Gets ANSI text color code
    Uses ANSI Escape Sequence Codes (https://stackabuse.com/how-to-print-colored-text-in-python/)
'''
def color_code(style, txt):
    return '\x1b[{};{}m'.format(style, txt)

PATH = cs(abspath(__file__))
DIR = cs(os.path.dirname(PATH))
CONFIG_PATH = DIR + '/config/config.json'

RESET = '\033[0m' # Reset code
INFO = color_code(1, 34) +    '(INFO)    ' + RESET # Bold and blue
ERROR = color_code(1, 31) +   '(ERROR)   ' + RESET # Bold and red
SUCCESS = color_code(1, 32) + '(SUCCESS) ' + RESET # Bold and green
WARNING = color_code(1, 33) + '(WARNING) ' + RESET # Bold and green
SP, NL, UL = " ", "\n", "\n\t - " # Sometimes useful for formatting in `printc`
CODE = color_code(1, 35) # Bold and purple

'''
Custom alternative to print which deals with with
    (a) Counting the current outputs
    (b) Coloring CodeStr-ings other non-str objects
'''
def printc(*args):
    # Setup counter
    global PRINT_COUNTER
    try: PRINT_COUNTER += 1
    except: PRINT_COUNTER = 1
    
    # Create string to print
    pstr = '[%s] '%PRINT_COUNTER
    for arg in args:
        is_code = not isinstance(arg, str) or hasattr(arg, "is_code")
        pstr = (pstr + CODE + str(arg) + RESET) if is_code else (pstr + arg)
    
    print(pstr)

def handle_logs_folder(folder_path):
    if not os.path.isdir(folder_path): # Folder exists
        os.mkdir(folder_path)
    
    file_path = cs(folder_path + "/log-%s.log"%int(time()))

    try:
        with open(file_path, "w") as log:
            printc(SUCCESS, "Created log file: ", file_path)
            log.write("Start of log file!")
    except:
        printc(ERROR, "Error creating or writing to log file")
    
    return file_path

if __name__ == '__main__':
    print()
    printc(INFO, 'Current Directory: ', DIR)

    # ========== DEAL WITH ARGUMENTS ==========

    if len(sys.argv) == 2:
        CONFIG_PATH = cs(abspath(sys.argv[1]))
    
    # Print usefull info for debugging
    printc(INFO, 'Config Path: ', CONFIG_PATH)
    
    # ============ IMPORTANT SETUP ============

    if os.access(CONFIG_PATH, os.R_OK | os.W_OK):
        with open(CONFIG_PATH, 'r') as config_file:
            try:
                config = json.load(config_file)
                printc(SUCCESS, "Read config file")
                
                logs_path = cs(abspath(config['logs']))
                printc(INFO, "Logs folder path: ", logs_path)
                log_path = handle_logs_folder(logs_path)
                os.system("npm run start %s %s"%(CONFIG_PATH, log_path))
            except:
                printc(ERROR, "Color not read config file. The file likely contains invalid json.")
    else:
        printc(
            ERROR, 'Can not read and write from config file', 
            UL, 'File may not exist or may not have proper permissions',
            UL, 'Config file path: ', CONFIG_PATH
        )