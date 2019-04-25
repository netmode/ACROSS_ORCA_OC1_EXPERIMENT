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

``` python  availability.py channel_list gain    ```

It returns the availability vector where 1 means the channel is available and 0 means occupied by a Primary User (PU) 

Where:
* channel_list: A list containing the central frequencies of the channels of interest
* sec: The time spent scanning each channel of the channel_list
* gain: The gain used for the reception (rx_gain), needs to be specified according to the environment
 
 Example:
	``` python availability [3600e6,3650e6,3700e6,3750e6,3800e6] 0.5 30 2```.

The script PU_transmit.py is also included. It is used to simulate a Primary User's transmission.

The script primary_users.py is executed in the primary users and it is responsible for realizing primary activity. It can be executed by running:

``` python primary_users.py channel_list sec gain ```

Where:
* channel_list: A list containing the central frequencies of the channels of interest
* sec: The time spent transmitting at a channel
* gain: The gain used for the transmission (tx_gain), needs to be specified according to the environment


 <b><i> The provided code is suited for direct deployment on ORBIT's Grid. To deploy in different execution environments new parametrization is required for the receiving gain in the appropriate scripts (rx) </i> </b> 

## Equally Contributing Authors

* <b> Grigoris Kakkavas </b>, gkakkavas@netmode.ntua.gr
* <b> Konstantinos Tsitseklis </b> , ktsitseklis@netmode.ntua.gr


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
