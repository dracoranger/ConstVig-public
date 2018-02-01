import subprocess
import string

amountOfFlows=4162 #Amount of flows you have in pcap
for flowNumber in range(0, amountOfFlows):
	tsharkCall2 = [	
					"tshark",
					"-nr",
					"test4.pcap", #Name of pcap file which you want to split into seperate flows
					"-2",
					"-R",
					"tcp.stream eq {}".format(flowNumber),
					"-w",
					"stream_{}.pcap".format(str(flowNumber)) #Name of pcap file for new flow
					]
	process = subprocess.Popen(tsharkCall2, shell=True, stdout=subprocess.PIPE)
	process.wait()