#############################################
### Script: flag_mod.py                   ###
### Authors: G. Kakkavas, K. Tsitseklis   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################

# this module is used as a global variable that can be changed from every script
# it is used by the discover.py and radio_receive.py script

flag = 0

def raise_flag():
    global flag
    flag = 1

def drop_flag():
    global flag
    flag = 0

def get_flag():
    global flag
    return flag
