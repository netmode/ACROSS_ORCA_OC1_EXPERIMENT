#!/bin/bash

num=$(ps -eo pid,comm | grep python | cut -d'p' -f 1)
kill -9 $num
/usr/local/lib/uhd/utils/b2xx_fx3_utils --reset-device
~/uhd/host/build/examples/tx_waveforms --freq 500e6 --rate 500e3 --gain 30 
rm discovery_phase/ok.txt dataSend_init* vectorsSend.txt final_gibbs_sampling/new_info.txt final_gibbs_sampling/myNew_info.txt final_gibbs_sampling/dataReceived.txt freq.txt channel.txt
