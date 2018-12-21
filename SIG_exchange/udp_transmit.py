#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Script: udp_transmit.py
# Authors: G. Kakkavas, K Tsitseklis
# Generated: Thu Oct  4 14:29:18 2018
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys
import time


class udp_transmit(gr.top_block):

    def __init__(self, IP_address, udp_port, filename):
        gr.top_block.__init__(self, "Udp Transmit")

        ##################################################
        # Variables
        ##################################################
        self.udp_port = udp_port
        self.samp_rate = samp_rate = 64000
        self.filename = filename
        self.IP_address = IP_address

        ##################################################
        # Blocks
        ##################################################
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_char*1, IP_address, udp_port, 1472, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, filename, True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_udp_sink_0, 0))    

    def get_udp_port(self):
        return self.udp_port

    def set_udp_port(self, udp_port):
        self.udp_port = udp_port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_source_0.open(self.filename, False)

    def get_IP_address(self):
        return self.IP_address

    def set_IP_address(self, IP_address):
        self.IP_address = IP_address


def transmit(IP_address, udp_port, filename, top_block_cls=udp_transmit, options=None):
    """ Transmits data via udp
        IP_address: destination IP address
        udp_port: the port utilized
        filename: file that contains the data about to be transmitted """
    tb = top_block_cls(IP_address, udp_port, filename)
    tb.start()
    time.sleep(0.25) # transmission's duration
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    IP_address = sys.argv[1]
    udp_port = int(sys.argv[2])
    filename = sys.argv[3]
    transmit(IP_address, udp_port, filename)
