#!/bin/bash

ip link set dev eth2 up &&
ifconfig eth2 192.168.10.1 netmask 255.255.255.0 &&

/usr/local/lib/uhd/utils/uhd_images_downloader.py &&
/usr/local/bin/uhd_image_loader --args="type=usrp2,addr=192.168.10.2"
