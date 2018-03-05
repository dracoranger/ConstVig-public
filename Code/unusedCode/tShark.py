
import subprocess
import os
import re

#work_dir = os.getcwd()
#tgt_dir = os.path.dirname(work_dir)
#pcap_dir = ''
#for dir_name in os.walk(tgt_dir):
#	if 'put_pcaps_here' == os.path.basename(dir_name[0]):
#		pcap_dir = dir_name[0]
#		print('here')


for fil in range(1): #os.listdir(pcap_dir):
	sname = "small.pcap"
	fname = "C:\\Users\\x86075\\Documents\\GitHub\\ConstVig\\Code\\unusedCode" + "\\"+sname #pcap_dir+"\\"+sname
	fbase = sname.split(".")[0]
	newf = fbase + ".csv"
	if ".pcap" == sname[-5:]:
		tsharkCall1 = [
						"tshark",
						"-r",
						fname,
						"-T",
						"fields",
						"-e",
						"frame.time_epoch"
		]
		#namer = subprocess.Popen(tsharkCall1, shell=True, stdout=subprocess.PIPE)
		tsharkCall2 = [
						"tshark",
						"-r",
						fname,
						"-Y",
						"frame contains '^\w{31}='",
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
						"C:\\Users\\x86075\\Documents\\GitHub\\ConstVig\\Code\\unusedCode" + "\\"+newf
		]
		process = subprocess.Popen(tsharkCall2, shell=True, stdout=subprocess.PIPE)
		process.wait()
#		os.unlink(fname)
#		hex: 31:41:47:33:35:39:54:47:47:41:47:47:37:41:4b:54:35:58:54:49:4f:38:4b:48:59:59:4c:58:30:4f:53:3d
