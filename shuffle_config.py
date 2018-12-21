import json
import sys
import random
from copy import deepcopy

if __name__=='__main__':
    
    nodes = eval(sys.argv[1])
    number_of_exp = eval(sys.argv[2])
    
    with open("config.json") as jsonfile:
        exp_dict = json.load(jsonfile)
        experiments = exp_dict['experiments']
    
    channel_list = experiments[0]['channel_list']
    transmission_list = list()
    for n in nodes:
        trans_list = 'trans_list_'+str(n)
        transmission_list.append(experiments[0][trans_list])
    
    print transmission_list    
    
    
    for exper in range(1,number_of_exp+1):
        temp = zip(*transmission_list)
        temp2 = deepcopy(experiments[0])
        random.shuffle(temp)
        new_tr = list()
        for i in range(0,len(nodes)):
            new_tr.append([l[i] for l in temp])
            
        for n,i in enumerate(new_tr):
            trans_list = 'trans_list_' + str(nodes[n]) 
            temp2[trans_list] = i
        print new_tr
        
        number_of_channels = random.randint(2,len(channel_list))
        print "Num of channels = ", number_of_channels
        temp2['channel_list'] = sorted(random.sample(channel_list,number_of_channels))
        temp2['a/a'] = exper + 1
        temp2['sweeps'] = number_of_channels*10
        experiments.append(temp2)
        #print temp2, '\n'
        #print experiments[0], '\n'
        
    #print experiments
        
    with open('new_config.json','w') as outfile:
        json.dump(exp_dict,outfile)
