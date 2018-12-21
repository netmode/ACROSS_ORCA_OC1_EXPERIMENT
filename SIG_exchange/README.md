
# SIG_exchange

This module contains scripts used for the signaling exchange of all the nodes' vectors inside Gs. It can be also used for the exchange of any kind of information between nodes. 

## Getting Started

These instructions will get you a copy of the module up and running on [Universal Software Radio Peripheral (USRP)](https://www.ettus.com/) devices for development and testing purposes. 

### Prerequisites


In order to run the experiment you will need Python 2.7 environment with the following modules installed:

* json

Also, a recent version of GNU Radio open-source software development toolkit must be installed. For more installation details visit the following website (https://wiki.gnuradio.org/index.php/InstallingGR) 

It is also necessary to have access to the appropriate USRP devices with at least UHD driver version 3.13.


## Running the tests
In order to run this module please run node_threading.py . Also, you need the following additional file:

* <b> ipnet.json </b> : A JSON file containing all the nodes' IP addresses.

The module can be executed by running the following command

``` python  node_threading.py ID vectorsSend nCh gain    ```

Where:
* ID: A unique identifier for each node specified in ipnet.json
* vectorsSend: A text file containing the vectors of the particular node (proper format)
* nCh: The total number of channels
* gain: Tx gain for radio transmissions

It returns a  tuple containing 4 lists.
* List of vectors u in Ts
* List of availabilty vectors (a) in Gs
* List of vectors n in Gs
* List of vectors u in Gs 

Also in this module scripts used for the implementation of node's different radio operation is provided (receiving, relay, transceiving, etc)

 <b><i> The provided code is suited for direct deployment on ORBIT's Sandbox 4 . To deploy in different execution environments new parametrization is required for the receiving gain in the appropriate scripts (rx). </i> </b> 


### AUXILIARY SCRIPTS

* enable_usrp2.sh: Used in ORBIT Grid in order to enable the N210 USRPs
* reset_usrp.sh: Used to reset B205mini in ORBIT Sandbox 4 when running on Ubuntu 16
* shuffle_config.py: Used to create more experiments by shuffling the original config.json

## Equally Contributing Authors

* <b> Grigoris Kakkavas </b>, gkakkavas@netmode.ntua.gr
* <b> Konstantinos Tsitseklis </b> , ktsitseklis@netmode.ntua.gr


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
