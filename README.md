
# ACROSS ORCA Open Call 1

The provided code was implemented for the ACROSS experiment part of ORCA Open Call 1. It aimed at demonstrating the feasibility of the AuRoRA resource allocation framework based on Markov Random Fields for the first time in real cognitive radio topologies implemented via SDR.

## Getting Started

These instructions will get you a copy of the project up and running on [Universal Software Radio Peripheral (USRP)](https://www.ettus.com/) devices for development and testing purposes. 

### Prerequisites

In order to run the experiment you will need Python 2.7 environment with the following modules installed:

* netifaces
* scipy
* json

In order to install them you can run on your terminal the following command (on Debian based systems): 
```sudo apt install python-<name_of_package>```

Also, a recent version of GNU Radio open-source software development toolkit must be installed. For more installation details visit the following website (https://wiki.gnuradio.org/index.php/InstallingGR) 

It is also necessary to have access to the appropriate USRP devices with at least UHD driver version 3.13.



## Running the tests

In order to run our code please run the total_node.py script providing the proper ID for every node. Also, you need the following additional files in the same directory:

* <b> data.txt </b>: A text file with the data about to be transmitted. 

* <b> config.json </b>: A JSON configuration file containing all the experiments related parameters.  The config file specifies one (or more) experiment(s) and the transmissions in each round in the form of a list for every node. 

	A node about to transmit in round i sets the destination's ID in its transmission list in position i. The receiving node sets in the respective position the value -9. 

	For the relay operation, the transmission list must contain a list containing two numbers.  The first one is always a -9 and the second is the destination node's ID. 

	For the transceiver operation, the transmission list must contain a list containing two numbers. The first one is the destination node's ID and the second one is the value -9.

	For more information please refer to the README.md in SIG_exchange subfolder.

* <b> ipnet.json </b> : A JSON file containing all the nodes' IP addresses.
 
 Sample files of all the above categories are provided.
 
 <b><i> The provided code together with the auxiliary files are suited for direct deployment on ORBIT's Sandbox 4 with a square topology layout. To deploy in different execution environments new parametrization is required at the appointed places (see code comments and README files) </i> </b> 


### Auxiliary Scripts

* enable_usrp2.sh: Used in ORBIT Grid in order to enable the N210 USRPs
* reset_usrp.sh: Used to reset B205mini in ORBIT Grid when running on Ubuntu 16
* shuffle_config.py: Used to create more experiments by shuffling the original config.json


## Equally Contributing Authors

* <b> Grigoris Kakkavas </b>, gkakkavas@netmode.ntua.gr
* <b> Konstantinos Tsitseklis </b> , ktsitseklis@netmode.ntua.gr


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


