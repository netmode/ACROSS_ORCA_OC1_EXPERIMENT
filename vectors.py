#############################################
### Script: vectors.py                    ###
### Authors: K. Tsitseklis, G. Kakkavas   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################

import Collision_DET.energy_based_decision as decision
from operator import add


def calc_vectorN(TsU):
    """ Calculates the vector n of the node - does not return the real vector with values {0,1,2}, instead it counts all uses of each channel
        TsU: a list that contains the vectors u of the 1-hop neighbors """
    tmp = TsU[0]
    for i in range(1, len(TsU)):
        tmp = list( map(add, tmp, TsU[i]) )
    
    return tmp


def calc_cost(u_vector, c, busy_tone_channels, penalty, prize):
    #c = [0]*len(u_vector)
    for i in range(0, len(u_vector)):
        if (u_vector[i]==1):
            channel_state = decision.is_empty(busy_tone_channels[i])
            if (channel_state==0):
                c[i] = c[i] + prize
            else:
                c[i] = c[i] + penalty
    return c


def calc_cost2(u_vector, c_vector, busy_tone_channels, penalty=1):
    for i in range(0, len(u_vector)):
        c_vector[i] = 0.8 * c_vector[i]
        if (u_vector[i]==1):
            channel_state = decision.is_empty(busy_tone_channels[i])
            if (channel_state==1):
                c_vector[i] = min (1, c_vector[i] + penalty)
            else:
                c_vector[i] = 0
    return c_vector
    

def calc_cost3(c_vector, channel_id, penalize, penalty=1):
    """ updates the cost interference function of the node
        c_vector: the actual cost vector
        channel_id: the ID of the channel under examination
        penalize: boolean - indicates if there was a collision or not
        penalty: penalty value """
    for i in range(0, len(c_vector)):
        c_vector[i] = 0.8 * c_vector[i]
        if (penalize):
            c_vector[channel_id] = min (1, c_vector[channel_id] + penalty)
        else:
            c_vector[channel_id] = 0
    return c_vector


def cost_cooldown(c_vector):
    return [0.8*i for i in c_vector]


def calc_cost4(c_vector, col_channels, freq_tx_id_list, penalty=1):
    c_vector = [0.8*i for i in c_vector] #cooldown
   
    for index in freq_tx_id_list: #successful transmissions
        c_vector[index] = 0
   
    for index in col_channels: #collisions
        c_vector[index] = min (1, c_vector[index] + penalty)
    
    return c_vector
