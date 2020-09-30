import threading
from conta import Conta
import time

#Importa o mecanimos para sincronizar todas as threads de foma individual ou simultaneamente
condicao = threading.Condition()
#Descrição dos metodos:
# acquire() => sincroniza uma thread 
# realize() => finaliza a sincroniza
# wait() => coloca uma thread em espera
# notify() e notifyAll() => tira uma ou todas as threads no modo de espera



class ThreadTipo(threading.Thread):
  def __init__ (self, nome, valorConta, tempoVerificacao, tipoThread, conta):
    self.nome =nome
    self.valorConta = valorConta
    self.tempoVerificacao = tempoVerificacao
    self.tipoThread = tipoThread
    self.conta = conta
    self.qtdSaqueOuDeposito = 0
    print('Thread: ['+self.nome+'] criada')
    threading.Thread.__init__(self)

  # Método para exibir o relátorio de uma thread
  def threadReport(self):
    print('\n')
    print('=================== Relatório de saque da Thread: ['+self.nome+'] ===================')
    print("Quantidade de saques efetuados: "+ str(self.qtdSaqueOuDeposito))
    valor = self.qtdSaqueOuDeposito * self.valorConta
    if self.tipoThread == 'C':
      print('Total que foi sacado: '+str( valor) +' R$')
    else:
      print('Quantidade de depositos: '+str( valor) )
    print('=================== Fim do Relatório da Thread: [%s]  ==================='% self.nome)
    print('\n')

  # Método que realiza o depósito em uma conta
  def depositar(self,condicao):
      condicao.acquire() 
      print('Thread: [%s] Hora do deposito' % self.nome )
      self.qtdSaqueOuDeposito += self.conta.deposito(self.valorConta,self.nome)
      condicao.notifyAll()
      condicao.release()

  # Método que define o fluxo da atividade de realizar saque  
  def taskSaque(self,condicao):
    # Valida se a conta está disponível para saques
    while( self.conta.getSaldo() > 0 and self.conta.disponivel(self.valorConta,self.nome, self.tipoThread) ):
      time.sleep(self.tempoVerificacao)
      condicao.acquire()
      if( self.conta.disponivel(self.valorConta,self.nome, self.tipoThread) ):  
        self.qtdSaqueOuDeposito += self.conta.saque(self.valorConta,self.nome,self.tipoThread)

      condicao.release()

    # Se a conta não estiver disponível para saques a thread entrará em estado de espera
    # Somente as threads comsumidoras entrão em estado de espera
    condicao.acquire()  
    if(self.tipoThread == 'C'):
      print('\n')
      self.conta.setNrThreadWait(1);
      print("Thread: [" +self.nome+"] impossibilitada de sacar: "+str(self.valorConta)+ "R$, Erro: saldo insuficiente na conta: "+str(self.conta.getNumero())+" saldo Atual: "+str( self.conta.getSaldo())+"R$" )
      print('Thread: ['+self.nome+'] irá entrar em estado de espera, pois não pode mais realizar saques...')
      self.threadReport()
      condicao.wait()
    condicao.release()

  # Método que define o fluxo da atividade de realizar deposito   
  def taskDeposito(self):
    if(self.tipoThread == 'P'):
      # Atualiza  a situação de deposito
      time.sleep(self.tempoVerificacao)
      self.conta.atzSitDeposito()

      if(self.conta.getDepositTime()):
        self.depositar(condicao)

  # Método Principal que é chamda pelo start()
  def run(self):
    while(True):
      self.taskSaque(condicao)
      self.taskDeposito()

    