#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Udp Receive
# Authors: G. Kakkavas, K.Tsitseklis
# Generated: Thu Oct  4 14:29:13 2018
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys


class udp_receive(gr.top_block):

    def __init__(self, IP_address, udp_port, filename):
        gr.top_block.__init__(self, "Udp Receive")

        ##################################################
        # Variables
        ##################################################
        self.udp_port = udp_port
        self.filename = filename 
        self.IP_address = IP_address

        ##################################################
        # Blocks
        ##################################################
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_char*1, IP_address, udp_port, 1472, True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, filename, True)
        self.blocks_file_sink_0.set_unbuffered(True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_udp_source_0, 0), (self.blocks_file_sink_0, 0))    

    def get_udp_port(self):
        return self.udp_port

    def set_udp_port(self, udp_port):
        self.udp_port = udp_port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_sink_0.open(self.filename)

    def get_IP_address(self):
        return self.IP_address

    def set_IP_address(self, IP_address):
        self.IP_address = IP_address


def receive(IP_address, udp_port, filename, top_block_cls=udp_receive, options=None):

    tb = top_block_cls(IP_address, udp_port, filename)
    tb.start()
    tb.wait()


if __name__ == '__main__':
   # usage: receive a message via udp
    if len(sys.argv) != 4:
        print "Please insert correct number of arguments as specified below"
        print "node's IP, port to listen to, filename to write received info"
    else:
        IP_address = sys.argv[1]
        udp_port = int(sys.argv[2])
        filename = sys.argv[3]
        receive(IP_address, udp_port, filename)
