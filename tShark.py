import subprocess
tsharkCall2 = [	
				"tshark",
				"-r",
<<<<<<< HEAD
				"C:\\Users\\x86991\\Documents\\XE402\\test1.pcap",
=======
				"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\test1.pcap", #File path of pcap
>>>>>>> 76d9f04a8360d5285488734b26e1f7e02c5828f7
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
<<<<<<< HEAD
				"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\test4.csv"]

# process = subprocess.Popen(tsharkCall1, shell=True, stdout=subprocess.PIPE)
# process.wait()
=======
				"C:\\Users\\x85491\\Documents\\2017-2018\\IT401\\Sprint3\\testWS.txt" #File path for txt file written
				]
>>>>>>> 76d9f04a8360d5285488734b26e1f7e02c5828f7
process = subprocess.Popen(tsharkCall2, shell=True, stdout=subprocess.PIPE)
process.wait()
