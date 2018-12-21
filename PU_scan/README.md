# PU_scan

This module is responsible for the detection of active PU transmissions. 

## Getting Started

These instructions will get you a copy of the module up and running on [Universal Software Radio Peripheral (USRP)](https://www.ettus.com/) devices for development and testing purposes. 

### Prerequisites

In order to run the module a Python 2.7 environment is required.

Also, a recent version of GNU Radio open-source software development toolkit must be installed. For more installation details visit the following website (https://wiki.gnuradio.org/index.php/InstallingGR) 

It is also necessary to have access to the appropriate USRP devices with at least UHD driver version 3.13.


## Running the tests

The module can be executed by running the following command

``` python  PU_availability.py channel_list gain    ```

It returns the availability vector where 1 means the channel is available and 0 means occupied by a Primary User (PU) 

Where:
* channel_list: A list containing the central frequencies of the channels of interest
* gain: The gain used for the reception (rx_gain), needs to be specified according to the environment
 
 Example:
	``` python PU_availability [600e6,650e6,700e6,750e6,800e6] 50```.

The script PU_transmit.py is also included. It is used to simulate a Primary User's transmission.

 <b><i> The provided code is suited for direct deployment on ORBIT's Sandbox 4 . To deploy in different execution environments new parametrization is required for the receiving gain in the appropriate scripts (rx) </i> </b> 

## Equally Contributing Authors

* <b> Grigoris Kakkavas </b>, gkakkavas@netmode.ntua.gr
* <b> Konstantinos Tsitseklis </b> , ktsitseklis@netmode.ntua.gr


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
