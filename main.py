# -*- coding: utf-8 -*-
import threading 
from threadTipo import ThreadTipo
from conta import Conta


semaforo = threading.Semaphore(4)

# C = thread AGastadora
# C = thread AEconomica
# C = thread AEsperta
# P = thread APatrocinadora

print("FUNCIONAMENTO DA CONTA BANCÁRIA\n")
contaCompartilhada = Conta(123,'Ribamar Pedreiro',100.00)

print( contaCompartilhada.toString() )

AGastadora = ThreadTipo("AGastadora",10,3,'C',contaCompartilhada)
AEsperta = ThreadTipo("AEsperta",50,6,'C',contaCompartilhada)
AEconomica = ThreadTipo("AEconomica",5,12,'C',contaCompartilhada)
APatrocinadora = ThreadTipo("APatrocinadora",500,2,'P',contaCompartilhada)

threads =[] 
threads.append(AGastadora)
threads.append(AEsperta)
threads.append(AEconomica)
threads.append(APatrocinadora)

for i in threads:
  semaforo.acquire()
  i.start()
  
semaforo.release()
#AGastadora.start();
#AEsperta.start();
#AEconomica.start();
#APatrocinadora.start();

# metodo join() aguarda a thread finalizar para voltar ao código principal
AGastadora.join(); 
AEsperta.join();
AEconomica.join();
APatrocinadora.join();
print('\n')
print('\n')
print('\n')


print("============================== fim ================================")