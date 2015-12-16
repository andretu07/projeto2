import threading
import time
import hashlib
from socket import *
from subprocess import *
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
Função generateChecksum(package)
Gera o checksum dado o pacote, pegando o que possui no campo de dados e gerando o checksum e devolvendo o pacote com o checksum no seu campo devido.
'''
def generateChecksum(package):
	arq = getFieldPackage(package, 3)
	hash = hashlib.md5()
	hash.update(arq.encode())
	checksum = hash.hexdigest()
	package = createPackage(getFieldPackage(package, 0), checksum, getFieldPackage(package, 2), arq)
	return package

'''
Função listener(serverSocket)
Thread responsavel pela parte de receber os pedidos do cliente. Nao foi implementada a parte de corrupcao e nem de perda de pacotes.
'''
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

'''
Função burst(serverSocket)
Thread responsavel pela parte de enviar sua janela para o cliente no comeco da comunicacao. Nao foi implementado a parte da perda de pacotes com o Timer.
'''
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

#Variaveis responsaveis para a manipulacao no GobackN(Tamanho da janela, numbero base do GobackN, Numero do pacote a ser enviado e pacotes a serem enviados
N = 6
base = 0
requestNumber = 0
packages = []

'''
Função Main
Função que implementa as funcionalidades do Server. Primeiramente, o server pede a requisicao de envio de um arquivo. Tenta abri-lo, se o arquivo nao existir, o server envia uma mensagem de erro e nao envia mais nada, se o arquivo existir, inicia as duas threads, listener e burst, e  envia um OK ao cliente e comeca o envio do arquivo conforme o GobackN determina, enquanto a janela do GobackN nao chegar no limite, envia um pacote novo.
'''
serverPort = int(sys.argv[1])
#serverPort = 12000
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
				package = generateChecksum(package)
				package = package.encode()
				packages.append(package)
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
		print("chega")
		package = createPackage(0, 0, 1, "nada")
		serverSocket.sendto(package.encode(), clientAddress)
