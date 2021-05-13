import ply.yacc as yacc
from lex import tokens
from lex import literals
import sys

"""
LExp : Instrucoes

Instrucoes : Instrucoes Instrucao
           | Instrucao

Instrucao : Atribuicao
          | Operacao
          | Condicional
          | Funcao

Funcao : Write '(' Instrucao ')'
       | Read '(' Instrucao ')'
       | Repeat '(' Instrucao ')'

Atribuicao : int id '=' Operacao
           | id '=' Operacao

Operacao : Operacao '+' Termo
         | Operacao '-' Termo
         | Termo

Termo : Termo '*' Fator
      | Termo '/' Fator
      | Fator

Fator : Num
      | Id
      | '(' Operacao ')'

ts = {
    ('a',0,1)
    ...
}


"""


def p_LExp(p):
    "LExp : Instrucoes"
    p[0] = p[1]


def p_Instrucoes_Instrucao(p):
    "Instrucoes : Instrucoes Instrucao"
    p[0] = p[1] + p[2]

def p_Instrucoes_Vazio(p):
    "Instrucoes : Instrucao"
    p[0] = p[1]

def p_Instrucao_Atribuicao(p):
    "Instrucao : Atribuicao"
    p[0] = p[1]

def p_Instrucao_Operacao(p):
    "Instrucao : Operacao"
    p[0] = p[1]

"""def p_Instrucao_Condicional(p):
    "Instrucao : Condicional"
    p[0] = p[1]"""

"""def p_Instrucao_Funcao(p):
    "Instrucao : Funcao"
    p[0] = p[1]"""


def p_Atribuicao_Declaracao(p):
    "Atribuicao : Int Id '=' Operacao"
    p[0] = p[1] + " " + p[2] + " = " + str(p[4])


def p_Atribuicao_Alt(p):
    "Atribuicao : Id '=' Operacao"
    #verificar se TS[p[1]]
    #p[0] = "pushi" + p[3] + "\npushg" + TS[p[1]] 
    p[0] = p[1] + "=" + str(p[3])



def p_Operacao_Mais(p):
    "Operacao : Operacao '+' Termo"
    p[0] = p[1] + p[3]

def p_Operacao_Menos(p):
    "Operacao : Operacao '-' Termo"
    p[0] = p[1] - p[3]

def p_Operacao_Termo(p):
    "Operacao : Termo"
    p[0] = p[1]



def p_Termo_Mult(p):
    "Termo : Termo '*' Fator"
    p[0] = p[1] * p[3]

def p_Termo_Div(p):
    "Termo : Termo '/' Fator"
    p[0] = p[1] / p[3]

def p_Termo_Fator(p):
    "Termo : Fator"
    p[0] = p[1]
      


def p_Fator_Num(p): 
    "Fator : Num"
    p[0] = int(p[1])

def p_Fator_Id(p):
    "Fator : Id"
    p[0] = p[1]
    #P[0] = int(TS[p[1]])

def p_Fator_Operacao(p):
    "Fator : '(' Operacao ')'"
    p[0] = p[1]






#ERROR rule for sintax errors
def p_error(p):
    print("Syntax error in input: ",p)

#build the parser
parser = yacc.yacc()

#reading input
for linha in sys.stdin:
    result = parser.parse(linha)
    print(result)