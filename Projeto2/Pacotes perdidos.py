import random
#gerar numeros aleatorios que sejam menores a ou iguais a medida de chance ou "probabilidade" de um pacote ter sido perdido  
# 
def lostPack(prob_loss):

   global lostNum
   global pack_lost
    
               perda_aleatorio = random.randint(0,1000)       
               if perda_aleatorio < = prob_loss:
                       print(" o pacote que foi perdido e: = ", requestNumber)
                       pack_lost = True
                       if len(lostNum) == 0:
                           lostNum.append(resquestNumber)
                       if len(lostNum) > 0:
                           if requestNumber not in lostNum and (requestNumber>min(lostNum)):
                              lost_seq_num.append(seq_num) 
      