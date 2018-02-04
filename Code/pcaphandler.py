import subprocess
import os
import datetime

work_dir = os.getcwd()
tgt_dir = os.path.dirname(work_dir)
pcap_dir = ''
for dir_name in os.walk(tgt_dir):
	if 'put_pcaps_here' == os.path.basename(dir_name[0]):
		pcap_dir = dir_name[0]

for fil in os.listdir(pcap_dir):
	sname = os.fsdecode(fil)
	fname = pcap_dir+"\\"+sname
	splitLocl = 'SplitCap.exe'
	inp =  splitLocl +" -r " +fname = " -s session"
	process = subprocess.Popen(inp, shell=True, stdout=subprocess.PIPE)
	process.wait()
	os.unlink(fname)

for fil in os.listdir(pcap_dir):
	#need to figure out how to iterate through subfolder
	#nested for loop?
	sname = os.fsdecode(fil)
	fname = pcap_dir+"\\"+sname
	fbase = sname.split(".")[0]
	tname = datetime.datetime.now().strftime("%d_%H.%M.%S")
	#potential issue of two files having the same name IF:
	#1) the pcaps have the exact same name
	#2) they are processed in the same second
	#This is unlikely enough for us to accept the potential bug.
	newf = fbase + "_" + tname + ".csv"
	if ".pcap" == sname[-5:]:
		tsharkCall = [
						"tshark",
						"-r",
						fname,
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
						pcap_dir +"\\"+newf
		]
		process = subprocess.Popen(tsharkCall, shell=True, stdout=subprocess.PIPE)
		process.wait()
		os.unlink(fname)
