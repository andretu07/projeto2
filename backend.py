import socket
import re

# ips das maquinas
_pc1 = "127.0.0.1"
_pc2 = "127.0.0.1"
_pc3 = "127.0.0.1"

# porta
_port = 12000

def backend_func(s):
    s = s.split('\n')    #s = ['PC1\tps -ef\tdf -d\tfinger\tuptime', 'PC2\tuptime', 'PC3\tfinger']    
    for i in range(0, len(s)):  #para cada daemon
        cmds_daemon_atual = s[i].split('\t') #e.g. cmd_atual[0] = ['PC1', 'ps -ef', 'df -d', 'finger', 'uptime']
        daemon_atual = cmds_daemon_atual[0] # armazena pc atual
        cmds_daemon_atual.pop(0) #remove da lista para facilitar

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #conecta com o daemon
        dest = (get_daemon_ip(daemon_atual), _port) #define o ip de acordo com o numero do pc (daemon executando)        
        tcp.connect(dest) #handshake com o daemon

        req = ''
        resp = ''
        
        for cmd_atual in cmds_daemon_atual: #para cada comando no mesmo daemon

            #substitui os comandos por numeros
            if cmd_atual.startswith('ps'):
                cmd_atual = cmd_atual.replace('ps', '1') 
                nro_cmd = '1 ' #armazena o nro do cmd para utilizar
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

            tcp.send (req.encode()) #envia a string pronta atraves do socket
            resp = 'RESPONSE ' + nro_cmd + tcp.recv(4096).decode() #recebe e decodifica a string
        tcp.close() #encerra a conexão com o daemon

def get_daemon_ip(daemon_atual):
    if daemon_atual == 'PC1': return _pc1
    elif daemon_atual == 'PC2': return _pc2
    elif daemon_atual == 'PC3': return _pc3    

#teste
a = "PC1\tps -ef\tuptime\nPC2\tuptime\nPC3\tfinger"
backend_func(a)



