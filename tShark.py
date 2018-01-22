import subprocess
import os

work_dir = os.getcwd()
tgt_dir = os.path.dirname(work_dir)
pcap_dir = ''
for dir_name in os.walk(tgt_dir):
	if 'put_pcaps_here' == os.path.basename(dir_name[0]):
		pcap_dir = dir_name[0]

tsharkCall2 = [
				"tshark",
				"-r",
				pcap_dir + "\\test1.pcap",
				#"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\test1.pcap", #File path of pcap
				"-T",
				"fields",
				"-e",
				"frame.number",
				"-e",
				"frame.time",
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
				#"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\testWS.txt" #File path for txt file written
				]
process = subprocess.Popen(tsharkCall2, shell=True, stdout=subprocess.PIPE)
process.wait()
