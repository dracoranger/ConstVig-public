# Splits pcaps into managable flows and converts to .csv format

# NAME: pcap Handler
# FILE: ConstVig/Code/pcaphandler.py
# CLASSES: N/A
# EXCEPTIONS:
# FUNCTIONS:
#     split
#     getSqlData


import subprocess
import os


def split():
    work_dir = os.getcwd() # Gets current directory
    tgt_dir = os.path.dirname(work_dir) # Moves up one level
    pcap_dir = ''
    changed = 0
    for dir_name in os.walk(tgt_dir):
        # Walks through all sister directories of current directory
        if os.path.basename(dir_name[0]) == 'put_pcaps_here':
            pcap_dir = dir_name[0]
            os.chdir(pcap_dir)
    for fil in os.listdir(pcap_dir):
        if os.path.isfile(fil):
            changed = changed + 1
            # Splits up large pcaps into smaller pcaps inside folders
            # and deletes large pcaps
            sname = os.fsdecode(fil)
            fname = pcap_dir+"\\"+sname
			# This is the path to SplitCap; not just a string.
            splitLocl = '''C:\\Users\\T\\Documents
			\\GitHub\\ConstVig\\SplitCap_2-1\\SplitCap_2-1\\SplitCap.exe'''
            inp = splitLocl + " -r " + fname + " -s session"
            process = subprocess.Popen(inp, stdout=subprocess.PIPE)
            process.wait()
            #os.unlink(fname)
    return changed


def getSqlData():
    work_dir = os.getcwd() # Gets current directory
    tgt_dir = os.path.dirname(work_dir) # Moves up one level
    pcap_dir = ''
    ret = []
    for dir_name in os.walk(tgt_dir):
        # Walks through all sister directories of current directory
        if os.path.basename(dir_name[0]) == 'put_pcaps_here':
            pcap_dir = dir_name[0]
    for sub_dir in os.walk(pcap_dir):
        for fil in os.listdir(sub_dir[0]):
            sname = os.fsdecode(fil)
            fname = sub_dir[0] +"\\"+sname
            fbase = sname.split(".")[0] # File name without '.pcap'
            #tname = datetime.datetime.now().strftime("%d_%H.%M.%S")
            newf = fbase + ".csv"
            if sname[-5:] == ".pcap":
                ret.append(newf)
                tsharkCall = [
                    "E:\\Programs\\Wireshark\\tshark.exe",
                    "-r",
                    fname,
                    #"-Y",
                    #"frame contains 31:41:47:33:35:39:54:",
                    "-T",
                    "fields",
                    "-e",
                    "frame.number",
                    "-e",
                    "frame.time_epoch",
                    "-e",
                    "tcp.srcport",
                    "-e",
                    "tcp.dstport",
                    "-E",
                    "header=y",
                    "-E",
                    "separator=,",
                    "-E",
                    "quote=d",
                    "-E",
                    "occurrence=f",
                    ">",
                    'C:\\Users\\T\\Documents\\GitHub\\ConstVig\\\
                    put_pcaps_here'+"\\"+newf
                ]
                process = subprocess.Popen(tsharkCall,
                          shell=True, stdout=subprocess.PIPE)
                process.wait()
    return ret
