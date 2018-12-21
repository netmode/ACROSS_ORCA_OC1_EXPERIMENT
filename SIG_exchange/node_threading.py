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
import threading
import time
import udp_transmit
import udp_receive
import radio_receive
import radio_transmit
import flag_mod as f
import rv


f.flag = 0
timeToEnd = False

def rem_dupl(alist):
    """ Removes duplicates from the list given as input """
    newl = list()
    for el in alist:
        if el not in newl:
            newl.append(el)
    return newl

def udp_listen(IP_address, udp_port, filename):
    # wait for the controller to tell the node that its turn to transmit
    udp_receive.receive(IP_address, udp_port, filename)
    # udp receiver closes only when something is received
    f.flag = 1
    # flag is raised, so radio_send will see this change

def radio_listen(freq, filename):
    # keep listening while it is not yet your turn to transmit and after you have
    # transmitted your vectors until all nodes have finished their transmissions
    global timeToEnd
    while (not timeToEnd):
        if (f.flag == 0):
            radio_receive.receive(freq, filename)
        else:
            continue


def radio_send(freq, filename, gain, IP_address, udp_port, filename2):
    # When instructed by the controller, transmit your vectors
    global timeToEnd
    while (not timeToEnd):
        if (f.flag == 1):
            print "Radio SENDING -- signaling exchange"
            radio_transmit.transmit(freq, filename, gain)
            udp_transmit.transmit(IP_address, udp_port, filename2)
            f.flag = 0


def one_iteration(filename, filename1, filename2, filename3, filename4, ID, nCh, gain):
    """ Info exchange within transmission range (1-hop neighbors)
        ID: Identifier of the node
        nCh: number of channels
        gain: tx gain for radio transmissions """
   
    # designated port for the signaling exchange phase - controller listens to that port
    udp_port = 11000
    freq = 400e6 # control channel
    
    # read configuration file
    with open('/root/total/ipnet.json') as jf:
        diction = json.load(jf)
        ips = diction['net']
    
    # dictionary ips contains the IP addresses of the nodes
    ips = {int(x): y.encode('utf8') for x,y in ips.items()}
   
    nodeList = ips.keys() # list of nodes
    c_id = max(ips.keys()) # controller always takes the largest id
    
    # each node sleeps for a particular amount of time, depending on its ID in order to avoid 
    # sending simultaneously the corresponding notifications to the controller
    time.sleep(ID/5.0+0.7)
    
    # notify the controller that you are ready to transmit your vectors
    udp_transmit.transmit(ips[c_id], udp_port, filename)
    
    # create separate threads
    t1 = threading.Thread(target=udp_listen, args=[
                          ips[ID], udp_port, filename1, ])

    t2 = threading.Thread(target=radio_listen, args=[
                          freq, filename2, ])

    t3 = threading.Thread(target=radio_send, args=[
                          freq, filename3, gain, ips[c_id], udp_port, filename, ])

    t1.start()
    t2.start()
    t3.start()
    
    # wait for the controller to notify you for the termination
    udp_receive.receive(ips[ID], udp_port+1, filename4)
    
    f.flag = 2

    global timeToEnd
    timeToEnd = True
    
    # parse and clean the received data (the specified file contains the data of all 1-hop neighbors)
    winners, lA, lN, lC, lU = rv.getVectors('/root/total/SIG_exchange/dataReceived.txt', nCh, nodeList)
    
    os.remove(filename1)
    os.remove(filename2)
    os.remove(filename3)
    os.remove(filename4)
    
    t1.join()
    t2.join()
    t3.join()
  
    f.flag = 0
    timeToEnd = False
    
    return (winners, lA, lN, lC, lU)
    
    
def exchange(ID, vectorsSend, nCh, gain):
    """ Vectors' exchange within the neighborhood Gs.
        vectorsSend: contains the filename with the data to be exchanged """

    filename = '/root/total/SIG_exchange/sendMe.txt'
    filename1 = '/root/total/SIG_exchange/order.txt'
    filename2 = '/root/total/SIG_exchange/dataReceived.txt'
    filename3 = vectorsSend
    filename4 = '/root/total/SIG_exchange/term.txt'
    
    # exchange vectors within transmission range Ts
    # winners is a list that contains the lines corresponding to each neighbor data
    # tsA, tsN, tsC, tsU are lists of the 1-hop neighbors respective vectors
    winners, tsA, tsN, tsC, tsU = one_iteration(filename, filename1, filename2, filename3, filename4, ID, nCh, gain)
    
    print "First step completed! -- Signalling Exchange"
    
    # write in the file the data of your 1-hop neighbors
    f2 = open(filename3, 'w')
    for w in winners:
        f2.write(w)
    f2.close()
    
    # exchange within your transmission range the above file
    _, gA, gN, gC, gU = one_iteration(filename, filename1, filename2, filename3, filename4, ID, nCh, gain)
    
    print "Second step completed! -- Signalling Exchange"
    
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
    
    return (tsU, GA, GN, GU)
   

if __name__ == '__main__':
    ID = eval(sys.argv[1])
    vectorsSend = sys.argv[2]
    nCh = eval(sys.argv[3])
    gain = eval(sys.argv[4])
    exchange(ID, vectorsSend, nCh, gain)
