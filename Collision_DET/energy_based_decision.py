#!/usr/bin/env python2
#############################################
### Script: energy_based_decision.py      ###
### Authors: K. Tsitseklis, G. Kakkavas   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################

import sys
import transmit_busy_tone as busy
import avg
import channel_energy
import os

def is_empty(mu):
    """ Returns 0 if channel is empty, otherwise returns 1 - the channel is occupied and a collision will occur
        Inputs
        mu: the mean received signal energy """
    if (mu<-48): #-54 corresponds to the noise background level - should be calibrated accordingly for different environments
        print "EMPTY CHANNEL"
        return 0
    else:
        print "COLLISION!"
        return 1


def single_detect_collision(mu, c_freq, threshold):
    if (not is_empty(mu)):
        print "EMPTY CHANNEL"
        return 0
    elif (mu>threshold-1) and (mu<threshold+1):
        print "COLLISION ABOUT TO HAPPEN - DO NOT TRANSMIT"
        return 1            
    else:
        print "COLLISION HAPPENING RIGHT NOW"
        return 2

        
def detect_collision(channel_list, bandwidth):
    collision_channels = [0]*len(channel_list)
    
    for i in range(len(channel_list)):
        ch = channel_list[i]
        channel_energy.energy_measurements(ch, bandwidth)
        mu, _ = avg.find_average('mean_power.txt')
        os.remove('mean_power.txt')
        val = is_empty(mu)
        if val==1:
            collision_channels[i] = 1
   
    return collision_channels #list with 1 in channels with collisions
        

if __name__ == "__main__": ##FIX THIS
    channel_list = eval(sys.argv[1])
    bandwidth = eval(sys.argv[2])
    print detect_collision(channel_list, bandwidth)
