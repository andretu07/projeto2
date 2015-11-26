#!/usr/bin/python3

from socket import *
import struct
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
	return "+++".join((str(seqNumber), str(ackNumber), str(checksum), str(finbit), data))

def getFieldPackage(package, number):
	field = package.split("+++")
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
response, clientAddress = clientSocket.recvfrom(2048)
error = getFieldPackage(response.decode(), 4)
if error == "200 OK":
	response, clientAddress = clientSocket.recvfrom(2048)
	error = getFieldPackage(response.decode(), 3)
	while int(error) != 1:
		arquivo.append(getFieldPackage(response.decode(), 4))
		message = createPackage(0, int(getFieldPackage(response.decode(), 0))+len(getFieldPackage(response.decode(), 4)), 0, 0, "nada")
		clientSocket.sendto(message.encode(),(serverName, serverPort))
		response, clientAddress = clientSocket.recvfrom(2048)
		error = getFieldPackage(response.decode(), 3)
	arquivo = "".join(arquivo)
	with open("teste3.txt", 'wb') as f:
		f.write(arquivo.encode("ISO-8859-1"))
	print("Arquivo criado com sucesso!")
	clientSocket.close()
else:
	print("Arquivo nao encontrado")
	clientSocket.close()
