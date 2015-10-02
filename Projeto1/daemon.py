operacao = ""

'''
Funcao executestr(checkstr)
'''

def parse_and_execute(sentence):
	global operacao

	if (sentence[0:7] == "REQUEST"):
		saidaValida = True
		comando = sentence[8:]

		if (comando[0] == "1"):
			operacao = "1 "
			comando = comando.replace("1","ps",1)
		elif (comando[0] == "2"):
			operacao = "2 "
			comando = comando.replace("2","df",1)
		elif (comando[0] == "3"):
			operacao = "3 "
			comando = comando.replace("3","finger",1)
		elif (comando[0] == "4"):
			operacao = "4 "
			comando = comando.replace("4","uptime",1)
		else:
			operacao = "0"
			saidaValida = False

		if(saidaValida):
			comando = cleanStr(comando)
			comando = comando.replace(' ',' -',1)
			comando = comando.split()
			print comando
			saida = subprocess.check_output(comando)
			return saida
		else:
			return ''
	else:
		operacao = "0"
		return ''

def cleanStr(stringUser):
	erro = len(stringUser)
	outro_erro = stringUser.find('>')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)
	outro_erro = stringUser.find('<')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)
	outro_erro = stringUser.find('|')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)
	outro_erro = stringUser.find('&')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)
	outro_erro = stringUser.find(';')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)
	return stringUser[0:erro]

def threadfunction(connectionSocket):	
	connectionSocket.settimeout(21)
	try:
		while 1:
			sentence = connectionSocket.recv(10000)
			print sentence
			comando_executado = parse_and_execute(sentence)
			msgfinal = "RESPOND " + operacao + comando_executado.decode()
			connectionSocket.send(msgfinal.encode())
	except timeout:
		connectionSocket.close()

#main
from socket import *
import threading
import subprocess

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
#serverSocket.settimeout(60)
print ("The server is ready to receive")
while 1:
	connectionSocket, addr = serverSocket.accept()
	#inicio da thread
	t = threading.Thread(target=threadfunction, args=(connectionSocket, ))
	t.daemon = True
	t.start()
