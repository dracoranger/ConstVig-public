from scapy.all import *
import csv
import time

start = time.time()

pkts = rdpcap('test4.pcap')
ports = [22] #Specify what ports you want the pkts to have for destination and source
myData = [['Source Port'],['Destination Port'],['Payload'],['Time Stamp']] #List to keep data from packets
for pkt in pkts: #filter which packets to keep
	if TCP in pkt and (pkt[TCP].sport in ports or pkt[TCP].dport in ports):
	# for pkt in filtered:q
		l = pkt.getlayer(Raw)
		rawdata = Raw(l)
		# payload = str(rawdata)
		payload = str(rawdata).encode("HEX") #Encode payload into Hex
		myData[0].append(pkt[TCP].sport)
		myData[1].append(pkt[TCP].dport)
		myData[2].append(str(payload))
		myData[3].append(pkt.time)

		
# print(myData)
myData = zip(*myData)

with open('example4.csv', 'wb') as myFile: #Create csv file
# with open('example.csv', 'w') as myFile:
	writer = csv.writer(myFile)
	writer.writerows(myData) #Write information from myData to each row in csv file

end = time.time()

print(start)
print(end)
print(end-start)


# rdpcap comes from scapy and loads in our pcap file
# packets = rdpcap('test1.pcap')

# Let's iterate through every packet
#for packet in packets:
	# We're only interested packets with a DNS Round Robin layer
# print(packets)
# sniff(filter = 'dst port 22')
#		# If the an(swer) is a DNSRR, print the name it replied with.
#		if isinstance(packet.an, DNSRR):
#	print(p)

#	print(packet)
# print(packets)

# def pkt_callback(pkt):
	# pkt.show() # debug statement
# sniff(offline='test1.pcap',prn=pkt_callback, filter = None)