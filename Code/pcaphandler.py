import subprocess
import os
#import datetime

work_dir = os.getcwd() #gets current directory
tgt_dir = os.path.dirname(work_dir) #moves up one level
pcap_dir = ''
for dir_name in os.walk(tgt_dir):
	#walks through all sister directories of current directory
	if 'put_pcaps_here' == os.path.basename(dir_name[0]):
		pcap_dir = dir_name[0]

for fil in os.listdir(pcap_dir):
	#splits up large pcaps into smaller pcaps inside folders, deletes large pcaps
	sname = os.fsdecode(fil)
	fname = pcap_dir+"\\"+sname
	splitLocl = 'SplitCap' #is a path to SplitCap, not just a string.
	inp =  splitLocl + " -r " + fname + " -s session"
	process = subprocess.Popen(inp, stdout=subprocess.PIPE)
	process.wait()
	os.unlink(fname)

for sub_dir in os.walk(pcap_dir):
	for fil in os.listdir(sub_dir[0]):
		#need to figure out how to iterate through subfolder
		#nested for loop?
		sname = os.fsdecode(fil)
		fname = sub_dir[0] +"\\"+sname
		fbase = sname.split(".")[0] #file name without '.pcap'
		#tname = datetime.datetime.now().strftime("%d_%H.%M.%S")
		newf = fbase + ".csv"
		if ".pcap" == sname[-5:]:
			tsharkCall = [
							"tshark",
							"-r",
							fname,
							"-Y",
							"frame contains 31:41:47:33:35:39:54:",
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
							sub_dir[0] +"\\"+newf
			]
			process = subprocess.Popen(tsharkCall, shell=True, stdout=subprocess.PIPE)
			process.wait()
			#os.unlink(fname) #***
