from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png

grammar1 = '''
// Regras Sintaticas
start: sentido intervalos

intervalos: intervalo (intervalo)*

intervalo: PE NUMERO VIR NUMERO PD

sentido: MAIS
        | MENOS

// Regras Lexicográficas
MAIS:"+"
MENOS:"-"
NUMERO:/[-?0-9]+/
PE:"["
PD:"]"
VIR:","

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase = "+[-40,-30][0,9][40,50]"

p = Lark(grammar1) # cria um objeto parser

tree = p.parse(frase)  # retorna uma tree

print(tree.pretty())

class CalculosIntervalos(Transformer):
  def __init__(self):
    self.sinal=1
    self.amplitude=0
    self.menor=None
    self.maior=None

  def start(self,elementos):
    print("start",elementos)
    return elementos

  def sentido(self,sentido):
    print("sentido",sentido[0].value)
    if sentido[0].value == '-':
      self.sinal=-1
    return Discard

  def intervalos(self,intervalos):
    print("intervalos",intervalos)
    # verificacao intervalos maior e menor
    for i in range(len(intervalos)):
        # intervalo maior
        if (self.maior is None or intervalos[i][1] - intervalos[i][0] > self.maior[1] - self.maior[0]) and self.sinal == 1:
            self.maior = intervalos[i]
        elif (self.maior is None or intervalos[i][0] - intervalos[i][1] > self.maior[0] - self.maior[1]) and self.sinal == -1:
            self.maior = intervalos[i]
        # intervalo menor
        if (self.menor is None or intervalos[i][1] - intervalos[i][0] < self.menor[1] - self.menor[0]) and self.sinal == 1:
            self.menor = intervalos[i]
        elif (self.menor is None or intervalos[i][0] - intervalos[i][1] < self.menor[0] - self.menor[1]) and self.sinal == -1:
            self.menor = intervalos[i]
    print("Maior Intervalo",self.maior)
    print("Menor Intervalo",self.menor)
    # amplitude dos intervalos
    self.amplitude = abs(intervalos[-1][1] - intervalos[0][0])
    print("Amplitude",self.amplitude)
    return intervalos

  def intervalo(self,intervalo):
    print("intervalo",intervalo)
    return intervalo

  def NUMERO (self,numero):
    print("NUMERO",numero)
    return int(numero)

  def PE(self,pe):
    print("PE",pe)
    return Discard

  def PD(self,pd):
    print("PD",pd)
    return Discard

  def VIR(self,vir):
    print("VIR",vir)
    return Discard

class TransformerIntervalos(Transformer):
  def __init__(self):
    self.sinal=1
    self.erros = False

  def start(self,elementos):
    print("start",self.erros)
    return self.erros

  def sentido(self,sentido):
    print("sentido",sentido[0].value)
    if sentido[0].value == '-':
      self.sinal=-1
    return Discard

  def intervalos(self,intervalos):
    print("intervalos",intervalos)
    for i in range(len(intervalos) - 1):
        # verificacao dos intervalos
        if (intervalos[i][1] >= intervalos[i+1][0] and self.sinal == 1) or (intervalos[i][1] <= intervalos[i+1][0] and self.sinal == -1):
            print("Intervalo invalido. Razão - intervalos desalinhados/sobrepostos:",intervalos[i],intervalos[i+1])
            self.erros = True
            return Discard
    return intervalos

  def intervalo(self,intervalo):
    print("intervalo",intervalo)
    # verificar intervalo atual
    if (intervalo[0] > intervalo[1] and self.sinal == 1) or (intervalo[0] < intervalo[1] and self.sinal == -1):
      print("Intervalo invalido. Razão - irregularidade no intervalo de acordo com sinal:",intervalo)
      self.erros = True
      return Discard
    return intervalo

  def NUMERO (self,numero):
    print("NUMERO",numero)
    return int(numero)

  def PE(self,pe):
    print("PE",pe)
    return Discard

  def PD(self,pd):
    print("PD",pd)
    return Discard

  def VIR(self,vir):
    print("VIR",vir)
    return Discard

data = TransformerIntervalos().transform(tree)
if not data:
    data = CalculosIntervalos().transform(tree)
print(f"saida :{data}")