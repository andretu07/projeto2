from socket import *
import threading
import subprocess

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
			saidaValida = False

		if(saidaValida):
			comando = cleanStr(comando)
			comando = comando.replace(' ',' -',1)
			comando = comando.split(None, 2)
			if(len(comando) == 2):
				print ("DAEMON processou:",comando[0], comando[1])
			else:
				print ("DAEMON processou:",comando[0])
			try:
				saida = subprocess.check_output(comando[0:2]).decode()
			except subprocess.CalledProcessError:
				operacao = "0"
				return "\n"
			return saida
		else:
			operacao = "0"
			return "\n"
	else:
		operacao = "0"
		return "\n"

def cleanStr(stringUser):
	erro = len(stringUser)
	outro_erro = stringUser.find(';')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)
	outro_erro = stringUser.find('&')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)
	outro_erro = stringUser.find('|')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)
	outro_erro = stringUser.find('>')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)
	outro_erro = stringUser.find('<')
	if(outro_erro > 0):
		erro = min(erro,outro_erro)


	return stringUser[0:erro]

def threadfunction(connectionSocket):	
	connectionSocket.settimeout(60)
	try:
		while 1:
			sentence = connectionSocket.recv(4096).decode()
			print ("Daemon recebeu:", sentence)
			comando_executado = parse_and_execute(sentence)
			msgfinal = "RESPOND " + operacao + comando_executado
			connectionSocket.send(msgfinal.encode())
	except timeout:
		connectionSocket.close()

#main
daemonPort = 12000
daemonSocket = socket(AF_INET,SOCK_STREAM)
try:
	daemonSocket.bind(('',daemonPort))
except:
	print("Porta Ocupada. Espere um momento ou tente outra porta.")
	exit(0)
daemonSocket.listen(1)
print ("DAEMON está pronto para uso.")
while 1:
	connectionSocket, addr = daemonSocket.accept()
	#inicio da thread
	t = threading.Thread(target=threadfunction, args=(connectionSocket, ))
	t.daemon = True
	t.start()
