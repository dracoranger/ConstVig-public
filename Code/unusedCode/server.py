#!/usr/bin/python3

from socket import *
import threading
import sys
import locale, datetime
import time
import os


"""
chatServer.py
Author: LTC Raymond with updates by COL Ransbottom and Dr. Hughes
Date: October 2016, January 2013, original August 2012
Description: Simple server for CS484 programming assignment 2, chat client.
  This program listens on port specified by user on command line.  If
  no port number is provided, listens on port 5000.
Update Notes:
Oct16: Now runs with Python3; also does not crash when client dies
       Added graceful shutdown.

Usage: chatServer.py [port number]
"""

DEFAULT_PORT = 5000
logfile = "chat.log"

class chatThread(threading.Thread):
    """
    Class: chatThread
    Purpose: Each client connection spawns a new chatThread object
      and interaction with the client is via this thread.
    """

    def __init__(self, parent, csock):
        """ chatThread constructor """
        # Call parent class constructor
        threading.Thread.__init__(self)
        self.csock = csock

        # Need to be able to reference parent to send messages to all threads
        self.parent = parent

    def run(self):
        """ Main loop for chatThread objects """

        try:
            while (1):
                # Receive chat message from client
                message = self.csock.recv(1024)
                message = message.decode()

                # reading from a closed socket will yield empty messages (0 bytes)
                if len(message) == 0:
                    raise Exception("Client closed unexpectedly")

                # Call method in parent that iterates through all
                # connected client threads and sends message to all

                # log the request
                log_fh = open(logfile, "a")

                logdate = datetime.datetime.utcnow().strftime('%b %d %H:%M:%S')
                log_line = logdate + ": " + message

                log_fh.write(log_line+"\n")
                log_fh.close()

                self.parent.sendToAll(message.encode())

        except:  # handle exception type
            # client has left, close socket and end thread
            self.csock.close()


    def sendMsg(self, msg):
        """ Send a message to the client in this thread. """
        # message must be in bytes format
        self.csock.send(msg)


class chatServer:
    """
    Class: chatServer
    Purpose: Main class for chatServer program.
    """

    # Need a list of threads in order to iterate through them and send
    # incoming message to each
    mythreads = [] # list of all threads

    def __init__(self, serverPort):
        """ chatServer constructor (just sets local variables). """
        self.serverPort = serverPort

    def sendToAll(self, msg):
        """ Messages from a chatClient go to all connected clients. """
        # Iterate through all client threads
        for thread in self.mythreads:
            # Make sure thread is still alive (client is connected)
            if thread.isAlive():
                # Call sendMsg method for each chatThread
                thread.sendMsg(msg)


    def main(self):
        """ Main logic for chatServer program. """
        # Create new socket and bind to listening port
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(('',self.serverPort))

        # Allow up to 5 queued connections
        serverSocket.listen(5)
        print('Ready to serve on port',self.serverPort)

        # Loop forever, waiting for clients to connect
        try:
            while True:
                # Accept connection
                connectionSocket, addr = serverSocket.accept()

                # Create new chatThread and hand off socket
                chatter = chatThread(self, connectionSocket)

                # Add new chatThread to list of all threads
                self.mythreads.append(chatter)

                #start new chatThread
                chatter.start()
#                print('New client joined')

                for thread in self.mythreads:
                    if not thread.isAlive():
                        thread.join()
                        self.mythreads.remove(thread)

        except KeyboardInterrupt:
            self.sendToAll("Server shutting down now! End your chats!\n".encode())

            # close main socket
            serverSocket.close()

            # wait for clients to finish
            for workerThread in self.mythreads:
                workerThread.join()

            print("Shutdown complete... exiting")
            sys.exit()


if __name__ == "__main__":
    """ Main starting point for chatServer program. """
    # Enter port number as argument if you want other than default
    servPort = DEFAULT_PORT

    if len(sys.argv) > 1:
        try:
            servPort = int(sys.argv[1])

            if (servPort < 1024) or (servPort > 65535):
                raise ValueError("Out of range")
        except:
            print("Invalid or range type for port number.  Setting to default (" \
                  + str(DEFAULT_PORT) + ")")
            servPort = DEFAULT_PORT

    server = chatServer(servPort)
    server.main()
