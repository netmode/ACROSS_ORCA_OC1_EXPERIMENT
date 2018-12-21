#############################################
### Script: avg.py                        ###
### Authors: K. Tsitseklis, G. Kakkavas   ###
### Licence: MIT                          ###
### Python version: Python 2.7            ###
#############################################

import scipy


def find_average(filename):
    """ Returns the mean and average of the received signal energy
        filename: the file that contains the measurements """
    
    avg = []
    f = scipy.fromfile(open(filename), dtype=scipy.float32)
    n = int(len(f)/1024)

    for i in range(0, n):
        #calculate the average of every 1024 block - we use 1024 FFT
        avg.append(sum(f[i*1024:i*1024+1024])/1024)

    # calculate mean
    mu = sum(avg)/len(avg)
    # calculate variance
    sigma = sum((xi - mu) ** 2 for xi in avg) / len(avg)

    return (mu, sigma)