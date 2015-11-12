from socket import *
import sys

#if len(sys.argv) != 4:
#	print("python3 client.py <hostname_do_rementente> <numero_de_porta_do_rementente> <nome_do_arquivo>")
#else:
#	print (sys.argv[0]) # prints python_script.py
#	print (sys.argv[1]) # prints var1
#	print (sys.argv[2]) # prints var2
#	print (sys.argv[3]) # prints var2
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
#nome do arquivo a receber
message = "ariehfabbro".encode()
clientSocket.sendto(message,(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print (modifiedMessage.decode())
clientSocket.close()
