#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import argparse, socket, random, string

class tcp_variable(object):
	def __init__(self):
		pass
	def recvall(self, sock, length):
		data = b''
		while len(data) < length:
			more = sock.recv(length - len(data))
			if not more:
				raise EOFError('was expecting %d bytes but only received'
							   ' %d bytes before the socket closed'
							   % (length, len(data)))
			data += more
		return data
		
	def random_msg(self, sock):
		""" Creates an alpha-numeric string of between 1 and 3000 characters in length.  Python 3 strings are unicode (2-bytes per char), 	so we 
		will change the encoding to ascii to reduce the size of the message in transit, as a result the message size will the same as the length (1 to 3000 bytes)
		"""
		#The double carriage return line feed sequence is typically used to denote the end of an application layer protocol header
		size = random.randint(1,3000)
		messageHeader = "Length: " + str(size + 10) + "\r\n\r\n" 
		messageBody = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(size)])
		message = messageHeader + messageBody
		return message.encode('ascii')

	def server(self, interface, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((interface, port))
		sock.listen(1)
		print('Listening at', sock.getsockname())
		while True:
			print('Waiting to accept a new connection')
			sc, sockname = sock.accept()
			print('We have accepted a connection from', sockname)
			print('  Socket connects:', sc.getsockname(),  'and',  sc.getpeername())
			message = self.recvall(sc, 16).decode('ascii')
			print('The incoming sixteen-octet message says', message)
			sc.sendall(message.encode('ascii'))
			length = int(message.split()[1])
			message = self.recvall(sc, length - 16).decode('ascii')
			print(message)
			sc.sendall(message.encode('ascii'))
			sc.close()
			print('  Reply sent, socket closed')

	def client(self, host, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, port))
		print('Client has been assigned socket name', sock.getsockname())
		sock.sendall(self.random_msg(sock))
		reply = self.recvall(sock, 16).decode('ascii')
		print('The server said', reply)
		length = int(reply.split()[1])
		reply = self.recvall(sock, length - 16).decode('ascii')
		print(reply)
		sock.close()

if __name__ == '__main__':
	x = tcp_variable()
	choices = {'client': x.client, 'server': x.server}
	parser = argparse.ArgumentParser(description='Send and receive over TCP')
	parser.add_argument('role', choices=choices, help='which role to play')
	parser.add_argument('host', help='interface the server listens at;'
						' host the client sends to')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060,
						help='TCP port (default 1060)')
	args = parser.parse_args()
	function = choices[args.role]
	function(args.host, args.p)
