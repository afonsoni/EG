#!/usr/bin/env python3

# Documentação que fica guardada na variável __doc__
'''
NAME
   word_freq - Calculates word frequency in a text

SYNOPSIS
   word_freq [options] input_files
   options: 
        -m 20 : Show 20 most common
        -n : Order alfabetically
Description'''


from jjcli import * 
from collections import Counter # Dicionario chave - nº ocorrencias (multi-set)
import re

__version__ = "0.0.1"

def tokeniza(texto):
    palavras = re.findall(r'\w+(?:\-\w+)?|[,;.:_?!—]+', texto)
    # (?: ...) agrupa mas não captura
    return palavras

def imprime(lista, opt):
    if opt == 'm':
        for palavra, n_ocorr in lista:
            print(f"{palavra}   {n_ocorr}")
    elif opt in ('n','o'):
        for palavra, n_ocorr in lista:
            print(f"{n_ocorr}   {palavra}")
def main():
    # "-m" recebe um argumento logo leva ":", ao contrário de "-n"
    cl=clfilter("nmo:", doc=__doc__)     ## option values in cl.opt dictionary

    for txt in cl.text():     ## process one file at the time
        lista_palavras = tokeniza(txt)
        ocorr = Counter(lista_palavras)

        if "-m" in cl.opt:
            imprime(ocorr.most_common(int(cl.opt.get("-m"))), 'm')
        elif "-n" in cl.opt:
            lista_palavras.sort()
            ocorr = Counter(lista_palavras)
            imprime(ocorr.items(), 'n')
        elif "-o" in cl.opt:
            lista_palavras = [word.lower() for word in lista_palavras]
            ocorr = Counter(lista_palavras)
            imprime(ocorr.items(), 'o')
        else:
            imprime(ocorr.items(), 'm')





