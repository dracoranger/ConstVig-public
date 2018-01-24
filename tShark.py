import subprocess
import os

work_dir = os.getcwd()
tgt_dir = os.path.dirname(work_dir)
pcap_dir = ''
for dir_name in os.walk(tgt_dir):
	if 'put_pcaps_here' == os.path.basename(dir_name[0]):
		pcap_dir = dir_name[0]

fname = pcap_dir + "\\test1.pcap"
tsharkCall1 = [
				"tshark",
				"-r",
				fname,
				"-T",
				"fields",
				"-e",
				"frame.time_epoch"
]
namer = subprocess.Popen(tsharkCall1, shell=True, stdout=subprocess.PIPE)
tsharkCall2 = [
				"tshark",
				"-r",
				fname,
				#"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\test1.pcap", #File path of pcap
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
				"separator=/t",
				"-E",
				"quote=d",
				"-E",
				"occurrence=f",
				">",
				pcap_dir + "\\testWS.txt"
				#"C:\\Users\\x86991\\Documents\\XE402\\ConstVig\\put_pcaps_here\\test1.pcap" #File path for txt file written
				]
process = subprocess.Popen(tsharkCall2, shell=True, stdout=subprocess.PIPE)
process.wait()
