#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Script: simple_radio_transmit.py
# Authors: K. Tsitseklis, G. Kakkavas
# Generated: Sat Oct 13 13:19:16 2018
##################################################


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

class simple_radio_transmit(gr.top_block):

    def __init__(self, freq, filename, gain):
        gr.top_block.__init__(self, "Simple Radio Transmit")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200000
        self.freq = freq
        self.filename = filename

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
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(10e6, 0)
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
            samples_per_symbol=2,
            bt=0.35,
            verbose=False,
            log=False,
        )
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((1, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, filename, True)
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
                samples_per_symbol=2,
                bits_per_symbol=1,
                preamble='',
                access_code='',
                pad_for_usrp=True,
            ),
            payload_length=0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_multiply_const_vxx_1, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_source_0.open(self.filename, True)


def transmit(freq, filename, sec, gain, top_block_cls=simple_radio_transmit, options=None):
    """ freq: the central frequency of the channel
        filename: file that contains the data about to be transmitted
        sec: duration of transmission 
        gain: tx gain """
    tb = top_block_cls(freq, filename, gain)
    tb.start()
    print 'I am transmitting at',freq
    time.sleep(sec)
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    freq = eval(sys.argv[1])
    filename = sys.argv[2]
    sec = eval(sys.argv[3])
    gain = eval(sys.argv[4])
    transmit(freq, filename, sec, gain)
