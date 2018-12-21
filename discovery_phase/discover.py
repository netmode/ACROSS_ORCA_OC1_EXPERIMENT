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

flag_mod.flag = 0
timeToEnd = False

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
            n = int(line[0])
            if n not in nodeList:
                continue
        except ValueError:
            continue
            
        if n not in nodesFound:
            nodesFound.append(n)
    k = len(nodesFound)
    
    winners = k_mostCommonLines(lines, k)

    return winners


def udp_listen(IP_address, udp_port, filename):
    # wait for the controller to tell the node that its his turn to transmit
    udp_receive.receive(IP_address, udp_port, filename)
    # udp receiver closes only when something is received
    flag_mod.flag = 1
    # flag is raised, so radio_send thread will see this change

def radio_listen(freq, filename):
    # while it is not yet turn to transmit and after the transmission and till
    # all nodes have transmitted their info, keep listening
    global timeToEnd
    while (not timeToEnd):
        if (flag_mod.flag == 0):
            radio_receive.receive(freq, filename)
        else:
            continue


def radio_send(freq, filename, gain, IP_address, udp_port, filename2):
# when instructed by the controller, transmit proper data 
    global timeToEnd
    while (not timeToEnd):
        if (flag_mod.flag == 1):
            print "Radio SENDING -- discovery phase at gain ", gain
            radio_transmit.transmit(freq, filename, gain)
            udp_transmit.transmit(IP_address, udp_port, filename2)
            flag_mod.flag = 0
            break


def one_iteration(ID, myIP, file2broad, receivFile, controllerIP, gain):

    # specified port for discovery phase (controller listens to this port in 
    # order to handle discovery requests)    
    udp_port = 12000
    # control frequency (fine tune according to operation environment)
    freq = 400e6

    f = open('/root/total/discovery_phase/ready.txt', 'w')
    f.write('Ready ' + str(ID) + ' To Discover\n')
    f.close()

    f = open('/root/total/discovery_phase/ok.txt', 'w')
    f.write('ok!\n')
    f.close()

    # sleep for some amount of time so the requests from various nodes are not send 
    # simultaneously to the controller
    time.sleep(int(ID)/5.0)

    udp_transmit.transmit(controllerIP, udp_port , '/root/total/discovery_phase/ready.txt')

    myIP = ni.ifaddresses('eth1')[ni.AF_INET][0]['addr']
    t1 = threading.Thread(target=udp_listen, args=[
                          myIP, udp_port, '/root/total/discovery_phase/timeTosend.txt', ])

    t2 = threading.Thread(target=radio_listen, args=[
                          freq, receivFile, ])

    t3 = threading.Thread(target=radio_send, args=[
                          freq, file2broad, gain, controllerIP, udp_port, '/root/total/discovery_phase/ok.txt', ])


    t1.start()
    t2.start()
    t3.start()
  
    udp_receive.receive(myIP, udp_port+1, '/root/total/discovery_phase/over.txt')
        
    flag_mod.flag = 2

    global timeToEnd
    timeToEnd = True
       
    os.remove('/root/total/discovery_phase/ready.txt')
    os.remove('/root/total/discovery_phase/ok.txt')   
    os.remove('/root/total/discovery_phase/timeTosend.txt')
    os.remove('/root/total/discovery_phase/over.txt')
    
    t1.join()
    t2.join()
    t3.join()
  
    flag_mod.flag = 0
    timeToEnd = False    
    
    
    
def getNeigh(ID, myIP, controllerIP, gain):

    f = open('/root/total/discovery_phase/myID.txt', 'w')

    if not isinstance(myIP,basestring):
        myIP = l2str(myIP)
    
    str2fil = str(ID) + ' ' + myIP + '\n'
    f.write(str2fil)
    f.close()
   
    myIP = socket.gethostbyname(socket.gethostname())
    with open('/root/total/ipnet.json') as jf:
        diction = json.load(jf)
        ips = diction['net']
    
    nodeList = [int(x) for x in ips.keys()]

    one_iteration(ID, myIP, '/root/total/discovery_phase/myID.txt', '/root/total/discovery_phase/neighIDs.txt', controllerIP, gain)
    # at this time each node has a text file containing info from all nodes
    # getVectors is used in order to find all the information in the file (repetition, damaged data)
    winners = getVectors('/root/total/discovery_phase/neighIDs.txt', 2, nodeList)
    os.remove('/root/total/discovery_phase/myID.txt')
    os.remove('/root/total/discovery_phase/neighIDs.txt') 
    
    return winners

if __name__ == '__main__':

    # usage: used to discover a node's neighbours (Ts)
    # must specify a proper absolute path for the algorithm
    # to be able to properly run and open/close/remove needed files
    if len(sys.argv) != 5:
        print "Please insert correct number of arguments as specified below"
        print "node ID, node's IP address, controller node's IP address, gain"
    else:
        ID = (sys.argv[1])
        myIP = sys.argv[2]
        controllerIP = sys.argv[3]
        gain = eval(sys.argv[4])
        w = getNeigh(ID, myIP, controllerIP, gain)
        print "Neighbors:", w
