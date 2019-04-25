#############################################
### Script: discover.py                   ###
### Authors: G. Kakkavas, K. Tsitseklis   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################

import threading
import udp_transmit
import udp_receive
import sys
import radio_receive
import radio_transmit
import flag_mod
import json
import os 
import random
import time  
import socket
from collections import Counter
import socket
import netifaces as ni
import receive_transmit


def l2str(alist):
    s = ''
    for e in alist:
        s = s + str(e)
    return s

def makeDictionary(list):
    dictionary = {}
    numCh = len(list[0])
    for t in list:
        dictionary[t[0]] = []
        for i in range(1,numCh):
            dictionary[t[0]].append(t[i])
    return dictionary


def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]
    
    
def k_mostCommonLines(lines, k):
    winners = list()
    for i in range(k):
        winners.append(Most_Common(lines))
        lines = [l for l in lines if l != winners[i]]
    return winners

def getVectors(filename, strlen, nodeList):

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    lines = [l for l in lines if l != '\n']
     
    nodesFound = list()
    for line in lines:
        if len(line.split()) != strlen:
            continue
        try:    
            n = int(line.split()[0])
            if n not in nodeList:
                continue
        except ValueError:
            continue
            
        if n not in nodesFound:
            nodesFound.append(n)
    k = len(nodesFound)
    
    winners = k_mostCommonLines(lines, k)

    return winners

    
    
def exchange_info(ID, data, controllerIP, gain, udp_port):

    freq_control = 3000e6
    file2send = '/root/total/discovery_phase/my_info.txt'
    file_received = '/root/total/discovery_phase/received_info.txt'
    ready_file = '/root/total/discovery_phase/ready.txt'
    ok_file = '/root/total/discovery_phase/ok.txt'
    sec = 4
    
    f = open(file2send, 'w')
   
    if not isinstance(data,basestring):
        data = l2str(data)
    
    str2fil = str(ID) + ' ' + data + '\n'
    f.write(str2fil)
    f.close()
   
    myIP = socket.gethostbyname(socket.gethostname())
    with open('/root/total/ipnet.json') as jf:
        diction = json.load(jf)
        ips = diction['net']
    
    nodeList = [int(x) for x in ips.keys()]
    num_of_ch = len(nodeList)-1
    print 'num_of_channels ', num_of_ch
    f = open('/root/total/discovery_phase/ready.txt', 'w')
    f.write('Ready ' + str(ID) + ' To Exchange\n')
    f.close()
    udp_transmit.transmit(controllerIP, udp_port+int(ID), ready_file) 
   
    udp_receive.receive(myIP, udp_port, ok_file)
    
     
    receive_transmit.transceive(freq_control+int(ID)*100e6, freq_control+100e6*min(nodeList), file2send, file_received, sec, num_of_ch, gain)   

    winners = getVectors(file_received, 2, nodeList)
    os.remove(file2send)
    os.remove(file_received)
    os.remove(ok_file)
    os.remove(ready_file) 
    
    return winners

if __name__ == '__main__':

    # usage: used to discover a node's neighbours (Ts)
    # must specify a proper absolute path for the algorithm
    # to be able to properly run and open/close/remove needed files
    if len(sys.argv) != 6:
        print "Please insert correct number of arguments as specified below"
        print "node ID, data2exchage, controller node's IP address, gain and udp_port"
    else:
        ID = (sys.argv[1])
        data = sys.argv[2]
        controllerIP = sys.argv[3]
        gain = eval(sys.argv[4])
        udp_port = eval(sys.argv[5])
        w = exchange_info(ID, data, controllerIP, gain, udp_port)
        print "Neighbors:", w
