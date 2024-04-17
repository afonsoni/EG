from lark import Lark
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def start(self, tree):
        for statement in tree.children:
            self.visit(statement)

    def classe(self, tree):
        class_name = tree.children[0].value
        self.functions[class_name] = {}
        for statement in tree.children[2:]:
            self.visit(statement)

    def funcao(self, tree):
        func_name = tree.children[0].value
        self.functions[func_name] = tree.children[3:]

    def decl(self, tree):
        var_name = tree.children[1].value
        if len(tree.children) > 2:
            var_type = tree.children[2]
            print(var_type)
            if len(tree.children) > 3:
                value = self.visit(tree.children[3])
                if isinstance(value, str) and value.isdigit():
                    value = int(value)
            else:
                value = None
        else:
            var_type = None
            value = None
        self.variables[var_name] = {'type': var_type, 'value': value}

    def atribuicao(self, tree):
        var_name = tree.children[0].value
        value = self.visit(tree.children[1])
        if var_name in self.variables:
            var_type = self.variables[var_name]['type']
            if var_type is not None and not isinstance(value, var_type):
                raise TypeError(f"Cannot assign value of type {type(value).__name__} to variable '{var_name}' of type {var_type}.")
        else:
            raise NameError(f"Name '{var_name}' is not defined.")
        self.variables[var_name]['value'] = value


grammar2 = '''
// Regras Sintaticas - Pitão
start: (classe | funcao | decls | insts)+

classe: "classe" ID ACHA (funcao | decls | insts)* FCHA

funcao: "fun" ID APAR parametros? FPAR ("=>" tipo)? ACHA (funcao | decls | insts)* FCHA
parametros: decl (VIR decl)*

decls: decl+
decl: var? ID ":" tipo ("=" expr)? | var? ID ()":" tipo)? "=" expr

var: "let" | "const"
tipo: "Int" | "Set" | "Array" | "Tuplo" | "Estringue" | "Lista"

insts: inst+
inst: atribuicao | chamar | ler | escreve | imprime | selecao | repeticao

atribuicao: ID "=" expr
chamar: ID APAR parametros? FPAR
ler: "ler" ID
escreve: "escreve" expr
imprime: "imprime" expr

selecao: se | caso

se: "se" expr "entao" insts ("senao" expr "entao" insts)* "defeito" insts "fim"
caso: "corresponde" expr "com" ("caso" expr "=>" insts ("break")?)+ "defeito" "=>" insts "fim" 

repeticao: enq_fazer | repetir_ate

enq_fazer: "enq" expr "fazer" insts
repetir_ate: "fazer" insts "ate" expr

expr: term (OP term)*
term: NUM | STRING | ID | APAR expr FPAR

// Regras Lexicográficas
NUM: /[0-9]+(,[0-9]+)?/
STRING: /"([^"]+)"/
ID: /[a-zA-Z_]\w*/
OP: "+" | "-" | "*" | "/" | "%" | "^" | "==" | "!=" | "<" | "<=" | ">" | ">=" | "e" | "ou"
VIR: ","
APAR: "("
FPAR: ")"
ACHA: "{"
FCHA: "}"

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase = """
classe Principal {
    let x: Int
    x = 5
    se x > 0 entao
        main()
    defeito
        escreve "nope"
    fim
    
    fun main() {
        escreve "Hello, World!"
    }
}
        """

frase2 = """
classe Exemplo {
    const VARIAVEL: Int

    fun soma(a: Int, b: Int) => Int {
        c = a + b
        return c
    }
    
    fun imprime_mensagem() {
        escreve "Olá, mundo!"
    }
}

fun main() {
    const numero: Int = 10
    const texto: Estringue = "Python"

    se numero > 0 entao
        escreve "O número é positivo."
    senao numero < 0 entao
        escreve "O número é negativo."
    defeito
        escreve "O número é zero."
    fim

    numero = "Teste"

    enq numero > 0 fazer
        imprime_mensagem()
        numero = numero - 1
    

    corresponde numero com
        caso 1 =>
            escreve "Número é 1."
        caso 2 =>
            escreve "Número é 2."
        defeito =>
            escreve "Número é diferente de 1 e 2."
    fim
}
    """

p = Lark(grammar2) # cria um objeto parser

tree = p.parse(frase2)  # retorna uma tree
print(tree)
print(tree.pretty())
pydot__tree_to_png(tree,'lark_test.png')
parse_tree = p.parse(frase2)
data = MyInterpreter().visit(parse_tree)