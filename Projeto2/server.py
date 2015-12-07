﻿import threading
import time
from socket import *
from subprocess import *

def createPackage(seqAckNumber, checksum, finbit, data):
	return "+++".join((str(seqAckNumber), str(checksum), str(finbit), data))

def getFieldPackage(package, number):
	field = package.split("+++")
	return field[number]

def listener(serverSocket):
	global requestNumber
	global base
	serverSocket.settimeout(60)
	try:
		while 1:
			response, clientAddress = serverSocket.recvfrom(2048)
			base = requestNumber + 1
	except timeout:
		serverSocket.close()
	#Erro na decodificação do unicode. Ignorar.
	except:
		None

def burst(serverSocket):
	global base
	global requestNumber
	counter = base
	serverSocket.settimeout(60)
	try:
		time.sleep(1)
		while counter != requestNumber - 1:
			serverSocket.sendto(packages[counter], clientAddress)	
			counter += 1
	except timeout:
		serverSocket.close()
	#Erro na decodificação do unicode. Ignorar.
	except:
		None

N = 6
base = 0
requestNumber = 0
packages = []

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("The server is ready to receive")
while 1:
	response, clientAddress = serverSocket.recvfrom(2048)
	fileToOpen = getFieldPackage(response.decode(), 3)
	requestNumber = int(getFieldPackage(response.decode(), 0))
	try:
		fl = open(fileToOpen, 'rb')
	except IOError:
		package = createPackage(0, 0, 0, "404 Not Found")
		serverSocket.sendto(package.encode(), clientAddress)
	else:
		count = 0
		with open(fileToOpen, "rb") as f:
			for chunk in iter(lambda: f.read(1024), b""):
				package = createPackage(count, 0, 0, chunk.decode("ISO-8859-1"))
				packages.append(package.encode())
				count += 1
		t1 = threading.Thread(target=listener, args=(serverSocket, ))
		t1.daemon = True
		t1.start()
		t2 = threading.Thread(target=burst, args=(serverSocket, ))
		t2.daemon = True
		t2.start()
		package = createPackage(0, 0, 0, "200 OK")
		serverSocket.sendto(package.encode(), clientAddress)
		while requestNumber < len(packages):
			if requestNumber < base + N:
				print("Enviando pacote " + str(requestNumber))
				serverSocket.sendto(packages[requestNumber], clientAddress)					
				requestNumber += 1
				time.sleep(0)
		print("chega")
		package = createPackage(0, 0, 1, "nada")
		serverSocket.sendto(package.encode(), clientAddress)
