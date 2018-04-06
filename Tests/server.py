# chat_server.py

#http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php

import sys
import socket
import select
import threading

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096

#PORT = 9009

def chat_server(port, message):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, port))
    server_socket.listen(10)

    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)

    print("Chat server started on port " + str(port))

    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        if ready_to_read != []:
            print(ready_to_read)
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)

                #broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
                send(server_socket, sockfd, message)

    server_socket.close()

# broadcast chat messages to all connected clients
def send(server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

#if __name__ == "__main__":
def main():
    threads = []
    threads.append(threading.Thread(target=chat_server, args=([9001,"NEXV2="])))
    threads.append(threading.Thread(target=chat_server, args=([9901,"NXX73="])))
    threads.append(threading.Thread(target=chat_server, args=([9991,"KUOI1="])))
    threads.append(threading.Thread(target=chat_server, args=([9999,"PONH7="])))
    threads.append(threading.Thread(target=chat_server, args=([9009,"CBES6="])))
    for i in threads:
        i.start()
    while True:
        for i in threads:
            i.run()
main()
