
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
	sname = "test1.pcap"
	fname = "C:\\Users\\x86075\\Documents\\GitHub\\ConstVig\\pcap_test_backups" + "\\"+sname #pcap_dir+"\\"+sname
	fbase = sname.split(".")[0]
	newf = fbase + ".csv"
	r=r"^\w\t"
	regx = re.compile(r)
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
						"ip.src",
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
						"C:\\Users\\x86075\\Documents\\GitHub\\ConstVig\\pcap_test_backups" + "\\"+newf
		]
		process = subprocess.Popen(tsharkCall2, shell=True, stdout=subprocess.PIPE)
		process.wait()
#		os.unlink(fname)
