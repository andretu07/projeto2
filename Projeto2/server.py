#!/usr/bin/python3

from socket import *
import sys

def Package(seqNumber, ackNumber, checksum, finbit, data):
  return "\n".join((str(seqNumber), str(ackNumber), str(checksum), str(finbit), data))
 	
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

test = Package(0,0,0,0,"ola mundo")

clientSocket.sendto(test.encode(),(serverName, serverPort))




