#!/usr/bin/python3

from socket import *
import hashlib
import struct
import sys

'''
Função createPackage(seqAckNumber, checksum, finbit, data)
Cria um pacote, separados cada campo por +++, com os seguintes campos:
campo 1 - sequence number/ack Number
campo 2 - checksum
campo 3 - bit de final de arquivo
campo 4 - dados do arquivo
Retorna o pacote criado.
'''
def createPackage(seqAckNumber, checksum, finbit, data):
	return "+++".join((str(seqAckNumber), str(checksum), str(finbit), data))

'''
Função getFieldPackage(package, number)
Recupera os detalhes de um campo especifico de acordo com o numero para recuperacao
0 para recuperar o sequence number/ack Number
1 para recuperar o checksum
2 para recuperar o bit de final de arquivo
3 para recuperar os dados do arquivo
Retorna os detalhes do campo requisitado.
'''
def getFieldPackage(package, number):
	field = package.split("+++")
	return field[number]

'''
Função checkChecksum(package)
Verifica se o campo do checksum eh igual ao checksum criado com os dados do pacote.
'''
def checkChecksum(package):
	arq = getFieldPackage(package, 3)
	hash = hashlib.md5()
	hash.update(arq.encode())
	checksum = hash.hexdigest()
	return checksum == getFieldPackage(package, 1)

"""
Funcao Main
Cliente requisita um arquivo ao servidor com o primeira requisicao de pacote. Caso tenha o arquivo, espera a entrega do pacote requisitado e pede o proximo. Caso receba um pacote com o bit de fim de arquivo, o cliente encerra o programa escrevendo o arquivo requisitado em um arquivo na pasta do cliente. Possui um inicio de corrupcao de arquivo verificando o checksum do pacote recebido.
"""
arquivo = []

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_DGRAM)
requestNumber = 0

#nome do arquivo a receber
#message = createPackage(requestNumber, 0, 0, "teste.txt")
message = createPackage(requestNumber, 0, 0, sys.argv[3])
clientSocket.sendto(message.encode(),(serverName, serverPort))
response, clientAddress = clientSocket.recvfrom(2048)
error = getFieldPackage(response.decode(), 3)
stopError = getFieldPackage(response.decode(), 2)
if error == "200 OK":
	print ("Pedido o pacote " + str(requestNumber))
	while int(stopError) != 1:
		response, clientAddress = clientSocket.recvfrom(2048)
		if requestNumber == int(getFieldPackage(response.decode(), 0)) and checkChecksum(response.decode()):
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
