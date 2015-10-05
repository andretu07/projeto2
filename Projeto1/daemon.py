from socket import *
import threading
import subprocess

operacao = ""

'''
Função executestr(checkstr)
Faz o parse da string recebida e executa o comando do linux referente ao
comando que deseja executar.

Quando o backend envia uma string sem o Requestno começo, a função retorna
quebra-linha

Quando o backend envia uma string sem o número correspondente do comando,
a função retorna quebra-linha

Quando ocorre a exceção CalledProcessError, a função retorna quebra-linha

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
			comando = comando.split(None, 2)
			if(len(comando) == 2):
				print ("DAEMON processou:",comando[0], comando[1])
			else:
				print ("DAEMON processou:",comando[0])
			try:
				saida = subprocess.check_output(comando[0:2]).decode()
			except subprocess.CalledProcessError:
				operacao = "0"
				return "O comando não pôde ser executado."
			return saida
		else:
			operacao = "0"
			return "O número do comando é inválido."
	else:
		operacao = "0"
		return "A requisição não está no formato adequado"
'''
Função cleanStr(stringUser)
Devolve uma fatia da string na qual não tem os caracteres não desejados (; & | > <) do
começo dela até uma posição anterior do caracter. 
'''
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

'''
Função threadfunction(connectionSocket)
Função da thread que recebe a string do backend, faz um parse, executa
o comando requisitado e envia de volta ao backend.

Fecha a conexão do socket após 60 segundos de conexão aberta. 
'''
def threadfunction(connectionSocket):	
	connectionSocket.settimeout(60)
	try:
		while 1:
			sentence = connectionSocket.recv(1024).decode()
			if (len(sentence) == 0):
				return
			print ("Daemon recebeu:", sentence)
			comando_executado = parse_and_execute(sentence)
			msgfinal = str("RESPONSE " + operacao + comando_executado)
			connectionSocket.send(msgfinal.encode())
	except timeout:
		connectionSocket.close()
	except:
		print("")


#Main - preparação do server
daemonPort = 12000
daemonSocket = socket(AF_INET,SOCK_STREAM)
daemonSocket.bind(('',daemonPort))
daemonSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
daemonSocket.listen(1)
print ("DAEMON está pronto para uso.")
while 1:
	connectionSocket, addr = daemonSocket.accept()
	#inicio da thread - para receber multi-usuários
	t = threading.Thread(target=threadfunction, args=(connectionSocket, ))
	t.daemon = True
	t.start()
