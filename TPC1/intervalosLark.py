from lark import Lark
from lark.tree import pydot__tree_to_png

grammar2 = '''
// Regras Sintaticas
start: sentido intervalos

intervalos: intervalo (intervalo)*

intervalo: PE NUMERO VIR NUMERO PD

sentido: MAIS
        | MENOS

// Regras Lexicográficas
MAIS:"+"
MENOS:"-"
NUMERO:"0".."9"+ // [0-9]+
PE:"["
PD:"]"
VIR:","

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase = "+[1,23][24,50][51,57]"

p = Lark(grammar2) # cria um objeto parser

tree = p.parse(frase)  # retorna uma tree
print(tree)
print(tree.pretty())
pydot__tree_to_png(tree,'lark_test.png')