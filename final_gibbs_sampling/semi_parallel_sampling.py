#############################################
### Script: fast_node_threading.py        ###
### Authors: K. Tsitseklis, G. Kakkavas   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################


import random
import numpy as np 
import math
import sys
import time
import local_energy
import itertools
from datetime import datetime
import vectors
from shutil import copyfile
import udp_receive
import udp_transmit
import rv
import os
import json
from scipy.stats import bernoulli



def read_new_info(filename, nodeList):
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
    winners = rv.k_mostCommonLines(lines,k)
    return winners


def get_new_vectors(winners):
    results = list()
    for w in winners:
        data = w.split(' * ')
        ID = int(data[0])
        affected = [int(ch) for ch in data[1] if ch != ' ' and ch!='\n']
        u_old = [int(ch) for ch in data[2] if ch != ' ' and ch!='\n']
        u_new = [int(ch) for ch in data[3] if ch != ' ' and ch!='\n']
        results.append([ID, affected, u_old, u_new])
    return results


def lst2str(alist):
    aStr = ''
    for i in alist:
        aStr = aStr + str(i) + ' '
    return aStr
    

def roulette_wheel_sel(population, probabilities):
    r = random.uniform(0,1)
    i = 0
    while (i < len(probabilities) and r > sum(probabilities[:i+1])):
        i = i + 1
    if i>len(probabilities):
        i = i-1    
    return population[i]


def roulette_wheel_sel2(population, probabilities):
    res = np.random.choice([reduce(lambda x, y: str(x) + str(y), p) for p in population], p=probabilities)
    res = [int(c) for c in res]
    print res, '--->', probabilities[population.index(res)]
    return res, probabilities[population.index(res)]


def local_conditional_numerator(T, TsU, GsU, GsA, GsN, myU, myA, myC, rs, u_prev):
    P_s_num = np.exp( -1/T * local_energy.energy_calc(TsU, GsU, GsA, GsN,   myU, myA, myC, rs, u_prev) )
    return P_s_num


def local_conditional_denumerator(T, TsU, GsU, GsA, GsN, myA, myC, rs, poss_u, u_prev): # Zs
    P_s_den = 0
    for u in poss_u:
        P_s_den += local_conditional_numerator(T, TsU, GsU, GsA, GsN, u, myA, myC, rs, u_prev)
    return P_s_den


def all_poss_u(a):
    num_channels = len(a)
    candidates = list()
    combinations = ["".join(seq) for seq in itertools.product("01", repeat=num_channels)]
    tmp = [int(c) for myStr in combinations for c in myStr]
    chunks = [tmp[x:x+ num_channels] for x in range(0, len(tmp), num_channels)]
    candidates = chunks[1:] # remove option [0, 0, 0, 0]

    return candidates
    

def temperature(sweep,c0):
    T = c0/math.log1p(1+sweep)
    return T


def draw_sample(T, TsU, GsU, GsA, GsN, myA, myC, rs, u_prev):
    prob_list = list()
    poss_u = all_poss_u(myA)
    Zs = local_conditional_denumerator(T, TsU, GsU, GsA, GsN, myA, myC, rs, poss_u, u_prev)
    for u in poss_u:
        P_s = local_conditional_numerator(T, TsU, GsU, GsA, GsN, u, myA, myC, rs, u_prev)/Zs
        prob_list.append(P_s)
    
    ## implementing roulette (c)
    samp = roulette_wheel_sel2(poss_u, prob_list)
    return samp


def gibbs_samp(ID, ips, sweeps, TsU, GsU, GsA, GsN, myA, myC, myU, rs, convergence_filename):
    nodeList = [int(x) for x in ips.keys()]
    Ts_nodes = [n[0] for n in TsU]
    Gs_nodes = [n[0] for n in GsU]
    prob = 0
    for w in range(1,sweeps+1):
        if (w != 1):
            winners = list()
            udp_receive.receive(ips[ID], 8000, '/root/total/final_gibbs_sampling/new_info.txt')
            winners = read_new_info('/root/total/final_gibbs_sampling/new_info.txt', nodeList)
            data = get_new_vectors(winners)
            for n_vectors in data:
                node_id = n_vectors[0]
                if node_id in Ts_nodes:
                    if n_vectors[2] != n_vectors[3]: # change has happened
                        index = TsU.index([node_id] + n_vectors[2]) # find index of u vector
                        TsU[index] = [node_id] + n_vectors[3] # replace new value
                if node_id in Gs_nodes:
                    if n_vectors[2] != n_vectors[3]: # change has happened
                        index = GsU.index([node_id] + n_vectors[2]) # find index of u vector
                        GsU[index] = [node_id] + n_vectors[3] # replace new value
                for j,node in enumerate([i[0] for i in GsN]):
                    if node in n_vectors[1]:
                        GsN[j] = [k-g for k,g in zip(GsN[j], [node_id] + n_vectors[2])] 
                        GsN[j] = [k+g for k,g in zip(GsN[j], [node_id] + n_vectors[3])] 
                
        T = temperature(w,2)
        tau = 0.2 # may need fine-tuning
        temp = bernoulli.rvs(tau, size=1)
        
        if (temp[0] == True):
            print "I will update my state!"
            u_star, prob = draw_sample(T, TsU, GsU, GsA, GsN, myA, myC, rs, myU)
        else:
            print "I will NOT update my state!"
            u_star = myU
            

        loc_energy = local_energy.energy_calc(TsU, GsU, GsA, GsN, u_star, myA, myC, rs, myU)
        c_f = open(convergence_filename,'a')
        c_f.write(str(w) + '    ' + lst2str(u_star) + '    ' +   str(round(loc_energy,3)) + '    ' + str(round(prob,3)) + '\n')
        c_f.close()
        print 'i picked u: ', u_star
        affected = Ts_nodes
        length = 6 + len(affected) + len(myU)*2
        MYstring = str(ID) + ' * ' + lst2str(affected) + '* ' + lst2str(myU) + '* ' + lst2str(u_star) + '* ' + str(length)
        myU = u_star
        if w!=1:
            os.remove('/root/total/final_gibbs_sampling/new_info.txt')
        f = open('/root/total/final_gibbs_sampling/new_info.txt', 'w+') ## must overwrite
        f.write(MYstring)
        f.write('\n\n')
        f.close()
        copyfile('/root/total/final_gibbs_sampling/new_info.txt','/root/total/final_gibbs_sampling/myNew_info.txt')
        mx = max(ips.keys()) #ID of controller
        time.sleep(1.9)
        udp_transmit.transmit(ips[mx], 8000+int(ID), '/root/total/final_gibbs_sampling/new_info.txt')
        os.remove('/root/total/final_gibbs_sampling/new_info.txt')

    return u_star
