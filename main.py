# -*- coding: utf-8 -*-
import threading 
from threadTipo import ThreadTipo
from conta import Conta

# - Decisões:
# Para a sincronisação criamos 2 objetos, o "semáforo" que é instanciado no arquivo main
# e define a quantidade de threads no processo, outro objeto é o "condicao" que realiza o 
# controle das threads, entrada na espera, saída da espera e a "Sincronização" dos blocos de 
# código permitindo assim apenas uma única thread no intervalo entre "condicao.acquire()" e 
# "condicao.release()"
#
# A idéia é trabalhar com duas tasks uma para realizar as operações de saques e outra para realizar
# os depósitos na conta 


#Definindo o número de threads para o processo
semaforo = threading.Semaphore(4)

# C = thread AGastadora
# C = thread AEconomica
# C = thread AEsperta
# P = thread APatrocinadora


print("FUNCIONAMENTO DA CONTA BANCÁRIA\n")
contaCompartilhada = Conta(123,'Ribamar Pedreiro',1000.00)

print( contaCompartilhada.toString() )

AGastadora = ThreadTipo("AGastadora",10,3,'C',contaCompartilhada)
AEsperta = ThreadTipo("AEsperta",50,6,'C',contaCompartilhada)
AEconomica = ThreadTipo("AEconomica",5,12,'C',contaCompartilhada)
APatrocinadora = ThreadTipo("APatrocinadora",100,2,'P',contaCompartilhada)

threads =[] 
threads.append(AGastadora)
threads.append(AEsperta)
threads.append(AEconomica)
threads.append(APatrocinadora)

for i in threads:
  semaforo.acquire()
  i.start()
  
semaforo.release()

# metodo join()  utilizado para aguardar a thread finalizar para voltar ao fluzo do código principal
for j in threads:
  j.join()