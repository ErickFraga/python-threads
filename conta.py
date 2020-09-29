import threading 

# Descrição dos atributos da classe conta
# numero => número identificado da conta
# titular => nome do proprietário da conta
# saldo => valor disponível na conta para saques
# depositTime => indica se a conta está no momento correto para o depósito
# nrThreadWait => indica o número de threads que estão em espera, por não poder mais sacar
 
class Conta():
  def __init__(self, numero, titular, saldo):
    self.numero = numero
    self.titular = titular
    self.saldo = saldo
    self.depositTime = False
    self.nrThreadWait =0

  def getNrThreadWait(self):
    return self.nrThreadWait

  def setNrThreadWait(self,num):
    self.nrThreadWait = num

  def getTitular(self):
    return self.titular
  
  def getNumero(self):
    return self.numero

  def getSaldo(self):
    return self.saldo
  #Metodo que realiza a ação de depósito
  def deposito(self,quantia, tNome):
    self.saldo += quantia
    print("Thread: ["+tNome+"] Depositou: "+str(quantia)+" R$ Saldo restante: "+str(self.saldo)+"R$")
    self.setNrThreadWait(0)
    self.setDepositTime(False)
    return 1

  def getDepositTime(self):
    return self.depositTime
  
  def setDepositTime(self, value):
    self.depositTime = value

  def toString(self):
    return 'Conta: '+str(self.numero)+' Saldo disponível: '+str(self.saldo)+' R$ Proprietário(a): Sr(a) '+self.titular
  #Metodo para atualiza a situação de depósito
  def atzSitDeposito(self):
    if self.getSaldo() == 0 or self.getNrThreadWait() == 3:
      self.setDepositTime(True)

  #Verifica a possibilidade de efetuar um saque
  def disponivel(self,quantia,tNome,tTipo):
    if(self.saldo >= quantia and tTipo == 'C'):
      return True
    elif tTipo == 'C':
      #self.nrThreadWait += 1
      # Determina se é hora de depositar novamente na conta 'depositTime'
      # Como são 3 threads caso elas entrem em espera, significa que também é hora de depositar
      if self.getSaldo() == 0 or self.getNrThreadWait() == 3:
        self.setDepositTime(True)
        
      return False
    else:
      return False
  

  def saque(self, quantia, tNome,tTipo):
    if(tTipo == 'C'):
      self.saldo = self.saldo - quantia
      print("Thread: ["+tNome+"] Sacou: "+str(quantia)+" R$ Saldo restante: "+str(self.saldo)+"R$")
      return 1
    else:
      return 0

