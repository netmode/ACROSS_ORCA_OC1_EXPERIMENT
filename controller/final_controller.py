#! /usr/bin/env python2
#############################################
### Script: final_controller.py           ###
### Authors: G. Kakkavas, K. Tsitseklis   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################
import udp_receive
import udp_transmit
import time
import sys
import os
import json

def check_file(nodes, filename):
    """ Parses file and returns a list of the found nodes """

    f = open(filename, 'r')

    for line in f:
        try:
            n = int(line.split()[1])
        except:
            continue

        if n not in nodes:
            nodes.append(n)

    return nodes


if __name__ == '__main__':
    
    # read the IP addresses of the nodes
    with open('/root/total/ipnet.json') as jf:
        diction = json.load(jf)
        ips = diction['net']
   
    # dictionary with records of the form Node ID: IP address
    ips = {int(x): y.encode('utf8') for x,y in ips.items()}
      
    IP_address = sys.argv[1] # your IP address
    udp_port = eval(sys.argv[2]) # the port you will be using
    filename = sys.argv[3]
    filename3 = sys.argv[4]
    
    while (1):
        nodes = list()
        while len(nodes) < len(ips.keys())-1:
            print "RECEIVING!"
            # receive notification from a SU
            udp_receive.receive(IP_address, udp_port, filename)
            # update the list of ready SUs
            nodes = check_file(nodes, filename)
            print nodes

        print "ALL nodes are ready!"
        time.sleep(1.5)
        for n in nodes:
            print 'Sending at node ' + str(n)
            filename2 = open('node' + str(n), 'w+')
            filename2.write('Node ' + str(n) + ' send!')
            filename2.close()
            # instruct the particular SU that it is its turn to broadcast its vectors
            udp_transmit.transmit(ips[n], udp_port, 'node' + str(n))
            # wait for the node to tell you that it finished transmitting
            udp_receive.receive(IP_address, udp_port, filename3)

      
        print "Signalling Broadcasting terminated!"
        
        # notify the SUs about the end of the signalling phase
        for n in nodes:
            print 'Sending at node ' + str(n)
            filename4 = open('node' + str(n), 'w+')
            filename4.write('Terminate SIG phase')
            filename4.close()
            udp_transmit.transmit(ips[n], udp_port+1, 'node' + str(n))
            # time.sleep(3)
            
        os.remove(filename)
        os.remove(filename3)
        
        print "Terminated this round!"
        

    
