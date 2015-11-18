#!/usr/bin/python3

from socket import *
import sys

"""
Cada pacote eh uma lista com os varios campos do protocolo TCP
Sao eles:
1 campo: sequence number
2 campo: ack number
3 campo: checksum
4 campo: finbit - determina se ha dados para enviar (1 para dizer que ha)
5 campo: dados propriamente ditos
"""

def createPackage(seqNumber, ackNumber, checksum, finbit, data):
	return "\n".join((str(seqNumber), str(ackNumber), str(checksum), str(finbit), data))

def getFieldPackage(package, number):
	field = package.split("\\n")
	return field[number]

#if len(sys.argv) != 4:
#	print("python3 client.py <hostname_do_rementente> <numero_de_porta_do_rementente> <nome_do_arquivo>")
#else:
#	print (sys.argv[0]) # prints python_script.py
#	print (sys.argv[1]) # prints var1
#	print (sys.argv[2]) # prints var2
#	print (sys.argv[3]) # prints var3

arquivo = []

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

#nome do arquivo a receber
message = createPackage(0, 0, 0, 0, "teste.txt")
clientSocket.sendto(message.encode(),(serverName, serverPort))
response = clientSocket.recvfrom(2048).decode()
error = getFieldPackage(response, 4)
if error == "200 OK":
	response = clientSocket.recvfrom(2048)
	error = error = getFieldPackage(response, 3)
	while error != 1:
		arquivo.append(getFieldPackage(response, 4))
		message = createPackage(0, getFieldPackage(response, 0)+len(getFieldPackage(response, 4)), 0, 0, 0)
		clientSocket.sendto(message,(serverName, serverPort))
		response = clientSocket.recvfrom(2048)
		error = error = getFieldPackage(response, 3)
	clientSocket.close()
else:
	print("Arquivo nao encontrado")
