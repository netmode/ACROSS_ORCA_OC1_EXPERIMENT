
# Collision Detection

This module performs the energy based collision detection. 

## Getting Started

These instructions will get you a copy of the module up and running on [Universal Software Radio Peripheral (USRP)](https://www.ettus.com/) devices for development and testing purposes. 

### Prerequisites


In order to run the experiment you will need Python 2.7 environment with the following modules installed:

* scipy

Also, a recent version of GNU Radio open-source software development toolkit must be installed. For more installation details visit the following website (https://wiki.gnuradio.org/index.php/InstallingGR) 

It is also necessary to have access to the appropriate USRP devices with at least UHD driver version 3.13.


## Running the tests

The module can be executed by running the following command

``` python  energy_based_decision.py channel_list bandwidth    ```

It returns a binary list with 1 indicating channels where a collision occured.

Where:
* channel_list: A list containing the central frequencies of the channels of interest
* bandwidth:  The channel bandwidth (by convention all channels have the same bw)
 
 Example:
	``` python energy_based_decision.py [600e6,650e6,700e6,750e6,800e6] 10e6```.


 <b><i> The provided code is suited for direct deployment on ORBIT's Sandbox 4 . To deploy in different execution environments new parametrization is required for the receiving gain in the appropriate scripts (rx). Also, it is important to specify the proper background noise level (hardcoded inside function is_empty) for each application scenario</i> </b> 

## Equally Contributing Authors

* <b> Grigoris Kakkavas </b>, gkakkavas@netmode.ntua.gr
* <b> Konstantinos Tsitseklis </b> , ktsitseklis@netmode.ntua.gr


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
