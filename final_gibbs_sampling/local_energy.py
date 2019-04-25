#! /usr/bin/env python2
###########################################################
### Script: local_energy.py                             ###
### Authors: Aggeliki Chroni, G. Kakkavas, K Tsitseklis ###
### Licence: MIT                          #################
### Python version: Python 2.7            #################
###########################################################

import numpy as np

def first_potential(x,a,rs,l1=4,d1=500,A=2,B=-1,C=2,d=0):

    def sig(x,A,B,C,d, rs):
        return (A/(1+1*np.exp(-C*(x-d-rs)))) + B

    numAssignCh = sum(x)    #L1-norm 
    vect=[1]*len(x)        #create vector (1,1,1,1)
    # choose between different V1 potential functions, now is for sigmoid, for parabolic comment out next line.
    rs = 0
    if numAssignCh >=1 and np.inner(x,a) == np.inner(x,vect):
        return l1*(1-sig(numAssignCh,A,B,C,d,rs))
        #return l1*(numAssignCh-rs)**2
    else:
        return d1        # d1  high value

    
def second_potential(xs,cs,dictTsU,Gs,N,U,j,xj,aj,u_prev,l2=2,l3=2,d2=500): # called only for j in Gs
    
    def calc_nsk(u_prev, nk):
        nk = [x if x <= 1 else 2 for x in nk]
        tmp2 = [i-j for (i,j) in zip(nk, u_prev)]
        return [i if i <= 1 else 1 for i in tmp2]
    
    Ts = dictTsU.keys()
    if (j in Ts) and np.inner(xs,aj)!=0 and np.array_equal(np.bitwise_and(xs,aj),xs):
        return l2*np.inner(xs,xj) + l3*np.inner(xs,cs) 
    elif j not in Ts and j in Gs:    # ONLY for j in Gs
        # find summ
        summ = 0
        for k in Ts:
            nsk = calc_nsk(u_prev,N[k])
            summ = summ + np.inner(xs,nsk)
        numGswithoutTs = len(Gs) - len(Ts) 
        return (l2 * summ + l3 * np.inner(xs,cs) ) / numGswithoutTs
    else:
        return d2    #high value


def makeDictionary(list):
    dictionary = {}
    numCh = len(list[0])
    for t in list:
        dictionary[t[0]] = []
        for i in range(1,numCh):
            dictionary[t[0]].append(t[i])
    return dictionary


def energy_calc(TsU, GsU, GsA, GsN, myU, myA, myC, rs, u_prev):

    dictTsU = makeDictionary(TsU)

    dictGsU = makeDictionary(GsU)
    dictGsA = makeDictionary(GsA)
    dictGsN = makeDictionary(GsN)

    v1 = first_potential(myU,myA,rs)
    local_energy = v1 + sum(second_potential(myU,myC,dictTsU,dictGsU.keys(),dictGsN,dictGsU,j,dictGsU[j],dictGsA[j],u_prev) for j in dictGsU.keys())

    return local_energy