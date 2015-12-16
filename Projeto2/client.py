#!/usr/bin/python3

from socket import *
import struct
import sys

"""
Cada pacote eh uma lista com os varios campos do protocolo TCP
Sao eles:
1 campo: sequence number(server)/ack number(client)
3 campo: checksum
4 campo: finbit - determina se ha dados para enviar (1 para dizer que ha)
5 campo: dados propriamente ditos
"""

def createPackage(seqAckNumber, checksum, finbit, data):
	return "+++".join((str(seqAckNumber), str(checksum), str(finbit), data))

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


"""
N  = window size
Rn = request number
Sn = sequence number
Sb = sequence base
Sm = sequence max

Receiver:
Rn = 0
Do the following forever:
If the packet received = Rn and the packet is error free
        Accept the packet and send it to a higher layer
        Rn = Rn + 1
        Send a Request for Rn
Else
        Refuse packet
        Send a Request for Rn
"""

arquivo = []

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
requestNumber = 0

#nome do arquivo a receber
#message = createPackage(requestNumber, 0, 0, "teste.txt")
message = createPackage(requestNumber, 0, 0, "projeto2.pdf")
print ("Pedido o pacote " + str(requestNumber))
clientSocket.sendto(message.encode(),(serverName, serverPort))
response, clientAddress = clientSocket.recvfrom(2048)
error = getFieldPackage(response.decode(), 3)
stopError = getFieldPackage(response.decode(), 2)
if error == "200 OK":
	while int(stopError) != 1:
		response, clientAddress = clientSocket.recvfrom(2048)
		if requestNumber == int(getFieldPackage(response.decode(), 0)):
			arquivo.append(getFieldPackage(response.decode(), 3))
			print ("Recebido o pacote " + str(requestNumber))
			requestNumber += 1
			message = createPackage(requestNumber, 0, 0, "ada")
			print ("Pedido o pacote " + str(requestNumber))
			clientSocket.sendto(message.encode(),(serverName, serverPort))
		stopError = getFieldPackage(response.decode(), 2)
	arquivo = "".join(arquivo)
	#with open("teste3.txt", 'wb') as f:
	with open("projeto3.pdf", 'wb') as f:
		f.write(arquivo.encode("ISO-8859-1"))
	print("Arquivo criado com sucesso!")
	clientSocket.close()
else:
	print("Arquivo nao encontrado")
	clientSocket.close()
