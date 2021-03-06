#! /usr/bin env python2

#############################################
### Script: total_node.py                 ###
### Authors: G. Kakkavas, K. Tsitseklis   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################


import os
import sys
import time
import random
import json
import socket
from datetime import datetime
import PU_scan
import Collision_DET as CD
import final_gibbs_sampling as GIBBS
import SIG_exchange as syn
import vectors
import discovery_phase.discover
import netifaces as ni
from shutil import copyfile



def negotiate_rx(ip_addr, channel_list):
    print "Negotiating receiving channel"
    
    GIBBS.udp_receive.receive(ip_addr, 9999 , '/root/total/freq.txt')
    copyfile('/root/total/freq.txt', '/root/total/freq_backup.txt')
    f_file = open('/root/total/freq.txt')
    lines = f_file.readlines()
    f_file.close()
    common_lines = syn.rv.k_mostCommonLines(lines, 1)
    element = common_lines[0]
    chosen_channel = channel_list[int(element.split()[3])]
    previous = int(element.split()[1])
    sender = int(element.split()[2])
    os.remove('/root/total/freq.txt')
    return previous, sender, chosen_channel


def negotiate_tx(ip_dest, ID, dest, u, sender=None):
    print "Negotiating transmitting channel"
    
    avail_ch =  [i for i, x in enumerate(u) if x == 1]
    chosen_channel_id = random.choice(avail_ch)
    f = open('/root/total/freq.txt', 'w+')
    if not sender:
        sender = ID
    f.write(str(dest) + ' ' +  str(ID) + ' ' + str(sender) + ' ' + str(chosen_channel_id) + '\n')
    f.close()
    time.sleep(4)
    GIBBS.udp_transmit.transmit(ip_dest, 9999 , '/root/total/freq.txt')

    os.remove('/root/total/freq.txt')
    
    return chosen_channel_id
    
def clear2send(ips, sender, freq_rx, bandwidth, collisions):
    #update_cost = False
    #CD.channel_energy.energy_measurements(freq_rx, bandwidth)
    #mu, _ = CD.avg.find_average('/root/total/mean_power.txt')
    #os.remove('/root/total/mean_power.txt')
    #val = CD.energy_based_decision.is_empty(mu)
    #if val==1:
        #collisions = collisions + 1
        #update_cost = True
    # SEND ACK TO TRANSMITTER IN PORT 9000
    print "i am in clear2send"
    with open('/root/total/bar.txt', 'w+') as f:
        #if update_cost:
            #f.write("Collision!\n\n")
        #else:
            #f.write("Start transmitting!\n\n")
        f.write('Start trasmission!\n\n')
    GIBBS.udp_transmit.transmit(ips[sender], 9000, '/root/total/bar.txt')
    os.remove('/root/total/bar.txt')

    #return collisions


def list_to_str(lst):
    val = ''
    for i in lst:
        val = val + ' ' + str(i)
    return val


def wait_ack(ips, ID):
    print "i am in wait_ack"
    # wait for ack from final destination
    GIBBS.udp_receive.receive(ips[ID], 9000, '/root/total/foo.txt')
    #f2 = open('/root/total/foo.txt', 'r')
    #info = f2.readlines()
    #f2.close()
    #os.remove('/root/total/foo.txt')
    #info = [i for i in info if i != '\n'] # remove empty lines
    #info_line = syn.rv.k_mostCommonLines(info,1)
    #penalize = False
    #if info_line[0].rstrip() == 'Collision!':
        #penalize = True
    # We assume that a node calculates cost function only when it is a transmitter
    #return penalize

def choose_channel(ID, ips, sweeps, controller_id, channel_list, my_last_known_vectors, last_known_neigh_vectors, gain_tx, gain_rx, rs, convergence_filename):

    C_old = my_last_known_vectors[2]
    U_old = my_last_known_vectors[3]
    TU = last_known_neigh_vectors[0]
    GA = last_known_neigh_vectors[1]
    GN = last_known_neigh_vectors[2]
    GU = last_known_neigh_vectors[3]
    sec = 1

    # PU SCAN - CALCULATE VECTOR MY A
    myA = PU_scan.availability.scan(channel_list, 1, gain_rx)
    print "My availability vector:", myA
    print "Exchange a in Ts"
    # must exchange myA with neighbors for correct energy calc
    neighAs = discovery_phase.discover.exchange_info(ID, myA, ips[controller_id], gain_tx, 12000)
    print "Finished exchanging" 
    
    for a_str in neighAs:
        a_str = a_str.split()
        ID_neighbor = int(a_str[0])
        a = [int(i) for i in a_str[1]]
        indexes = [i[0] for i in GA]
        index = indexes.index(ID_neighbor)
        GA[index] = [ID_neighbor] + a
    
    # GIBBS SAMPLING
    myU = GIBBS.sequential_sampling.gibbs_samp(ID, ips, sweeps, TU, GU, GA, GN, myA, C_old, U_old, rs, convergence_filename)
    
    tmp = discovery_phase.discover.exchange_info(ID, myU, ips[controller_id], gain_tx, 12000)  # instead of ip send u_vector
    TU_new = list()
    for z in tmp:
        vec = [int(z.split()[0])]
        for zi in z.split()[1]:
            if zi != ' ' and zi != '\n':
                vec.append(int(zi))
        TU_new.append(vec)
    print "TU IS ... ", TU_new

    # CALCULATE VECTOR N BASED ON NEW SELECTIONS OF CHANNELS
    TU2 = [el[1:] for el in TU_new]  # REMOVE ID FROM EVERY NODE
    print TU2
    myN = vectors.calc_vectorN(TU2)  # DOES NOT RETURN REAL N {0,1,2}

    # BROADCAST SIGNALING
    # CREATE FILE vectorsSend for transmission
    tmp = str(ID) + list_to_str(myA+myN+C_old+myU) + '\n'  
    f = open('/root/total/vectorsSend.txt', 'w')
    f.write(tmp)
    f.write('\n')
    f.close()
    #copyfile('/root/total/vectorsSend.txt', '/root/total/tsitse.txt')

    new_neigh_vectors = syn.node_threading.exchange(ID, '/root/total/vectorsSend.txt', len(channel_list), gain_tx, sec)  # RADIO EXCHANGE IN CONTROL CHANNEL

    my_new_vectors = [myA, myN, C_old, myU]

    return (my_new_vectors, new_neigh_vectors)


def neigh_initialization(ID, neigh, my_vectors):
    a = my_vectors[0]
    n = my_vectors[1]
    c = my_vectors[2]
    u = my_vectors[3]

    myStr = (str(ID) + ' ' + GIBBS.sequential_sampling.lst2str(a) + GIBBS.sequential_sampling.lst2str(n)+ GIBBS.sequential_sampling.lst2str(c) + GIBBS.sequential_sampling.lst2str(u))
    f = open('dataSend_init.txt', 'w+')
    f.write(myStr[:-1])
    f.write('\n\n')
    f.close()

    TU, _, _, _, _ = GIBBS.fast_node_threading.exchange(ID, 'dataSend_init.txt', len(u), neigh)

    tsU = [l[1:] for l in TU]  # remove ID from vectors
    # this is the correct N according to the U selection of neighbors
    myN = vectors.calc_vectorN(tsU)

    f = open('dataSend_init2.txt', 'w+')
    myStr = (str(ID) + ' ' + GIBBS.sequential_sampling.lst2str(a) + GIBBS.sequential_sampling.lst2str(myN)
                    + GIBBS.sequential_sampling.lst2str(c) + GIBBS.sequential_sampling.lst2str(u))
    f.write(myStr[:-1])
    f.write('\n\n')
    f.close()

    TU, GA, GN, _, GU = GIBBS.fast_node_threading.exchange(ID, 'dataSend_init2.txt', len(u), neigh)
    
    return (myN, TU, GA, GN, GU)


def mrf(incr, transmission_list, ID, sweeps, controller_id, controller_ip, channel_list, busy_tones):

    # transmission_list[i] in range of nodes (i.e. 3-6) means send to that node
    # transmission_list[i] == -1, neither send nor receive
    # transmission_list[i] == -9, receive by someone
    res_f = open('results'+ str(ID)+'.txt','a')
    gain_rx = 15
    gain_tx = 23
    myIP = ni.ifaddresses('eth1')[ni.AF_INET][0]['addr']
    tmp = discovery_phase.discover.exchange_info(ID, myIP, controller_ip, gain_tx, 12000)  
    neigh = list()
    n_ids = list()
    for z in tmp:
        lin = z.split()
        neigh.append(lin[1])
        n_ids.append(lin[0])
    print "Neighborhood of node: ", n_ids
    res_f.write('Neighborhood: ' + str(n_ids) + '    ')
    res_f.close()
    with open('ipnet.json') as jsonfile:  
        ipnet_dict = json.load(jsonfile)
        ips = ipnet_dict['net']
    
        
    ips = {int(x): y.encode('utf8') for x,y in ips.items()} 

    # INITIALISATION
    collisions = 0  # log number of collisions that take place when you are receiving
    bandwidth = 10e6  # THE SAME FOR ALL CHANNELS
    
    control_channel = 3400e6
    duration = 1  # This is the duration of the data transmission slot
    c_duration = 1  # This is the duration of the control transmissions

    #myA = PU_scan.PU_availability.availability(channel_list, 50)
    myA = [1]*len(channel_list)
    print "INITIALISATION"
    # dummy, will be corrected after getting neighbors U
    myN = [random.sample([0, 1, 2], 1)[0] for i in range(len(channel_list))]
    myC = [0]*len(channel_list)
    myU = [0]*len(channel_list)
    index = random.randint(0, len(channel_list)-1)
    myU[index] = 1
    my_vectors = [myA, myN, myC, myU]
    # USE NODE_INITIALIZATION TO GET NEIGHBORS VECTORS
    myN, TU, GA, GN, GU = neigh_initialization(ID, neigh, my_vectors)
    neigh_vectors = [TU, GA, GN, GU]
    my_vectors[1] = myN  # correct myN

    for gyros, dest in enumerate(transmission_list):
        ## wait until controller clears you out
        convergence_filename = 'convergence_' + str(incr) + '_' + str(ID) + '_' + str(gyros) + '.txt'
        convergence_f = open(convergence_filename, 'w') 
        convergence_f.write('Sweep       u drawn         energy         probability\n')
        convergence_f.close()         
        res_f = open('results'+ str(ID)+'.txt','a')
        res_f.write('exp_id: '+ str(incr) + ' ' + 'round: ' + str(gyros) + ' ')
        if dest==-9:
            role = 'rx'
            rs = 0
        elif dest==-1:
            role = 'none'
            rs = 0
        elif type(dest) == list and -9 in dest:
            role = 'relay' if dest[0] == -9 else 'tx/rx'
            rs = 1
        elif type(dest)== list:
            role = 'multi-tx'
            rs = len(dest)
        else:
            role = 'tx'
            rs = 1
        #rs = rs
        res_f.write('role: ' + role + ' ')
        if gyros != 0:
            GIBBS.udp_receive.receive(ips[ID], 14000, 'empty.txt')
            os.remove('empty.txt')
        t1 = datetime.now()
        my_vectors, neigh_vectors = choose_channel(ID, ips, sweeps, controller_id, channel_list, my_vectors, neigh_vectors, gain_tx, gain_rx, rs, convergence_filename)
        elapsed_t = datetime.now() - t1
        u = my_vectors[3]
        res_f.write('a: ' + str(my_vectors[0]) + ' ' + 'u: ' + str(u) + ' ' + 'assign_time: ' + str(elapsed_t) + ' ')
        if type(dest) == list and -9 in dest:
            time.sleep(random.uniform(0.1,1))
            # should open transceiver, must do two things at the same time
            if dest[0] == -9:   # node acts as an intermediate (multihop)
                previous, sender, freq_rx = negotiate_rx(ips[ID], channel_list)
                freq_rx_id = channel_list.index(freq_rx)
                u2 = u[:]
                if (sum(u) > 1):
                    u2[freq_rx_id] = 0
                freq_tx_id = negotiate_tx(ips[dest[1]], ID, dest[1], u2, sender) #for collision detection - find original sender
                freq_tx = channel_list[freq_tx_id]
                #sender, freq_rx = negotiate_rx(ips[ID],channel_list)
                print "i am going to receive at freq ", freq_rx
                print "i am going to send at freq ", freq_tx
                #penalize = wait_ack(ips, ID)
                wait_ack(ips, ID)
                #my_vectors[2] = vectors.calc_cost3(my_vectors[2], freq_tx_id, penalize) 
    
                # send clear to original source
                # time.sleep(random.randint(1,10)) # min:1sec max:10sec
                #freq_rx_id = channel_list.index(freq_rx)
                #collisions = clear2send(ips, sender, freq_rx, bandwidth, collisions)
                clear2send(ips, previous, freq_rx, bandwidth, collisions)
                print "Repeater is set to ", gain_tx          
                res_f.write('source: ' + str(sender) + ' destination: ' + str(dest[1]) + ' rx/tx_channel_id: ' + str(freq_rx_id) + '/' + str(freq_tx_id) + ' ') 
                #res_f.write('collisions: ' + str(collisions) + ' ')
                rec_file = '/root/total/data' + str(incr) +str(gyros) +'.txt'
                bts = syn.radio_repeater.repeat(freq_tx, freq_rx, duration, 60, rec_file)
                res_f.write('data transfered: ' + str(bts) + ' ')
            else:
                # receive and send at the same time (no multihop)
                previous, sender, freq_rx = negotiate_rx(ips[ID],channel_list)
                freq_rx_id = channel_list.index(freq_rx)
                u2 = u[:]
                if (sum(u) > 1):
                    u2[freq_rx_id] = 0
                freq_tx_id = negotiate_tx(ips[dest[0]], ID, dest[0], u2)
                freq_tx = channel_list[freq_tx_id]
                #sender, freq_rx = negotiate_rx(ips[ID],channel_list)
                #freq_rx_id = channel_list.index(freq_rx)
                #penalize = wait_ack(ips, ID)
                wait_ack(ips, ID)
                #my_vectors[2] = vectors.calc_cost3(my_vectors[2], freq_tx_id, penalize) 
                #time.sleep(random.uniform(0,6)) # min:1sec max:6sec
                #collisions = clear2send(ips, sender, freq_rx, bandwidth, collisions)
                clear2send(ips, previous, freq_rx, bandwidth, collisions)
                rec_file = '/root/total/data' + str(incr) +str(gyros) +'.txt'
                res_f.write('source: ' + str(sender) + ' destination: ' + str(dest[0]) + ' rx/tx_channel_id: ' + str(channel_list.index(freq_rx)) + '/' + str(freq_tx_id) + ' ') 
                #wait4Pu(channel_list,freq_tx_id)
                syn.transceiver.transceive(freq_tx, freq_rx, '/root/total/data.txt', rec_file, duration)
                #res_f.write('collisions: ' + str(collisions) + ' ')
                bts = os.stat(rec_file).st_size
                res_f.write('data transfered: ' + str(bts) + ' ')
            chosen_channel_id = freq_tx_id #this is done for the collisions if statement
            chosen_channel = freq_rx #this is done for the collisions if statement
        elif (type(dest) == list): #multi destination transmission
            # receive clear2send from all destinations
            freq_tx_list = list()
            freq_tx_id_list = list()
            u2 = u[:]
            for i in range(len(dest)):
                chosen_channel_id = negotiate_tx(ips[dest[i]], ID, dest[i], u2)
                if sum(u2)>1:
                    u2[chosen_channel_id] = 0
                    extra_channel = -1      
                elif  sum(u2)==1 and i!=len(dest)-1:
                    extra_channel = chosen_channel_id
                freq = channel_list[chosen_channel_id]
                freq_tx_list.append(freq)
                freq_tx_id_list.append(chosen_channel_id)
                wait_ack(ips, ID)
                
            res_f.write('destination: ' + str(dest) + ' ' + 'chosen_channel_ids: ' + str(freq_tx_id_list) + ' ')
            time.sleep(random.uniform(0.5,1))
            syn.multi_transmit.transmit(freq_tx_list, '/root/total/data.txt', duration, gain_tx)
        elif (dest == -9):  # you are a receiver in this round
            #update_cost = False  # flag to inform sender about collision
            # listen for receiving freq (chosen by transmitter) at control channel
            previous, sender, chosen_channel = negotiate_rx(ips[ID],channel_list)

            res_f.write('source: ' + str(sender) + ' ' + 'chosen_channel_id: ' + str(channel_list.index(chosen_channel)) + ' ')    
            # Wait a random interval so that transmissions do not coincide and there is a chance to detect collisions
            #time.sleep(random.uniform(0,6)) # min:1sec max:10sec
            #collisions = clear2send(ips, sender, freq_rx, bandwidth, collisions)
            clear2send(ips, previous, chosen_channel, bandwidth,  collisions)
            #res_f.write('collisions: ' + str(collisions)+ ' ')
            # open receiver for data receiving
            rec_file = '/root/total/data' + str(incr) + str(gyros) +'.txt'
            print "i am waiting at channel ", chosen_channel
            syn.simple_radio_receive.receive(chosen_channel, rec_file, duration, gain_rx)
            bts = os.stat(rec_file).st_size
            res_f.write('data transfered: ' + str(bts) + ' ')
        elif (dest == -1):
            pass
        else: # you are a transmitter in this round
            # choose the channel to communicate and send it to receiver
            chosen_channel_id = negotiate_tx(ips[dest], ID, dest, u)
            freq = channel_list[chosen_channel_id]
            res_f.write('destination: ' + str(dest) + ' ' + 'chosen_channel_id: ' + str(chosen_channel_id) + ' ')
            #penalize = wait_ack(ips, ID)
            wait_ack(ips, ID)
            time.sleep(random.uniform(0.5,1))#penalize = wait_ack(ips, ID)
            # We assume that a node calculates cost function only when it is a transmitter
            #my_vectors[2] = vectors.calc_cost3(my_vectors[2], chosen_channel_id, penalize) 
            # data.txt must contain some unique identifier for testing purposes
            #if (freq>1e9):
            #    syn.simple_radio_transmit.transmit(freq,'/root/total/data.txt', duration, 60) ### ACTUAL TRANSMISSION OF DATA
            #else:
            #wait4Pu(channel_list,chosen_channel_id)
            syn.simple_radio_transmit.transmit(freq,'/root/total/data.txt', duration, gain_tx) 
        
        # check if collisions happened 
        
        if (type(dest) == list and -9 not in dest):
            busy_tones_list = [busy_tones[id] for id in freq_tx_id_list]
            syn.multi_receive.receive(busy_tones_list, '/root/total/coll_info.txt', 2.5, gain_rx)
            f = open('/root/total/coll_info.txt', 'r')
            info = f.readlines()
            f.close()
            os.remove('/root/total/coll_info.txt')
            clean_info = list(set(info))
            col_channels = list()
            for i in range(len(dest)):
                if 'Collision in ' + str(freq_tx_id_list[i]) + '\n' in clean_info:
                    col_channels.append(freq_tx_id_list[i])
            if extra_channel>-1:
                col_channels.append(extra_channel)
                collisions = collisions + 1
                res_f.write('COLLISION ')
            my_vectors[2] = vectors.calc_cost4(my_vectors[2], col_channels, freq_tx_id_list)

        else:
            if ((type(dest)!=list) and dest>-1) or (type(dest)==list): #transmitter (simple and combined)
                print "I am receiving at ", busy_tones[chosen_channel_id]
                syn.busy_receiver.receive(busy_tones[chosen_channel_id], '/root/total/coll_info.txt', 2.5, gain_rx)
                f = open('/root/total/coll_info.txt', 'r')
                info = f.readlines()
                print "info: ", info
                f.close()
                os.remove('/root/total/coll_info.txt')
                if 'Collision!\n' in info:
                    print "There was a collision"
                    #collisions = collisions + 1
                    # inform collision vector
                    my_vectors[2] = vectors.calc_cost3(my_vectors[2], chosen_channel_id, True)
                else:
                    my_vectors[2] = vectors.calc_cost3(my_vectors[2], chosen_channel_id, False)   
                #res_f.write('collisions: ' + str(collisions)+ ' ')        
            if (dest == -9) or (type(dest)==list): #receiver (simple or combined)
                f = open(rec_file, 'r')
                info = f.readlines()
                f.close()
                temp_list = []
                for s in info:
                    s2  = [int(x) for x in s.split() if x.isdigit()]
                    temp_list = temp_list + s2
                set_of_ids = set(temp_list) 
                print "set_of_ids = ", set_of_ids
                print "sender  = ", sender
                
                if (len(set_of_ids)>1) or (len(set_of_ids)==1 and set_of_ids.pop()!=sender):
                    f = open('/root/total/coll_info2.txt','w')
                    print "Collision"
                    collisions = collisions + 1
                    f.write('Collision!\n')
                    res_f.write('COLLISION ')
                    #time2sl = 0.1
                #else:
                #    print "OK!"
                #    f.write('OK!\n')
                #    time2sl = 0.4
                #    time.sleep(random.uniform(time2sl,time2sl+0.15))
                    f.close()
                    syn.simple_radio_transmit.transmit(busy_tones[channel_list.index(chosen_channel)], '/root/total/coll_info2.txt', 1.5, gain_tx)            
                    os.remove('/root/total/coll_info2.txt')
                if (type(dest) != list):
                    my_vectors[2] = vectors.cost_cooldown(my_vectors[2])
            if dest==-1:
                my_vectors[2] = vectors.cost_cooldown(my_vectors[2])


        print "My c vector is: ", my_vectors[2]
        res_f.write('c: ' + str(my_vectors[2]) + ' ')
        ## tell controller you finished this round
        tmpf = open('ready.txt', 'w+')
        tmpf.write('I finished this round!\n')
        tmpf.close()
        GIBBS.udp_transmit.transmit(controller_ip, 14000+ID, 'ready.txt')
        os.remove('ready.txt')
        res_f.write('\n')
        res_f.close()
    print "Collisions Detected by this node", collisions
   


if __name__ == '__main__':
    
    # transmission_list = [4, 4, -1, -9, -1, -1] # hardcoded at first, different for each node.
                                               # number in range of nodes means transmit there. -1 do nothing, -9 receive.
    ID = eval(sys.argv[1])
    trans_list = 'trans_list_'+str(ID)
    with open("config.json") as jsonfile:
        exp_dict = json.load(jsonfile)
        experiments = exp_dict['experiments']
    t1 = datetime.now()
    for exper in range(0,len(experiments)):
        incr = experiments[exper]['a/a']
        sweeps = experiments[exper]['sweeps']
        controller_id = experiments[exper]['controller_id']
        controller_ip = experiments[exper]['controller_ip'].encode('utf8')
        channel_list = experiments[exper]['channel_list']
        busy_tones = experiments[exper]['busy_tones']
        transmission_list = experiments[exper][trans_list]
        #window = (experiments[exper]['window'])
        #rs_list = []
        #for i in range(0,len(transmission_list),window):
        #    r = 0
        #    unique = list()
        #    for j in transmission_list[i:i+window]:
        #        if j>0 and j not in unique:
        #            unique.append(j)
        #   r= len(unique)
        #    rs_list.append(r)    
        mrf(incr, transmission_list, ID, sweeps, controller_id, controller_ip, channel_list, busy_tones) 
        print "=========================END OF EXPERIMENT ================================================"
        time.sleep(1)
    print "Time Elapsed: ", datetime.now()-t1

