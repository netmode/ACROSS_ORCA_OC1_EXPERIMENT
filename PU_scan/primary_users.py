import PU_transmit
import udp_receive
import os
import random
import sys
import socket

if __name__ == '__main__':
    
    #usage: PU executes this script, it chooses at random a channel and starts transmitting at this channel for up to countdown slots
    channel_list = eval(sys.argv[1])
    gain = eval(sys.argv[2])
    sec = eval(sys.argv[3])
    #f = open('/root/total/PU_scan/PU_log.txt', 'a')
    myIP = socket.gethostbyname(socket.gethostname())

    countdown = random.randint(1,3)
    chosen_channel = random.sample(channel_list,1)[0] #choose a channel

    iteration= 0

    while 1:
        udp_receive.receive(myIP, 14000, 'empty.txt')
        os.remove('empty.txt')
        samp = random.uniform(0,1)
        print "Round: ", iteration
        print "Countdown: ", countdown
        f = open('/root/total/PU_scan/PU_log.txt', 'a')
        f.write('Round: ' + str(iteration) + ' ')
        if samp < 0.6:
            if (countdown <=0):
                chosen_channel = random.sample(channel_list,1)[0] #choose a channel
                countdown = random.randint(1,3)
            print "I am transmitting at channel: ", chosen_channel
            print "Chosen channel: ", chosen_channel
            f.write("Chosen_channel_id: " + str(channel_list.index(chosen_channel)))
            PU_transmit.transmit(chosen_channel, 'input.txt', gain, sec)
            print "I terminated my transmission!"
        countdown = countdown - 1
        f.write('\n')
        iteration = iteration + 1
        f.close()

