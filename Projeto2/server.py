def createPackage(seqAckNumber, checksum, finbit, data):
	return "+++".join((str(seqAckNumber), str(checksum), str(finbit), data))

def getFieldPackage(package, number):
	field = package.split("+++")
	return field[number]

from socket import *
"""
N  = window size
Rn = request number
Sn = sequence number
Sb = sequence base
Sm = sequence max

Sender:
Sb = 0
Sm = N − 1
Repeat the following steps forever:
1. If you receive a request number where Rn > Sb
        Sm = Sm + (Rn − Sb)
        Sb = Rn
2.  If no packet is in transmission, 
        Transmit a packet where Sb <= Sn <= Sm.  
        Packets are transmitted in order.
"""
N = 6
seqBase = 0
seqMax = N - 1

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
		package = createPackage(0, 0, 0, "200 OK")
		serverSocket.sendto(package.encode(), clientAddress)
		with open(fileToOpen, "rb") as f:
			for chunk in iter(lambda: f.read(1024), b""):
				if seqBase == requestNumber:
					package = createPackage(requestNumber, 0, 0, chunk.decode("ISO-8859-1"))
					serverSocket.sendto(package.encode(), clientAddress)
					seqBase += 1					
					requestNumber += 1
					print("Enviando pacote " + str(requestNumber))
					response, clientAddress = serverSocket.recvfrom(2048)
					requestNumber = int(getFieldPackage(response.decode(), 0))
		print("chega")
		package = createPackage(0, 0, 1, "nada")
		serverSocket.sendto(package.encode(), clientAddress)
