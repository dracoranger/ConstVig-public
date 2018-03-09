
import dpkt
import re
import time

s = time.time()

f = open("test1.pcap",'rb')
pcap = dpkt.pcap.Reader(f)
r = r"[A-Z0-9]{}=".format("{31}")
reg=re.compile(r)

matches = []
for ts, buf in pcap:
    eth = dpkt.ethernet.Ethernet(buf)
    ip = eth.data
    tcp = ip.data
    if tcp.data:
        line = tcp.data.strip()
        match = reg.findall(line.decode('utf-8',errors='ignore'))
        if len(match)>0:
            matches.append(match)

for match in matches:
    print(match)
e = time.time()

print("Total is: ", e-s)
f.close()
