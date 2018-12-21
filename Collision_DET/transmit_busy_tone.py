#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Script: transmit_busy_tone.py
# Authors: G. Kakkavas, K. Tsitseklis
# Generated: Mon Sep 10 12:18:40 2018
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import time
import sys


class transmit_busy_tone(gr.top_block):

    def __init__(self, b_freq, gain, dt):
        gr.top_block.__init__(self, "Transmit Busy Tone")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200000
        self.b_freq = b_freq

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(b_freq, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_bandwidth(10e6, 0)
        self.digital_dxpsk_mod_1 = digital.dbpsk_mod(
            samples_per_symbol=2,
            excess_bw=0.35,
            mod_code="gray",
            verbose=False,
            log=False)
            
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((10, ))
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_f(grc_blks2.packet_encoder(
                samples_per_symbol=2,
                bits_per_symbol=1,
                preamble='',
                access_code='',
                pad_for_usrp=True,
            ),
            payload_length=0,
        )
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SQR_WAVE, 500, 10, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blks2_packet_encoder_0, 0))    
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_dxpsk_mod_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.digital_dxpsk_mod_1, 0), (self.blocks_multiply_const_vxx_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)

    def get_b_freq(self):
        return self.b_freq

    def set_b_freq(self, b_freq):
        self.b_freq = b_freq
        self.uhd_usrp_sink_0.set_center_freq(self.b_freq, 0)


def b_transmit(b_freq, gain, dt, top_block_cls=transmit_busy_tone, options=None):
    """ Transmits busy tone
        b_freq: busy tone frequency
        gain: tx gain
        dt: duration of transmission """
    tb = top_block_cls(b_freq, gain, dt)
    tb.start()
    time.sleep(dt) #transmit for dt seconds
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    b_freq = eval(sys.argv[1])
    gain = eval(sys.argv[2])
    dt = eval(sys.argv[3])
    b_transmit(b_freq, gain, dt)
