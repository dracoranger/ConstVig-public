
import dpkt
import re
import time
import socket

def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

s = time.time()

f = open("small2.pcap",'rb')
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
        match = reg.findall(line.decode('utf-8',errors='ignore'),0)
        #print(inet_to_str(ip.src),' --> ', inet_to_str(ip.dst))
        #print('From: ',tcp.sport,' --> ', tcp.dport)
        if len(match)>0:
            for thing in match:
                if thing not in matches:
                    matches.append(thing)
                    print(inet_to_str(ip.src),' --> ', inet_to_str(ip.dst))
                    print('From: ',tcp.sport,' --> ', tcp.dport)
                    print(thing)
                    break
for match in matches:
    print(match)
print(len(matches))
e = time.time()
print(inet_to_str(ip.src),' --> ', inet_to_str(ip.dst))
print('From: ',tcp.sport,' --> ', tcp.dport)
print("Total is: ", e-s)
f.close()
