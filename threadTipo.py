import threading
#from threading import Thread
from conta import Conta
import time
#threadLock = threading.Lock()

#Importa o mecanimos para sincronizar todas as threads de foma individual ou simultaneamente
condicao = threading.Condition()
#Descrição dos metodos:
# acquire() => sincroniza uma thread 
# realize() => finaliza a sincroniza
# wait() => coloca uma thread em espera
# notify() e notifyAll() => tira uma ou todas as threads no modo de espera

deposito = 2

class ThreadTipo(threading.Thread):
  def __init__ (self, nome, valorConta, tempoVerificacao, tipoThread, conta):
    self.nome =nome
    self.valorConta = valorConta
    self.tempoVerificacao = tempoVerificacao
    self.tipoThread = tipoThread
    self.conta = conta
    self.qtdSaqueOuDeposito = 0
    self.stop = False
    print('Thread: ['+self.nome+'] criada')
    threading.Thread.__init__(self)
    #self.threadEvent = threading.Event()

  #Metodo para exibir o relátorio de uma thread
  def threadReport(self):
    print('\n')
    print('=================== Relatório de saque da Thread: ['+self.nome+'] ===================')
    print("Total de saques efetuados: "+ str(self.qtdSaqueOuDeposito))
    valor = self.qtdSaqueOuDeposito * self.valorConta
    if self.tipoThread == 'C':
      print('Quantidade de saques: '+str( valor) )
    else:
      print('Quantidade de depositos: '+str( valor) )
    print('=================== Fim do Relatório da Thread: [%s]  ==================='% self.nome)
    print('\n')

  #Metodo que realiza o depósito em uma conta
  def depositar(self,condicao):
      condicao.acquire() 
      print('Thread: [%s] Hora do deposito' % self.nome )
      if( self.qtdSaqueOuDeposito < deposito ):
        self.qtdSaqueOuDeposito += self.conta.deposito(self.valorConta,self.nome)
      else:
        self.stop = True
      
      condicao.notifyAll()
      condicao.release()

  #Medotdo que define o fluxo da atividade de realizar saque  
  def taskSaque(self,condicao):
    # Valida se a conta está disponível para saques

    while( self.conta.getSaldo() > 0 and self.conta.disponivel(self.valorConta,self.nome, self.tipoThread) ):
      condicao.acquire()
      if( self.conta.disponivel(self.valorConta,self.nome, self.tipoThread) ):  
        self.qtdSaqueOuDeposito += self.conta.saque(self.valorConta,self.nome,self.tipoThread)
        time.sleep(self.tempoVerificacao)

      condicao.release()

    # Se a conta não estiver disponível para saques a thread entrará em estado de espera
    # Somente as threads comsumidoras entrão em estado de espera
    condicao.acquire()  
    if(self.tipoThread == 'C'):
      self.conta.setNrThreadWait(1);
      print('Thread: ['+self.nome+'] irá entrar em estado de espera, pois não pode mais realizar saques...')
      self.threadReport()
      condicao.wait()
    condicao.release()

  #Metodo que define o fluxo da atividade de realizar deposito   
  def taskDeposito(self):
    if(self.tipoThread == 'P'):
      #Atuliza  a situação de deposito
      self.conta.atzSitDeposito()
      print('Thread: [%s] verificando a situacao da conta para depositar:[%s]' % (self.nome, str(self.conta.getDepositTime()) ) )
      if(self.conta.getDepositTime()):
        self.depositar(condicao)
      time.sleep(self.tempoVerificacao)

  #Foi um metodo que criei para tentar para o fluxo após um periodo, mas deu ceto n :(
  def finalizar(self):
    if(self.tipoThread == 'P' and self.stop): 
      condicao.acquire() 
      condicao.notifyAll()
      condicao.release()
      return True
    else:
      return False

  #Metodo Principal
  def run(self):
    while( not self.finalizar()):
      self.taskSaque(condicao)
      self.taskDeposito()

    if(self.tipoThread == 'P' and self.stop):
      print('Thread: [%s] já realizou %d depositos' % (self.nome, self.qtdSaqueOuDeposito ) )

    

