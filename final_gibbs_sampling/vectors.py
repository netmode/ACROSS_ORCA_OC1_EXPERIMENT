#from channel_energy import calc_energy
#import energy_based_decision as decision
from operator import add


## calc_energy returns the mean power of the channel
## energy_based_decision compares mean power with some thresholds to decide if the channel is empty, occupied by one node, or there is a colision
## there is 1-1 mapping between channesl and busy_tones_channels (where we broadcast corresponding busy tones)


def calc_vectorN(TsU):
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
        c_vector[i] = 0.98 * c_vector[i]
        if (u_vector[i]==1):
            channel_state = decision.is_empty(busy_tone_channels[i])
            if (channel_state==1):
                c_vector[i] = min (1, c_vector[i] + penalty)
            else:
                c_vector[i] = 0
    return c_vector
    

def calc_cost3(c_vector, channel_id, penalize, penalty=1):
    for i in range(0, len(c_vector)):
        c_vector[i] = 0.98 * c_vector[i]
        if (penalize):
            c_vector[channel_id] = min (1, c_vector[channel_id] + penalty)
        else:
            c_vector[channel_id] = 0
    return c_vector
