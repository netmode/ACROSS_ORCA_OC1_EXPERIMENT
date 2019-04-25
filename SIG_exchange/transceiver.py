#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Script: transceiver.py
# Authors: K. Tsitseklis, G. Kakkavas
# Generated: Thu Oct 18 10:29:35 2018
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
import os
import sys

class transceiver(gr.top_block):

    def __init__(self, freq_tx, freq_rx, filename_out, filename_in):
        gr.top_block.__init__(self, "Transceiver")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200000
        self.gain_tx = gain_tx = 50
        self.gain_rx = gain_rx = 50
        self.freq_tx = freq_tx
        self.freq_rx = freq_rx
        self.filename_out = filename_out 
        self.filename_in = filename_in 

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
        self.uhd_usrp_source_0.set_center_freq(freq_rx, 0)
        self.uhd_usrp_source_0.set_gain(gain_rx, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0.set_bandwidth(10e6, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("addr=192.168.10.2", "")),
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(freq_tx, 0)
        self.uhd_usrp_sink_0.set_gain(gain_tx, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(10e6, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
            1, samp_rate, samp_rate/2 - 2e3, (samp_rate/2 - 2e3)/4, firdes.WIN_HAMMING, 6.76))
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
            samples_per_symbol=2,
            bt=0.35,
            verbose=False,
            log=False,
        )
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=2,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,
            log=False,
        )
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, filename_in, True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, filename_out, True)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
                samples_per_symbol=2,
                bits_per_symbol=1,
                preamble='',
                access_code='',
                pad_for_usrp=True,
            ),
            payload_length=0,
        )
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
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/2 - 2e3, (self.samp_rate/2 - 2e3)/4, firdes.WIN_HAMMING, 6.76))

    def get_gain_tx(self):
        return self.gain_tx

    def set_gain_tx(self, gain_tx):
        self.gain_tx = gain_tx
        self.uhd_usrp_sink_0.set_gain(self.gain_tx, 0)


    def get_gain_rx(self):
        return self.gain_rx

    def set_gain_rx(self, gain_rx):
        self.gain_rx = gain_rx
        self.uhd_usrp_source_0.set_gain(self.gain_rx, 0)


    def get_freq_tx(self):
        return self.freq_tx

    def set_freq_tx(self, freq_tx):
        self.freq_tx = freq_tx
        self.uhd_usrp_sink_0.set_center_freq(self.freq_tx, 0)

    def get_freq_rx(self):
        return self.freq_rx

    def set_freq_rx(self, freq_rx):
        self.freq_rx = freq_rx
        self.uhd_usrp_source_0.set_center_freq(self.freq_rx, 0)

    def get_filename_out(self):
        return self.filename_out

    def set_filename_out(self, filename_out):
        self.filename_out = filename_out
        self.blocks_file_sink_0.open(self.filename_out)

    def get_filename_in(self):
        return self.filename_in

    def set_filename_in(self, filename_in):
        self.filename_in = filename_in
        self.blocks_file_source_0.open(self.filename_in, True)


def transceive(freq_tx, freq_rx, filename_in, filename_out, sec, top_block_cls=transceiver, options=None):
    """ Performs independent transmission and reception
        freq_tx: the central frequency of the transmission channel
        freq_rx: the central frequency of the reception channel
        filename_in: file that contains the data about to be transmitted
        filename_out: file where the received data are stored
        sec: duration of operation """
    tb = top_block_cls(freq_tx, freq_rx, filename_out, filename_in)
    tb.start()
    # keep listening until you start receiving
    while os.stat(filename_out).st_size<500:
        pass
    time.sleep(sec-0.2)
    tb.stop()
    tb.wait()


if __name__ == '__main__':
   freq_tx = eval(sys.argv[1])
   freq_rx = eval(sys.argv[2])
   filename_out = sys.argv[4]
   filename_in = sys.argv[3]
   sec = eval(sys.argv[5])
   transceive(freq_tx, freq_rx, filename_in, filename_out, sec)
