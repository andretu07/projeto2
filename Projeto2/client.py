#!/usr/bin/python3

from socket import *
import hashlib
import struct
import sys

"""
Cada pacote eh uma lista com os varios campos do protocolo TCP
Sao eles:
1 campo: sequence number(server)/ack number(client)
2 campo: checksum
3 campo: finbit - determina se ha dados para enviar (1 para dizer que ha)
4 campo: dados propriamente ditos
5 campo: Probabilidade de corrupção
"""

"""
def createPackage(seqAckNumber, checksum, finbit, data):
    return "+++".join((str(seqAckNumber), str(checksum), str(finbit), data))

"""

dev = sys.argv

# Foi acrescentado dois campo a mais em createPackage, um campo que conterá a probabilidade de perda de
# pacotes e um outro campo com a probabilidade de corrupção de pacotes.
def createPackage(seqAckNumber, checksum, finbit, data, probPerdaDePacotes, probCorrupcaoDePacotes):
    return "+++".join((str(seqAckNumber), str(checksum), str(finbit), data, str(probPerdaDePacotes), str(probCorrupcaoDePacotes)))

def getFieldPackage(package, number):
    field = package.split("+++")
    return field[number]

def checkChecksum(package):
    arq = getFieldPackage(package, 3)
    hash = hashlib.md5()
    hash.update(arq.encode())
    checksum = hash.hexdigest()
    return checksum == getFieldPackage(package, 1)

#if len(sys.argv) != 4:
#    print("python3 client.py <hostname_do_rementente> <numero_de_porta_do_rementente> <nome_do_arquivo>")
#else:
#    print (sys.argv[0]) # prints python_script.py
#    print (sys.argv[1]) # prints var1
#    print (sys.argv[2]) # prints var2
#    print (sys.argv[3]) # prints var3


"""
N  = window size
Rn = request number - Qual numero de pacote que o cliente está solicitando ao servidor
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

# Inicializa os valores de corrupção e de perda de pacotes para três pacotes.
# os valores apropriados são de 0 a 0,40. Pacotes com valores fora desse intervalo
# serão considerados corrompidos ou perdidos.
probPerdaPacote1 = 0.0
probPerdaPacote2 = 0,50    # Pacote com corrupção
probPerdaPacote3 = 0,10

probCorrupPacote1 = 0.0
probCorrupPacote2 = 0.50 # Pacote com perda
probCorrupPacote3 = 0.15

#nome do arquivo a receber
#message = createPackage(requestNumber, 0, 0, "teste.txt")

# Criação dos pacotes:
# Cria um pacote com a probabilidade 1
message1 = createPackage(requestNumber, 0, 0, "projeto2.pdf", probPerdaPacote1, probCorrupPacote1)
# Cria um pacote com a probabilidade 2 - Pacote com corrupção e perda
message2 = createPackage(requestNumber + 1, 0, 0, "projeto2.pdf", probPerdaPacote2, probCorrupPacote2)

#Envia a mensagem1 para o servidor e faz a verificação de corrupção
print ("Pedido o pacote " + str(requestNumber))
clientSocket.sendto(message1.encode(),(serverName, serverPort))
response, clientAddress = clientSocket.recvfrom(2048)
error = getFieldPackage(response.decode(), 3)
stopError = getFieldPackage(response.decode(), 2)
if error == "200 OK":
    while int(stopError) != 1:
        response, clientAddress = clientSocket.recvfrom(2048)
        # Se o pacote é livre de erro então aceita o pacote e envia o número de pacote que o cliente está
        # solicitando ao servidor.
        if ((int(getFieldPackage(response.decode(), 4)) >= 0) or (int(getFieldPackage(response.decode(), 4)) <= 0.40)): # pacote com perda
            arquivo.append(getFieldPackage(response.decode(), 3))
            print("Recebido o " + str(getFieldPackage(response.decode), 1))
            # Pede o proximo pacote
            #print("Pedido o pacote " + )
        else: # Pacote está corrompido - recusa o pacote e envia uma nova solicitação ao servidor
            print("Pacote corrompido: ")
            print ("Pedindo o pacote novamente ao servidor: ")
            # Pacote estou corrompido, realiza uma nova solicitação ao servidor
            print("pacote " + str(requestNumber + "corrompido"))
            print("Enviando nova solicitação para RN......")
            clientSocket.sendto(message.encode(), (serverName, serverPort))
            print("Solicitação enviada")
        stopError = getFieldPackage(response.decode(), 2)
    arquivo = "".join(arquivo)
    #with open("teste3.txt", 'wb') as f:
    with open("projeto2.pdf", 'wb') as f:
        f.write(arquivo.encode("ISO-8859-1"))
    print("Arquivo criado com sucesso!")
    clientSocket.close()
else:
    print("Arquivo nao encontrado")
    clientSocket.close()
                    
              

"""print ("Pedido o pacote " + str(requestNumber))
clientSocket.sendto(message.encode(),(serverName, serverPort))
response, clientAddress = clientSocket.recvfrom(2048)
error = getFieldPackage(response.decode(), 3)
stopError = getFieldPackage(response.decode(), 2)
if error == "200 OK":
    while int(stopError) != 1:
        response, clientAddress = clientSocket.recvfrom(2048)
        # Se o pacote é livre de erro então aceita o pacote e envia o número de pacote que o cliente está
        # solicitando ao servidor.
        if requestNumber == int(getFieldPackage(response.decode(), 0)) and checkChecksum(response.decode()):
            arquivo.append(getFieldPackage(response.decode(), 3))
            print ("Recebido o pacote " + str(requestNumber))
            requestNumber += 1
            message = createPackage(requestNumber, 0, 0, "ada")
            print ("Pedido o pacote " + str(requestNumber))
            clientSocket.sendto(message.encode(),(serverName, serverPort)) # socket.sendto(string, address)

            # Parte que faz o envio do ack para o servidor
            #pega o sequenceNumber/Ack do pacote
            sn = getFieldPackage(message, 1)
            # Faz o envio do ack para o servidor
            clientSocket.sendto(sn, (ServerName, serverPort))

        # Se o pacote estiver corrompido recusar o pacote e envia uma nova solicitação ao servidor
        else: 
            # Pacote estou corrompido, realiza uma nova solicitação ao servidor
            print("pacote " + str(requestNumber + "corrompido"))
            print("Enviando nova solicitação para RN......")
            clientSocket.sendto(message.encode(), (serverName, serverPort))
            print("Solicitação enviada")
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

"""