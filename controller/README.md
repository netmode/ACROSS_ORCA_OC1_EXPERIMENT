# controller
These scripts should be executed by the appointed controller, responsible for the coordination and synchronization of the Secondary Users' (SUs) operations

## Getting Started

These instructions will get you a copy of the module up and running on [Universal Software Radio Peripheral (USRP)](https://www.ettus.com/) devices for development and testing purposes. 

### Prerequisites

The  following additional file is required:
* <b> ipnet.json </b> : A JSON file containing all the nodes' IP addresses.

In order to run the experiment you will need Python 2.7 environment with the following modules installed:

* json

Also, a recent version of GNU Radio open-source software development toolkit must be installed. For more installation details visit the following website (https://wiki.gnuradio.org/index.php/InstallingGR) 

It is also necessary to have access to the appropriate USRP devices with at least UHD driver version 3.13.


## Execution

Three controller scripts are included in this module. Specifically:
* discovery_controller.py: Used to synchronize the discovery phase. Usage:
 ``` python discovery_controller.py controller_IP port file1 file2 ```
 Where:
	* controller_IP: Controller's IP address
	* port: The UDP port utilized
	* file1, file2: Auxiliary text files used for message exchange between the nodes and the controller
	
* giibs_controller.py: Used for the gibbs sampling phase and for round change. Two instances with different ports must be executed. Usage:
```python gibbs_controller.py file controller_ID port ```
Where:
	* file: Auxiliary text file used for message exchange between the nodes and the controller 
	* controller_ID: Controller's unique identifier
	* port: UDP port utilized
	
* final_controller.py: The controller of the signalling exchange phase. Usage:
```python final_controller.py controller_IP port file1 file2 ``` 
Where:
	* controller_IP: Controller's IP address
	* port: The UDP port utilized
	* file1, file2: Auxiliary text files used for message exchange between the nodes and the controller


## Equally Contributing Authors

* <b> Grigoris Kakkavas </b>, gkakkavas@netmode.ntua.gr
* <b> Konstantinos Tsitseklis </b> , ktsitseklis@netmode.ntua.gr


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

