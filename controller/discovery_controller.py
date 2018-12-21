#! /usr/bin/env python2
#############################################
### Script: discovery_controller.py       ###
### Authors: K. Tsitseklis, G. Kakkavas   ###
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

    f = open(filename, 'r')

    for line in f:
        # Node _ is ready!
        try:
            n = int(line.split()[1])
        except:
            continue

        if n not in nodes:
            nodes.append(n)

    return nodes


if __name__ == '__main__':
    # usage: controlls the discovery phase by telling each node when it is time to transmit
    # and notifying all nodes when the phase is complete

    if (len(sys.argv)!=5):
        print "Please specify the arguments in the order specified below"
        print "controller's IP address, port to listen to, temp_file1, temp_file2"
    else:
        with open('/root/total/ipnet.json') as jf:
            diction = json.load(jf)    
            ips = diction['net']
        
        ips = {int(x): y.encode('utf8') for x,y in ips.items()}

        IP_address = sys.argv[1]
        udp_port = eval(sys.argv[2])
        filename = sys.argv[3]
        filename3 = sys.argv[4]
        
        while (1):
            nodes = list()
            while len(nodes) < len(ips.keys())-1:
                print "RECEIVING!"
                udp_receive.receive(IP_address, udp_port, filename)
                nodes = check_file(nodes, filename)
                print nodes

            print "ALL nodes are ready!"

            # idle time varies according to number of nodes and execution environment
            time.sleep(3)
            for n in nodes:
                print 'Sending at node ' + str(n)
                filename2 = open('node' + str(n), 'w+')
                filename2.write('Node ' + str(n) + ' send!')
                filename2.close()
                print "Sending at:", ips[n], udp_port
                #print "size of file to send is ", os.stat('node'+str(n)).st_size
                udp_transmit.transmit(ips[n], udp_port, 'node' + str(n))
                # node notifies the receiver that it has completed its transmission
                udp_receive.receive(IP_address, udp_port, filename3)

            # reaching this point all nodes have broadcasted their information
            print "Signaling Broadcasting terminated!"
            
            for n in nodes:
                print 'Sending at node ' + str(n)
                filename4 = open('node' + str(n), 'w+')
                filename4.write('Phase has been completed')
                filename4.close()
                # each node receives a text file in a specific port that means that phase is complete
                udp_transmit.transmit(ips[n], udp_port+1, 'node' + str(n))
                # time.sleep(3)

            # auxiliary files are removed so they do not consume memory space    
            os.remove(filename)
            os.remove(filename3)
            
            print "Terminated iteration"
        

    
