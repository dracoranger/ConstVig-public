& 'C:\Program Files\Wireshark\tshark.exe' -r C:\Users\x85491\Documents\2017-2018\IT401\Sprint3\test1.pcap -T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e tcp.srcport -e tcp.dstport -E header=y -E separator=/t, -E quote=d -E occurrence=f > C:\Users\x85491\Documents\2017-2018\IT401\Sprint3\test2.csv
 
