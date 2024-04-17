# ------------------------------------------------------------
# TPC1 : Intervalos (definição sintática)
#  + [100,200][3,12][20,45]
#  + [-4,-2][1,2][3,5][7,10][12,14][15,19]
#  - [19,15][12,6][-1,-3]
#  - [1000,200][30,12]
# ------------------------------------------------------------
import sys
import ply.yacc as yacc
from intervalos_lex import tokens

# The set of syntatic rules
def p_sequencia(p):
    "sequencia : sentido intervalos"
    if parser.success == True:
        p[0] = p[2]
        print("Número intervalos: "+ str(len(p[0])))
        print("Comprimento de cada intervalo:" + str([abs(x[1]-x[0]) for x in p[0]]))
        print("Smallest interval:", parser.menor)
        print("Biggest interval:", parser.maior)
        print("Amplitude da sequência:" + str(abs(parser.last - parser.first)))
    else:
        print("Intervals with wrong format")

def p_sentidoA(p):
    "sentido : '+'"
    parser.flag = True

def p_sentidoD(p):
    "sentido : '-'"
    parser.flag = False

def p_intervalos_intervalo(p):
    "intervalos : intervalo"
    p[0] = [p[1]]

def p_intervalos_intervalos(p):
    "intervalos : intervalos intervalo"
    p[0] = p[1]
    p[0].append(p[2])

def p_intervalo(p):
    "intervalo : '[' NUM ',' NUM ']'"
    start = p[2]
    end = p[4]

    if parser.flag:
        condition = start < end
    else:
        condition = start > end

    if parser.last is None or (parser.flag and parser.last < start) or (not parser.flag and parser.last > start):
        p[0] = (start, end)
        parser.last = end
        if parser.first is None:
            parser.first = start
        update_min_max(start, end, condition)
    else:
        parser.success = False if condition else True

def update_min_max(start, end, condition):
    if start < end and condition:
        # Update minimum interval
        if parser.menor is None or (end - start) < (parser.menor[1] - parser.menor[0]):
            parser.menor = (start, end)
        # Update maximum interval
        if parser.maior is None or (end - start) > (parser.maior[1] - parser.maior[0]):
            parser.maior = (start, end)
    elif start > end and condition:
        # Update minimum interval
        if parser.menor is None or (start - end) < (parser.menor[0] - parser.menor[1]):
            parser.menor = (start, end)
        # Update maximum interval
        if parser.maior is None or (start - end) > (parser.maior[0] - parser.maior[1]):
            parser.maior = (start, end)
    else:
        parser.success = False

# Syntatic Error handling rule
def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

# Start parsing the input text
for line in sys.stdin:
    parser.success = True
    parser.flag = True
    parser.first = None
    parser.last = None
    parser.menor = None
    parser.maior = None
    parser.parse(line)