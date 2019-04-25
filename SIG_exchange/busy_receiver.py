#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Script: simple_radio_receive.py
# Authors: K Tsitseklis, G. Kakkavas
# Generated: Sat Oct 13 13:38:21 2018
##################################################


from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import time
import sys
import os
from datetime import datetime

class simple_radio_receive(gr.top_block):

    def __init__(self, freq, filename, gain):
        gr.top_block.__init__(self, "Simple Radio Receive")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200000
        self.freq = freq
        self.filename = filename 
        
        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("addr=192.168.10.2", "")),
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_source_0.set_bandwidth(10e6, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
            1, samp_rate, samp_rate/2 - 2e3, (samp_rate/2 -2e3)/4, firdes.WIN_HAMMING, 6.76))
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,
            log=False,
        )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1, ))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, filename, True)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
                access_code='',
                threshold=-1,
                callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
            ),
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_packet_decoder_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/2 - 2e3, self.samp_rate/4, firdes.WIN_HAMMING, 6.76))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_sink_0.open(self.filename)


def receive(freq, filename, sec, gain, top_block_cls=simple_radio_receive, options=None):
    """ freq: the central frequency of the channel
        filename: file where the received data are stored
        sec: duration of reception 
        gain: rx gain """
    tb = top_block_cls(freq, filename, gain)
    tb.start()
    # keep listening until you start receiving
    t_start = datetime.now()
    while (os.stat(filename).st_size<500 and (datetime.now()-t_start).total_seconds()<=sec):
        pass
    #time.sleep(sec)
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    freq = eval(sys.argv[1])
    filename = sys.argv[2]
    sec = eval(sys.argv[3])
    gain = eval(sys.argv[4])
    receive(freq, filename, sec, gain)
