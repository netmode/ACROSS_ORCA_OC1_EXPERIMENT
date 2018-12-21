#!/usr/bin/env python
#############################################
### Script: PU_availability.py            ###
### Authors: G. Kakkavas, K. Tsitseklis   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################

import os
import PU_detect_channel as PU
import sys

def availability(channel_list, gain):
    """ Returns the availability vector of the SU
        inputs: list of channels and rx gain """
    a = [0]*len(channel_list) # initially set all channels not available
    i = 0
    for ch in channel_list:
        # open a receiver at the specified channel
        PU.detect(ch, 'channel.txt', 0.1, gain)
        # if the produced text file is empty then there is no active PU transmission
        # and the channel is available
        if (os.stat("channel.txt").st_size == 0):
            a[i] = 1    
        i = i + 1
        os.remove("channel.txt")
    return a
    
if __name__ == '__main__':
    #the central frequencies of the channels under examination
    
    channel_list = eval(sys.argv[1])
    gain = eval(sys.argv[2])
    print availability(channel_list, gain)
