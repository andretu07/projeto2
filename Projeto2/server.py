#!/usr/bin/python3

from socket import *
import sys

def Package(seqNumber, ackNumber, checksum, finbit, data):
  return "\n".join((str(seqNumber), str(ackNumber), str(checksum), str(finbit), data))
 	
serverName = 'localhost'
serverPort = 12000

serverSocket= socket(AF_INET, SOCK_DGRAM)

msg = serverSocket.recvfrom(2048)
print(msg)





