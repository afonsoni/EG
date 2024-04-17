#!pip install lark
from lark import Lark,Token,Tree,Discard
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self):
        self.sinal = "+"
        self.amplitudes = []
        self.first = None
        self.last = None
        self.amplitude = 0

    def start(self, tree):
        print("Entrei na raíz, vou visitar os filhos (intervalos)")
        self.sinal = self.visit(tree.children[0])
        self.visit(tree.children[1])
        self.amplitude = abs(self.last - self.first)
        print("Intervalos visitados, vou regressar à main()")
        print("Sinal: ",self.sinal)
        print("Amplitude total: ",self.amplitude)
        print("Amplitudes: ",self.amplitudes)
        print("First: ",self.first)
        print("Last: ",self.last)

    def sentido(self, tree):
        return tree.children[0].value

    def intervalos(self, tree):
        print(tree.pretty())
        r = self.visit_children(tree)
        print("visit children : ",r)
        return r

    def intervalo(self, tree):
        if self.first is None:
            self.first = int(tree.children[1].value)
        amplitude = abs(int(tree.children[3].value) - int(tree.children[1].value))
        self.amplitudes.append(amplitude)
        self.last = int(tree.children[3].value)
        r = self.visit_children(tree)
        print("elemento",r)
        return r


## Primeiro precisamos da GIC
grammar = '''
start: sentido intervalos
sentido: MAIS
        | MENOS
intervalos: intervalo (intervalo)*
intervalo: PE NUMERO VIR NUMERO PD
MAIS:"+"
MENOS:"-"
NUMERO:"0".."9"+ // [0-9]+
PE:"["
PD:"]"
VIR:","

%import common.WS
%import common.ESCAPED_STRING
%ignore WS
'''

#frase = "-[44,32][23,15][10,5]"
frase = "+[1,23][24,50][51,57]"
p = Lark(grammar)
parse_tree = p.parse(frase)

data = MyInterpreter().visit(parse_tree)
#print("Número de número ",data[0]," Somatório: ",data[1])