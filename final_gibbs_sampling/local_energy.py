#! /usr/bin/env python2
###########################################################
### Script: local_energy.py                             ###
### Authors: Aggeliki Chroni, G. Kakkavas, K Tsitseklis ###
### Licence: MIT                          #################
### Python version: Python 2.7            #################
###########################################################

import numpy as np

def first_potential(x,a,rs,l1=2,d1=500,A=2,B=-1,C=2,d=0):

    def sig(x,A,B,C,d, rs):
        return (A/(1+1*np.exp(-C*(x-d-rs)))) + B

    numAssignCh = sum(x)    #L1-norm 
    vect=[1]*len(x)        #create vector (1,1,1,1)

    if numAssignCh >=1 and np.inner(x,a) == np.inner(x,vect):
        return l1*(1-sig(numAssignCh,A,B,C,d,rs))
    else:
        return d1        # d1  high value

    
def second_potential(xs,cs,dictTsU,Gs,N,U,j,xj,aj,l2=3,l3=5,d2=500): # called only for j in Gs
    
    def calc_nsk(us, nk, uk):
        nk = [x if x <= 1 else 2 for x in nk]
        tmp = [i+j if (i+j) <= 2 else 2 for (i,j) in zip(nk, uk)] # calc (nk + uk - us)
        tmp2 = [i-j for (i,j) in zip(tmp, us)]
        return [i if i <= 1 else 1 for i in tmp2]
    
    Ts = dictTsU.keys()
    if (j in Ts) and np.inner(xs,aj)!=0:
        return l2*np.inner(xs,xj) + l3*np.inner(xs,cs) 
    elif j not in Ts :    # ONLY for j in Gs
        # find summ
        summ = 0
        for k in Ts:
            nsk = calc_nsk(xs,N[k],U[k])
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


def energy_calc(TsU, GsU, GsA, GsN, myU, myA, myC, rs):

    dictTsU = makeDictionary(TsU)

    #Ts = dictTsU.keys()        #Ts = [2,3]

    dictGsU = makeDictionary(GsU)
    dictGsA = makeDictionary(GsA)
    dictGsN = makeDictionary(GsN)
    #dictGsC = makeDictionary(GsC)

    local_energy = first_potential(myU,myA,rs) + sum(second_potential(myU,myC,dictTsU,dictGsU.keys(),dictGsN,dictGsU,j,dictGsU[j],dictGsA[j]) for j in dictGsU.keys())

    return local_energy



if __name__ == '__main__':

    # usage: calculate the local energy of the node 
    # by computing first and second order potentials
    # by running this main script an example output is
    # produced 
    myU = [0,0,1,0]
    GsU = [ [1,0,0,0,1], [3,0,1,0,0], [4, 0, 1, 0, 0] ]
    TsU = [ [1,0,0,0,1], [3,0,1,0,0] ]
    GsA = [ [1,0,1,1,1], [3,0,1,1,1], [4,1,1,1,1] ]
    GsN = [ [1,0,0,1,0], [3,0,1,1,0], [4,0,1,0,0] ]
    myC = [0,0,1,0.2]
    myA = [0,1,1,1]
    # make dictionaries with key id
    local_energy = energy_calc(TsU, GsU, GsA, GsN, myU, myA, myC)

    print local_energy
