#! /usr/bin/env python2
#############################################
### Script: semipar_controller.py           ###
### Authors: G. Kakkavas, K. Tsitseklis   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################


import udp_receive
import udp_transmit
import time
import sys
import os
import threading
import json
from collections import Counter


def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]
    
    
def k_mostCommonLines(lines, k):
    winners = list()
    for i in range(k):
        winners.append(Most_Common(lines))
        lines = [l for l in lines if l != winners[i]]
    return winners
        

def get_new_Us(filename, nodeList):

    f = open(filename, 'r')
    lines = f.readlines()
    lines = [l for l in lines if l != '\n']
    f.close()
    nodesFound = list()
    for l in lines:
        ll = l.split()
        try:
            csm = int(ll[-1])
        except ValueError:
            continue
        if len(ll) != csm:
            continue
        try:    
            n = int(ll[0])
            if n not in nodeList: 
                continue
        except ValueError:
            continue
        if n not in nodesFound:
            nodesFound.append(n)
    k = len(nodesFound)
    winners = k_mostCommonLines(lines,k)
    return winners

    

def udp_listen(IP_address, udp_port, filename):           
    udp_receive.receive(IP_address, udp_port, filename) 
    print "got data from node", udp_port - 8000
    global counter
    counter = counter + 1
    print 'Received'
    

if __name__ == '__main__':
    # usage: controller of semi-parallel gibbs sampling phase 

    counter = 0
    
    if (len(sys.argv)!=4):
        print "Please set the algorithm's arguments in the order specified below"
        print "auxiliary file, id of controller, port to listen to"
    else:
        filename = sys.argv[1]
        controller_id = eval(sys.argv[2])
        udp_port = eval(sys.argv[3])     
        with open('/root/total/ipnet.json') as jf:
            diction = json.load(jf)
            ips = diction['net']
    
        ips = {int(x): y.encode('utf8') for x,y in ips.items()}

        IP_address = ips[controller_id]
        num_nodes = len(ips.keys()) - 1
        
        while (1):

            thread_array = []

            for i in ips.keys():
                if i == controller_id:
                    continue
                # open a thread for each node (except for controller), nodes will notify when they are ready (or finished)
                temp = threading.Thread(target=udp_listen, args=[ips[controller_id], udp_port+i, filename[:-4]+str(i)+'.txt', ])
                thread_array.append(temp)

            for t in thread_array:
                t.start()
                 
            #global counter
            while (counter<num_nodes):
                pass
            
            # at this point all nodes have notified the controller of their  readiness(completion)
            
            #time.sleep(0.01)        
            print "READY!!!"
            nodes = [i for i in ips.keys() if i != controller_id ]

            #read filename
            fname = 'all_msgs.txt'
            f2 = open(fname,'w')
            ids = [i for i in ips.keys() if i != controller_id]
            for i in ids:
                f = open(filename[:-4]+str(i)+'.txt','r')
                dataread = f.readlines()
                for l in dataread:
                    f2.write(l)
                f.close()
            f2.close()
            winners = get_new_Us(fname, ips.keys())

            #construct filename2
            filename2 = open('new_data.txt', 'w+')
            print 'winnners = ', winners
            for w in winners:
               filename2.write(w)
            filename2.close()
        

            for n in nodes:
                print 'Sending at N1-' + str(n)
                udp_transmit.transmit(ips[n], udp_port, 'new_data.txt')
            print "Terminated iteration"
            
            for t in thread_array:
                t.join()
            
            #global counter
            counter = 0
            #os.remove(filename)
            os.remove('new_data.txt')
            os.remove('all_msgs.txt')
            for i in ids:
                os.remove(filename[:-4]+str(i)+'.txt')
