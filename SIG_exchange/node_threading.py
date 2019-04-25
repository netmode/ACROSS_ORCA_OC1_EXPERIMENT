#############################################
### Script: flag_mod.py                   ###
### Authors: G. Kakkavas, K. Tsitseklis   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################

import json
import os
import random
import sys
import time
import udp_transmit
import udp_receive
import rv
import receive_transmit
from shutil import copyfile

def rem_dupl(alist):
    """ Removes duplicates from the list given as input """
    newl = list()
    for el in alist:
        if el not in newl:
            newl.append(el)
    return newl
    

def exchange(ID, vectorsSend, nCh, gain, sec):
    """ Vectors' exchange within the neighborhood Gs.
        vectorsSend: contains the filename with the data to be exchanged """

    udp_port = 11000
    freq_control = 3000e6
    ready_file = '/root/total/SIG_exchange/ready.txt'
    ok_file = '/root/total/SIG_exchange/ok.txt'
    file_received = '/root/total/SIG_exchange/dataReceived.txt'
    file_received2 = '/root/total/SIG_exchange/dataReceived2.txt'
    file2Send = '/root/total/SIG_exchange/tsdata.txt'

    with open(ready_file, 'w') as f:
        f.write("Ready to start phase!")

    # exchange vectors within transmission range Ts
    # winners is a list that contains the lines corresponding to each neighbor data
    # tsA, tsN, tsC, tsU are lists of the 1-hop neighbors respective vectors

    # read configuration file
    with open('/root/total/ipnet.json') as jf:
        diction = json.load(jf)
        ips = diction['net']
    
    # dictionary ips contains the IP addresses of the nodes
    ips = {int(x): y.encode('utf8') for x,y in ips.items()}
   
    nodeList = ips.keys() # list of nodes
    c_id = max(ips.keys()) # controller always takes the largest id
    
    udp_transmit.transmit(ips[c_id], udp_port+int(ID), ready_file)
    udp_receive.receive(ips[ID], udp_port, ok_file)    

    receive_transmit.transceive(freq_control+int(ID)*100e6, freq_control+100e6*min(nodeList), vectorsSend, file_received, sec, c_id-3, gain) 
    copyfile(file_received, '/root/total/kostacito.txt')
    winners, tsA, tsN, tsC, tsU = rv.getVectors(file_received, nCh, nodeList)
    tsA = [l for l in tsA if l[0] != ID]
    tsN = [l for l in tsN if l[0] != ID]
    tsC = [l for l in tsC if l[0] != ID]
    tsU = [l for l in tsU if l[0] != ID]
        
    print "First step completed! -- Signaling Exchange"
    
    # write in the file the data of your 1-hop neighbors
    f2 = open(file2Send, 'w')
    for w in winners:
        f2.write(w)
    f2.close()

    # exchange within your transmission range the above file
    receive_transmit.transceive(freq_control+int(ID)*100e6, freq_control+100e6*min(nodeList), file2Send, file_received2, sec, c_id-3, gain)
    _, gA, gN, gC, gU = rv.getVectors(file_received2, nCh, nodeList)
    
    print "Second step completed! -- Signaling Exchange"
    
    # GA, GN, GC, GU are lists of the neighbors respective vectors
    GA = rem_dupl(tsA + [l for l in gA if l[0] != ID]) # remove duplicates and yourself
    GN = rem_dupl(tsN + [l for l in gN if l[0] != ID])
    GC = rem_dupl(tsC + [l for l in gC if l[0] != ID])
    GU = rem_dupl(tsU + [l for l in gU if l[0] != ID])
    
    print "\nTRANSMISSION AREA"
    print tsA
    print tsN
    print tsC
    print tsU
    
    print "\nNEIGHBORHOOD"
    print GA
    print GN
    print GC
    print GU
    
    os.remove(file2Send)
    os.remove(file_received)
    os.remove(ok_file)
    os.remove(ready_file) 
    os.remove(file_received2)
    os.remove(vectorsSend)

    return (tsU, GA, GN, GU)
   

if __name__ == '__main__':
    ID = eval(sys.argv[1])
    vectorsSend = sys.argv[2]
    nCh = eval(sys.argv[3])
    gain = eval(sys.argv[4])
    sec = eval(sys.argv[5])
    exchange(ID, vectorsSend, nCh, gain, sec)
