def createPackage(seqNumber, ackNumber, checksum, finbit, data):
	return "+++".join((str(seqNumber), str(ackNumber), str(checksum), str(finbit), data))

def getFieldPackage(package, number):
	field = package.split("+++")
	return field[number]

from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("The server is ready to receive")
while 1:
	response, clientAddress = serverSocket.recvfrom(2048)
	fileToOpen = getFieldPackage(response.decode(), 4)
	try:
		fl = open(fileToOpen, 'rb')
	except IOError:
		package = createPackage(0, 0, 0, 0, "404 Not Found")
		serverSocket.sendto(package.encode(), clientAddress)
	else:
		package = createPackage(0, 0, 0, 0, "200 OK")
		serverSocket.sendto(package.encode(), clientAddress)
		testCount = 0
		with open(fileToOpen, "rb") as f:
			for chunk in iter(lambda: f.read(128), b""):
				package = createPackage(0, 0, 0, 0, chunk.decode("ISO-8859-1"))
				serverSocket.sendto(package.encode(), clientAddress)
				print("Enviando pacote " + str(testCount))
				testCount += 1
				response, clientAddress = serverSocket.recvfrom(2048)
		package = createPackage(0, 0, 0, 1, "nada")
		serverSocket.sendto(package.encode(), clientAddress)
