def executestr(checkstr):
	if (checkstr[0:7] == "REQUEST"):
		comando = checkstr.split()
		print (comando)
		comando.pop(0)
		if (comando[0] == "1"):
			comando.pop(0)
			comando.insert(0,"ps")
		elif (comando[0] == "2"):
			comando.pop(0)
			comando.insert(0,"df")
		elif (comando[0] == "3"):
			comando.pop(0)
			comando.insert(0,"finger")
		elif (comando[0] == "4"):
			comando.pop(0)
			comando.insert(0,"uptime")
		saida = subprocess.check_output(comando)
		return saida
	else:
		return "erro no REQUEST".encode()

def cleanStr(stringUser):
	string = stringUser.replace('>',' ')
	string = string.replace('|',' ')
	clearStr = string.replace(';',' ')
	return clearStr

def threadfunction(connectionSocket):
	sentence = connectionSocket.recv(10000)
	strlimpa = cleanStr(sentence.decode())
	comandoexecutado = executestr(strlimpa)
	msgfinal = "RESPONSE " + comandoexecutado.decode()
	connectionSocket.send(msgfinal.encode())
	connectionSocket.close()

#main
from socket import *
import threading
import subprocess

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ("The server is ready to receive")
while 1:
	connectionSocket, addr = serverSocket.accept()
	#inicio da thread
	t = threading.Thread(target=threadfunction, args=(connectionSocket, ))
	t.daemon = True
	t.start()
