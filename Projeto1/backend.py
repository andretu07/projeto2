import socket

# ips das maquinas
_pc1 = "192.168.0.103"
_pc2 = "192.168.0.103"
_pc3 = "192.168.0.103"

# porta
_port = 12000

def backend_func(s):
    """
    @obj: executar a função do backend; recebe a string do webserver na forma 'PC1\tps -ef\tuptime\nPC2\tuptime\nPC3\tfinger', envia para o(s) Daemons, recebe a resposta e retorna para o webserver
    @params: String 's' (\n separa os computadores que estarão executando o Daemon; \t separa os comandos por Daemon em execução)
    @lastmod: 04/10/2015
    @author: Cristian Pendenza
    @returns: lista contendo a resposta dos daemons no formato e.g. ['PC1 \n cmd1 \n cmd2 \n', 'PC2 \n cmd1', 'PC3 \n cmd2']      
    """    
    s = s.split('\n')    #s = ['PC1\tps -ef\tdf -d\tfinger\tuptime', 'PC2\tuptime', 'PC3\tfinger']    
    reply = []
    tcp = [None] * 3
    for i in range(0, len(s)):  #para cada daemon, de 0 até o numero total de daemons
        cmds_daemon_atual = s[i].split('\t') #divide por comandos (para cada daemon em execução) e.g. cmd_atual[0] = ['PC1', 'ps -ef', 'df -d', 'finger', 'uptime']
        daemon_atual = cmds_daemon_atual[0] # armazena pc atual (string 'PC1', 'PC2' ou 'PC3')
        cmds_daemon_atual.pop(0) #remove a string pc atual da lista para facilitar

        tcp[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #conecta com o daemon
        dest = (get_daemon_ip(daemon_atual), _port) #define o ip de acordo com o numero do pc (daemon executando)        
        tcp[i].connect(dest) #handshake com o daemon

        req = ''       
        resp = ''       

        for cmd_atual in cmds_daemon_atual: #para cada comando no mesmo daemon

            #substitui os comandos por numeros
            if cmd_atual.startswith('ps'):
                cmd_atual = cmd_atual.replace('ps', '1')                 
            elif cmd_atual.startswith('df'):
                cmd_atual = cmd_atual.replace('df', '2')                
            elif cmd_atual.startswith('finger'):
                cmd_atual = cmd_atual.replace('finger', '3')                
            elif cmd_atual.startswith('uptime'):
                cmd_atual = cmd_atual.replace('uptime', '4')                

            req = 'REQUEST ' + cmd_atual #e.g. "REQUEST 1 ef"

            #envia a string pronta atraves do socket
            tcp[i].send (req.encode()) 
            reply.append(tcp[i].recv(16*1024).decode())
            print(reply)

        tcp[i].close() #encerra a conexão com o daemon
    
    return reply

def get_daemon_ip(daemon_atual):
    """
    @obj: receber uma string (PC1, PC2 ou PC3) e devolver string com o numero do ip definido globlalmente nas variáveis _pc1, _pc2 e _pc3
    @params: String 'daemon_atual'    
    @lastmod: 02/10/2015
    @author: Cristian Pendenza
    @returns: string com o ip destino 
    """
    if daemon_atual == 'PC1': return _pc1
    elif daemon_atual == 'PC2': return _pc2
    elif daemon_atual == 'PC3': return _pc3    

#a = 'PC1\tps a\tuptime\nPC2\tuptime\nPC3\tfinger'
#a = 'PC1\tuptime\nPC2\tps'
#print(backend_func(a))

