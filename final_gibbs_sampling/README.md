
# final_gibbs_sampling

This module contains scripts used for the sequential gibbs sampling (sequential_sampling.py) and semi-parallel gibbs sampling (semi_parallel_sampling.py)

## Getting Started

These instructions will get you a copy of the module up and running on [Universal Software Radio Peripheral (USRP)](https://www.ettus.com/) devices for development and testing purposes. 

### Prerequisites


In order to run the experiment you will need Python 2.7 environment with the following modules installed:

* json
* numpy

Also, a recent version of GNU Radio open-source software development toolkit must be installed. For more installation details visit the following website (https://wiki.gnuradio.org/index.php/InstallingGR) 

It is also necessary to have access to the appropriate USRP devices with at least UHD driver version 3.13.


## Running the tests
This module is not meant to run independently. The scripts contained are called by total_node.py when appropriate.

 <b><i> The provided code is suited for direct deployment on ORBIT's Grid. To deploy in different execution environments new parametrization is required for the receiving gain in the appropriate scripts (rx). </i> </b> 

## Equally Contributing Authors

* <b> Grigoris Kakkavas </b>, gkakkavas@netmode.ntua.gr
* <b> Konstantinos Tsitseklis </b> , ktsitseklis@netmode.ntua.gr


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
