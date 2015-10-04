##HOST = '127.0.0.1'     # Endereco IP do Servidor
##PORT = 12000            # Porta que o Servidor esta
##tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##dest = (HOST, PORT)
##tcp.connect(dest)
##print ('Digite o comando\n') 
##msg = input()
##tcp.send (msg.encode())
##msg2 = tcp.recv(1024)
##print (msg2)
##tcp.close()

# main
##def splitRequest_1(s):
##    t = s.split()    
##    ans = "REQUEST "
##    pattern = "PC"
##    for index, item in enumerate(t):   # index = 0 , item "PC1"        
##        if item.startswith(pattern):
##            i = 0
##            while not t[i+1].startswith(pattern):
##                ans = ans + t[i+1] + ' '
##                print(t)
##                t.pop(0)                
##                input()
##            print (ans)
##        if t[0][2] == '1': pcNumber = 1
##        elif t[0][2] == '2': pcNumber = 2
##        elif t[0][2] == '3': pcNumber = 3

##def split_by_cmd(t):
##    req = "REQUEST "
##    p = re.compile(r'\W+')
##    print(p.split(t))

##def get_pc_number(cmd_atual):
##    if cmd_atual[0] == 'PC1': return 1
##    if cmd_atual[0] == 'PC2': return 2
##    if cmd_atual[0] == 'PC3': return 3

##def connect_to_daemon(s, _pc, _port):
##    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##    dest = (_pc, _port)
##    tcp.connect(dest)
##    tcp.send (s.encode())
##    s = tcp.recv(4096)
##    tcp.close()
##    return s

import socket
import re

# ips das maquinas
_pc1 = "localhost"
_pc2 = "localhost"
_pc3 = "localhost"

# porta
_port = 12000

# string teste
a = "PC1\tps -ef\tdf -d\tfinger\tuptime\tps -zx\tps -aux\nPC2\tuptime\nPC3\tfinger"

def backend_func(s):
    s = s.split('\n')    #s = ['PC1\tps -ef\tdf -d\tfinger\tuptime', 'PC2\tuptime', 'PC3\tfinger']    
    for i in range(0, len(s)):  #para cada daemon
        cmds_daemon_atual = s[i].split('\t') #e.g. cmd_atual[0] = ['PC1', 'ps -ef', 'df -d', 'finger', 'uptime']
        daemon_atual = cmds_daemon_atual[0] # armazena pc atual
        cmds_daemon_atual.pop(0) #remove da lista para facilitar

        #print("Daemon atual: ",daemon_atual)
        #print("Comandos Daemon atual: ",cmds_daemon_atual)

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #conecta com o daemon
        dest = (get_daemon_ip(daemon_atual), _port) #define o ip de acordo com o numero do pc (daemon executando)        
        tcp.connect(dest) #handshake com o daemon

        req = ''
        resp = ''
        
        for cmd_atual in cmds_daemon_atual: #para cada comando no mesmo daemon

            #substitui os comandos por numeros
            if cmd_atual.startswith('ps'):
                cmd_atual = cmd_atual.replace('ps', '1') 
                nro_cmd = '1 ' #armazena o nro do cmd para utilizar em RESPONSE
            elif cmd_atual.startswith('df'):
                cmd_atual = cmd_atual.replace('df', '2')
                nro_cmd = '2 '
            elif cmd_atual.startswith('finger'):
                cmd_atual = cmd_atual.replace('finger', '3')
                nro_cmd = '3 '
            elif cmd_atual.startswith('uptime'):
                cmd_atual = cmd_atual.replace('uptime', '4')
                nro_cmd = '4 '

            cmd_atual = cmd_atual.replace('-', '') #remove os hifens dos parametros
            req = 'REQUEST ' + cmd_atual #e.g. "REQUEST 1 ef"
            
            #testes - descomentar
            #print ("maquina ",daemon_atual[2])
            #print (req)

            tcp.send (req.encode())
            resp = 'RESPONSE ' + nro_cmd + tcp.recv(4096).decode()
            
            print (resp)
        tcp.close() #encerra a conexão com o daemon

def get_daemon_ip(daemon_atual):
    if daemon_atual == 'PC1': return _pc1
    elif daemon_atual == 'PC2': return _pc2
    elif daemon_atual == 'PC3': return _pc3    






