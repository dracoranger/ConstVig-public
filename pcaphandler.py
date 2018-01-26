import subprocess
import os

work_dir = os.getcwd()
#tgt_dir = os.path.dirname(work_dir)
pcap_dir = ''
for dir_name in os.walk(work_dir):
	if 'put_pcaps_here' == os.path.basename(dir_name[0]):
		pcap_dir = dir_name[0]

for fil in os.listdir(pcap_dir):
	sname = os.fsdecode(fil)
	fname = pcap_dir+"\\"+sname
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
		namer = subprocess.Popen(tsharkCall1, shell=True, stdout=subprocess.PIPE)
		tsharkCall2 = [
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
		process = subprocess.Popen(tsharkCall2, shell=True, stdout=subprocess.PIPE)
		process.wait()
		os.unlink(fname)
