import subprocess
tsharkCall1 = ["tshark", "-nr", "test4.pcap", "-2", "-R", "tcp.stream eq 1", "-w", "small.pcap",]
tsharkCall2 = [	"tshark",
				"-r",
				"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\test1.pcap",
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
				"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\test4.csv"]
				
# process = subprocess.Popen(tsharkCall1, shell=True, stdout=subprocess.PIPE)
# process.wait()
process = subprocess.Popen(tsharkCall2, shell=True, stdout=subprocess.PIPE)
process.wait()