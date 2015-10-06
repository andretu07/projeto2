import threading
from socket import *
from subprocess import *

operacao = ""

'''
Função executestr(checkstr)
Faz o parse da string recebida e executa o comando do linux referente ao
comando que deseja executar.

Quando o backend envia uma string sem o Requestno começo, a função retorna
quebra-linha

Quando o backend envia uma string sem o número correspondente do comando,
a função retorna quebra-linha

Se o programa não consegue executar o comando, gera uma exceção e retorna erro.

'''
def parse_and_execute(sentence):
	global operacao

	if (len(sentence) > 7 and sentence[0:7] == "REQUEST"):
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
			comando = comando.split()
			print ("DAEMON processou:",comando);
			try:
				proc = Popen(comando, stdout=PIPE, stderr=PIPE)
				out, err = proc.communicate()
				saida = (out + err).decode()
			except:
				operacao = "0 "
				saida = "O comando não pôde ser executado.\n"
			return saida
		else:
			operacao = "0 "
			return "O número do comando é inválido.\n"
	else:
		operacao = "0 "
		return "A requisição não está no formato adequado.\n"
'''
Função cleanStr(stringUser)
Devolve uma fatia da string na qual não tem os caracteres não desejados (; & | > <) do
começo dela até uma posição anterior do caracter. 
'''
def cleanStr(stringUser):
	erro = len(stringUser)
	outro_erro = stringUser.find(';')
	if(outro_erro > 0):
		stringUser = stringUser[0:erro]
	outro_erro = stringUser.find('&')
	if(outro_erro > 0):
		stringUser = stringUser[0:erro]
	outro_erro = stringUser.find('|')
	if(outro_erro > 0):
		stringUser = stringUser[0:erro]
	outro_erro = stringUser.find('>')
	if(outro_erro > 0):
		stringUser = stringUser[0:erro]
	outro_erro = stringUser.find('<')
	if(outro_erro > 0):
		stringUser = stringUser[0:erro]
	return stringUser

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
			sentence = connectionSocket.recv(1024).decode().replace("\r\n", "")
			if (len(sentence) == 0):
				return
			print ("Daemon recebeu:", sentence)
			comando_executado = parse_and_execute(sentence)
			msgfinal = str("RESPONSE " + operacao + comando_executado)
			connectionSocket.send(msgfinal.encode())
	except timeout:
		connectionSocket.close()
	#Erro na decodificação do unicode. Ignorar.
	except:
		None

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
