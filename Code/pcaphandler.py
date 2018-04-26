# Splits pcaps into managable flows and converts to .csv format

# NAME: pcap Handler
# FILE: ConstVig/Code/pcaphandler.py
# CLASSES: N/A
# EXCEPTIONS:
# FUNCTIONS:
#     split
#     get_sql_data


import subprocess
import os
import re
import socket
import datetime

import dpkt

import utilities

DictionNI = utilities.parse_config('NetworkIn')
PATH_SPLIT = DictionNI['splitlocl']

def split(pcap_dir):
    os.chdir(pcap_dir)
    for fil in os.listdir(pcap_dir):
        if os.path.isfile(fil):
            # Splits up large pcaps into smaller pcaps inside folders
            # and deletes large pcaps
            sname = os.fsdecode(fil)
            fname = pcap_dir+'\\'+sname
			# This is the path to SplitCap; not just a string.
            inp = PATH_SPLIT + ' -r ' + fname + ' -s session'
            process = subprocess.Popen(inp, stdout=subprocess.PIPE)
            process.wait()
            os.rename(fname, pcap_dir+'\\processed\\'+fil)

def inet_to_str(inet):
    '''
    Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    '''
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def get_sql_data(regex, working_directory, home_directory):#, length):
    reg = re.compile(regex)
    os.chdir(working_directory)
    csv = working_directory +'.csv'
    info = []
    for file in os.listdir(os.getcwd()):
        with open(file, 'rb') as fn:
            pcap = dpkt.pcap.Reader(fn)
            for ts, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data
                tcp = ip.data
                if tcp.data:
                    line = tcp.data.strip()
                    matches = reg.findall(line.decode('utf-8', errors='ignore'), 0)
                    for match in matches:
                        time = str(datetime.datetime.utcfromtimestamp(ts))
                        data = '{},{},{},{},{},{},{}\n'.format(time, inet_to_str(ip.src), inet_to_str(ip.dst), tcp.sport, tcp.dport, match, file)
                        if data not in info:
                            info.append(data)
        os.rename(os.getcwd()+'\\'+file, home_directory+'\\processed\\'+working_directory+'\\'+file)
    with open(csv, 'w') as w:
        for item in info:
            w.write(item)
