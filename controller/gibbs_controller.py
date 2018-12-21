#! /usr/bin/env python2
#############################################
### Script: gibbs_controller.py           ###
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

##global counter
##counter = 0

def udp_listen(IP_address, udp_port, filename):           
    udp_receive.receive(IP_address, udp_port, filename) 
    global counter
    counter = counter + 1
    print 'Received'
    

if __name__ == '__main__':
    # usage: controller of gibbs sampling phase
    # also used to notify nodes that a phase is complete 

    #global counter
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
                temp = threading.Thread(target=udp_listen, args=[ips[controller_id], udp_port+i, filename, ])
                thread_array.append(temp)

            for t in thread_array:
                t.start()
                
            #global counter
            while (counter<num_nodes):
                pass
            
            # at this point all nodes have notified the controller of their  readiness(completion)
            
            time.sleep(0.01)        
            print "READY!!!"
            nodes = [i for i in ips.keys() if i != controller_id ]
            for n in nodes:
                print 'Sending at N1-' + str(n)
                filename2 = open('node' + str(n), 'w+')
                filename2.write('Node ' + str(n) + ' send!')
                filename2.close()
                udp_transmit.transmit(ips[n], udp_port, 'node' + str(n))
            print "Terminated iteration"
            
            for t in thread_array:
                t.join()
            
            #global counter
            counter = 0
            os.remove(filename)
