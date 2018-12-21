
# Discovery Phase

This module is responsible for the discovery of each node's 1-hop neighborhood (transmission range). Generally it can be used in order to exchange any kind of information within this range. It returns a list with the info received from the neighbors.

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

In order to run this module the following are required:

* <b> ipnet.json </b> : A JSON file containing all the nodes' IP addresses.

The module can be executed by running the following command

``` python discovery.py ID node's_info controller's_IP gain    ```

Where:
* ID: A unique integer identifier for each node (set in ipnet.json)
*  node's_info: A text file containing the necessary information (for discovery it is the IP address)
* controller's_IP: The IP address of the controller
* gain: The gain used for the transmission, needs to be specified according to the environment
 
 Sample files of all the above categories are provided.
 
 <b><i> The provided code together with the auxiliary files are suited for direct deployment on ORBIT's Sandbox 4 . To deploy in different execution environments new parametrization is required for the receiving gain in the appropriate scripts (rx) </i> </b> 

## Equally Contributing Authors

* <b> Grigoris Kakkavas </b>, gkakkavas@netmode.ntua.gr
* <b> Konstantinos Tsitseklis </b> , ktsitseklis@netmode.ntua.gr


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
