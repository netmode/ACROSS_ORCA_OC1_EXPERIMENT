#! /usr/bin/env python2

import sys
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
        

def getVectors(filename, nCh, nodeList):

    f = open(filename, 'r')
    lines = f.readlines()
    lines = [l for l in lines if l != '\n']
     
    nodesFound = list()
    for line in lines:
        if len(line.split()) != (nCh*4)+1:
            continue
        try:    
            n = int(line.split()[0])
            if n not in nodeList:
                continue
        except ValueError:
            continue
            
        if n not in nodesFound:
            nodesFound.append(n)
    k = len(nodesFound)
    
    winners = k_mostCommonLines(lines, k)
    
    A = list()
    N = list()
    C = list()
    U = list()     

    for w in winners:
        tmp = w.split()
        a = [tmp[0]]+tmp[1:nCh+1]
        A.append([int(i) for i in a])
        
        n = [tmp[0]]+tmp[nCh+1:2*nCh+1]
        N.append([int(i) for i in n])
        
        c = [tmp[0]]+tmp[2*nCh+1:3*nCh+1]
        C.append([float(i) for i in c])
        
        u = [tmp[0]]+tmp[3*nCh+1:4*nCh+1]
        U.append([int(i) for i in u])
    f.close()       
    return (winners, A, N, C, U)
        
        

if __name__ == '__main__':
    
    ##TESTING
    filename = sys.argv[1]
    nCh = int(sys.argv[2])
    nodeList = eval(sys.argv[3])
    getVectors(filename, nCh, nodeList)