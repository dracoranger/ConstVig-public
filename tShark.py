import subprocess
tsharkCall2 = [	
				"tshark",
				"-r",
				"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\test1.pcap", #File path of pcap
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
				"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\testWS.txt" #File path for txt file written
				]
process = subprocess.Popen(tsharkCall2, shell=True, stdout=subprocess.PIPE)
process.wait()
