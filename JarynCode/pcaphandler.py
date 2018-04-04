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
import dpkt
import re
import time
import socket

#TODO DON"T USE RELATIVE PATHS


def split(pcap_dir):
    # Use the below to test the split() function alone:
        # work_dir = os.getcwd() # Gets current directory
        # tgt_dir = os.path.dirname(work_dir) # Moves up one level
        # pcap_dir = ''
        # changed = 0
        # for dir_name in os.walk(tgt_dir):
        #     # Walks through all sister directories of current directory
        #     if os.path.basename(dir_name[0]) == 'put_pcaps_here':
        #         pcap_dir = dir_name[0]
        #         os.chdir(pcap_dir)
    os.chdir(pcap_dir)
    changed=0
    for fil in os.listdir(pcap_dir):
        if os.path.isfile(fil):
            changed = changed + 1
            # Splits up large pcaps into smaller pcaps inside folders
            # and deletes large pcaps
            sname = os.fsdecode(fil)
            fname = pcap_dir+"\\"+sname
			# This is the path to SplitCap; not just a string.
            splitLocl = 'C:\\Users\\x86075\\Desktop\\DeskCV\\SplitCap_2-1\\SplitCap.exe'
            inp = splitLocl + " -r " + fname + " -s session"
            process = subprocess.Popen(inp, stdout=subprocess.PIPE)
            process.wait()
    return changed

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

def get_sql_data(regex,pcap_dir):#, length):
    #assembled = regex.format(length)

    reg=re.compile(regex)
    print(reg)
                    # work_dir = os.getcwd() # Gets current directory
                    # tgt_dir = os.path.dirname(work_dir) # Moves up one level
                    # for dir_name in os.walk(tgt_dir):
                    #     if os.path.basename(dir_name[0]) == 'put_pcaps_here':
                    #         pcap_dir = dir_name[0]
                    #         break
    s =time.time()
    os.chdir(pcap_dir)
    cwd=os.getcwd()
    for sub_dir in os.listdir(pcap_dir):
        os.chdir(cwd)
        if sub_dir == 'PROCESSED':
            continue
        os.chdir(sub_dir)
        newf = sub_dir +".csv"
        # if newf not in os.listdir(os.getcwd()):
        #     with open(newf,'w') as w:
        #         w.write('Filename,SRC IP,DST IP,SRC Port,DST Port,Flag\n')
        # with open(newf,'a') as data:
        os.mkdir('PROCESSED')
        info=[]
        for fil in os.listdir(cwd+'\\'+sub_dir):
            if fil=='PROCESSED':
                continue
            if fil.endswith('.csv'):
                print(True)
            with open(fil,'rb') as fn:
                pcap = dpkt.pcap.Reader(fn)
                for ts,buf in pcap:
                    eth=dpkt.ethernet.Ethernet(buf)
                    ip=eth.data
                    tcp=ip.data
                    if tcp.data:
                        line =tcp.data.strip()
                        matches=reg.findall(line.decode('utf-8',errors='ignore'),0)
                        if len(matches)>0:
                            for match in matches:

                                data = '{},{},{},{},{},{}\n'.format(fil,inet_to_str(ip.src),inet_to_str(ip.dst),tcp.sport,tcp.dport,match)
                                if data not in info:
                                    info.append(data)
            os.rename(os.getcwd()+'\\'+fil,os.getcwd()+'\\PROCESSED\\'+fil)

        with open(newf,'w') as w:
            w.write('Filename,SRC IP,DST IP,SRC Port,DST Port,Flag\n')
            for item in info:
                w.write(item)
    e =time.time()
    return ("Time was: ",e-s)