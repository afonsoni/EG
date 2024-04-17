import datetime
from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png

grammar1 = """
start: turmas

turmas: (turma PON)+

turma: "TURMA" ID alunos

alunos: aluno (PONVIR aluno)*

aluno: NOME PE notas PD

notas: NUM (VIR NUM)*

// Regras Lexicográficas
ID: /[A-Z]/
NOME: /[a-zA-Z]+/
NUM:/[-?0-9]+/
PE:"("
PD:")"
VIR:","
PON:"."
PONVIR:";"


// Tratamento dos espaços em branco
%import common.WS
%ignore WS

"""

frase = """TURMA A
afonso (12, 13, 15, 12, 13, 15, 14);
joana (9,7,3,6,9);
daniel (12,16).
TURMA B
ana (12, 13, 15, 12, 13, 15, 14);
joao (9,7,3,6,9,12);
xico (12,16)."""

p = Lark(grammar1) # cria um objeto parser

tree = p.parse(frase)  # retorna uma tree

print(tree.pretty())

class CalculosTurmas(Transformer):
    def __init__(self):
        self.contador_alunos = 0
        self.dict = {}
        self.turmasD = {}
        self.alunosD = {}

    def start(self,elementos):
        print(f"Número total de alunos: {self.contador_alunos}")
        print("\n")
        print(f"Alunos por notas: {self.dict}")
        print(self.turmasD)
        print(self.alunosD)
        return self
    
    def turmas(self,turmas):
        return turmas
    
    def turma(self,turma):
        self.turmasD[str(turma[0])] = turma[1]
        return turma
    
    def alunos(self,alunos):
        return alunos
    
    def aluno(self,aluno):
        self.alunosD[str(aluno[0])] = aluno[1]
        self.contador_alunos += 1
        for nota in aluno[1]:
            if nota not in self.dict:
                self.dict[nota] = set() # Inicializa um set para a nota se ela não existir
            self.dict[nota].add(aluno[0])
        media = sum(aluno[1])/len(aluno[1])
        print(f"Aluno {aluno[0]} tem média {media}")
        print("\n")
        return aluno
    
    def notas(self,notas):
        return notas

    def ID (self,id):
        return str(id)

    def NOME (self,nome):
        return str(nome)

    def NUM (self,num):
        return int(num)

    def PE(self,pe):
        return Discard

    def PD(self,pd):
        return Discard

    def VIR(self,vir):
        return Discard
    
    def PON(self,pon):
        return Discard

    def PONVIR(self,ponvir):
        return Discard

# Transforma a árvore usando a classe CalculosTurmas
data = CalculosTurmas().transform(tree)

# SQL Insert
with open('turmas.sql', 'w') as f:
    dataInsercao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for turma, alunos in data.turmasD.items():
        for aluno, notas in data.alunosD.items():
            for nota in notas:
                f.write(f"INSERT INTO turmas (turma, aluno, nota, dataInsercao) VALUES ('{turma}', '{aluno}', {nota}, '{dataInsercao}');\n")

# MD file
markdown = f"# Visualizador de turmas\n"
for turma, alunos in data.turmasD.items():
    markdown += f"## Turma {turma}\n"
    markdown += f"### Lista de alunos\n"
    for aluno, notas in data.alunosD.items(): # o erro está aqui
        markdown += f"Aluno: {aluno}\n"
        markdown += "\n"
    markdown += f"### Notas\n"
    markdown += "| Aluno | Media |\n"
    markdown += "| ----- | ----- |\n"
    for aluno, notas in data.alunosD.items(): # e aqui também
        markdown += f"| {aluno} | {round(sum(notas)/len(notas), 2)} |\n"
    markdown += "\n\n"

with open('turmas.md', 'w') as f:
    f.write(markdown)

print(f"saida :{data}")
