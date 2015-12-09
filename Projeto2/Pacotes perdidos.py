# esta funcao deve rodar dentro do servidor porém ela apresenta alguns erros na compilacao por isso resolvi postar separado do server.py
import random
#gerar numeros aleatorios que sejam menores a ou iguais a medida de chance ou "probabilidade" de um pacote ter sido perdido  
# 
def lostPack(prob_loss):

   global lostNum
   global pack_lost
               # gera numeros aleatorio entre 0 e 100
               perda_aleatorio = random.randint(0,100) 
               # verifica se o numero do pacote é menor ou igual a probabilidade de um pacote ser perdido
               if perda_aleatorio < = prob_loss:
                  # se o pacote foi perdido ele envia uma mensagem com o numero do pacote perdido
                       print(" o pacote que foi perdido e: = ", requestNumber)
                        # o pack_lost que comecou como falso recebe o valor true
                       pack_lost = True
                       # se a lista de pacotes perdidos for igual a zero como de inicio  mete o requestNumber na lista pacotes perdidos
                       if len(lostNum) == 0:
                           lostNum.append(resquestNumber)
                     # se ja tiver algum o requestNumber de algum pacote verifica se o requestNumber do pacote actual ja se encontra na lista de pacotes perdidos e se é menor que o requestNumber do menor pacote que ja foi perdiso 
                       if len(lostNum) > 0:
                           if requestNumber not in lostNum and (requestNumber>min(lostNum)):
                              # em caso positivo recebe o requestenumber do pacote perdido
                              lostNum.append(requestNumber) 
      
