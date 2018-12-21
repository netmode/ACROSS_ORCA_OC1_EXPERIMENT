#############################################
### Script: fast_node_threading.py        ###
### Authors: K. Tsitseklis, G. Kakkavas   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################

import threading
import udp_transmit
import udp_receive
import sys
import rv
import os
import random
import time
from shutil import copyfile
import json

counter = 0


def rev_lookup(adict, value):

    for index,element in adict.items():
        if element == value:
            return index


def rem_dupl(alist):
    newl = list()
    for el in alist:
        if el not in newl:
            newl.append(el)
    return newl

def udp_listen(IP_address, udp_port, filename):           
    udp_receive.receive(IP_address, udp_port, filename) 
    global counter
    counter = counter + 1


def udp_send(IP_address, udp_port, filename):           
    udp_transmit.transmit(IP_address, udp_port, filename)   
    global counter
    counter = counter + 1


def one_iteration(filename, filename1, filename2, filename3, ID, nCh, neigh):
    
    with open('/root/total/ipnet.json') as jf:
        diction = json.load(jf)
        ips = diction['net']

    ips = {int(x): y.encode('utf8') for x,y in ips.items()}
    
    nodeList = [int(x) for x in ips.keys()]

    threadR_array = []
    threadS_array = []

    # in a topology a node opens up as many receivers 
    # and transmitters as its neighbours number. Each is listening/transmitting 
    # in a carefully selected port.
    
    # open receivers in threads
    for ip in neigh:
        snd = rev_lookup(ips, ip)
        # port = sender*1000 + destination
        port = int(snd)*1000 + int(ID) 
        # open a receiver
        temp = threading.Thread(target=udp_listen, args=[ips[ID], port, filename2, ])
        threadR_array.append(temp)
        # open a sender
        port = int(ID)*1000 + int(snd)
        temp = threading.Thread(target=udp_send, args=[ip, port, filename3, ])
        threadS_array.append(temp)
    
    for t in threadR_array:
        t.start()

    # controller always has the maximum ID
    c_id = max(ips.keys())
    udp_transmit.transmit(ips[c_id], 13000+ID, filename)
    udp_receive.receive(ips[ID], 13000, filename1)
    
    for t in threadS_array:
        t.start()

    global counter
    while(counter<(len(threadR_array)+len(threadS_array))):
        pass

    counter = 0

    winners, lA, lN, lC, lU = rv.getVectors('/root/total/final_gibbs_sampling/dataReceived.txt', nCh, nodeList)
    
    os.remove(filename1)
    os.remove(filename2)
    os.remove(filename3)
    
    for t in threadR_array:
        t.join()

    for t in threadS_array:
        t.join()
  
    time.sleep(0.1)

    return (winners, lA, lN, lC, lU)
    
    
def exchange(ID, filename3, nCh, neigh):
    
    ID = int(ID) 
    filename = '/root/total/final_gibbs_sampling/sendMe.txt'
    filename1 = '/root/total/final_gibbs_sampling/order.txt'
    filename2 = '/root/total/final_gibbs_sampling/dataReceived.txt'

    winners, tsA, tsN, tsC, tsU = one_iteration(filename, filename1, filename2, filename3, ID, nCh, neigh)
    
    f2 = open(filename3, 'w')
    for w in winners:
        f2.write(w)
    f2.close()
    
    _, gA, gN, gC, gU = one_iteration(filename, filename1, filename2, filename3, ID, nCh, neigh)
    
    # remove possible duplicates
    GA = rem_dupl(tsA + [l for l in gA if l[0] != ID])
    GN = rem_dupl(tsN + [l for l in gN if l[0] != ID])
    GC = rem_dupl(tsC + [l for l in gC if l[0] != ID])
    GU = rem_dupl(tsU + [l for l in gU if l[0] != ID])

    
    return (tsU, GA, GN, GC, GU)   


if __name__ == '__main__':
    # usage: This script is responsible for the info exchange between nodes 
    # during gibbs sampling
    if (len(sys.argv)!=4):
        print "Please insert the correct number of arguments as specified below"
        print "node ID, filename to send, number of channels, neighborhood of node" 
    else:
        ID = eval(sys.argv[1])
        filename = sys.argv[2]
        nCh = eval(sys.argv[3])
        neigh = eval(sys.argv[4])
        exchange(ID, filename, nCh, neigh)
