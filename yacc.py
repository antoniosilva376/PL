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
          | Funcao


Atribuicao : int id
           | int id '[' Num ']'
           | int id '[' Num ',' Num ']'
           | int id '=' Operacao
           | int id '=' ReadInt '(' ')'
           | id '=' Operacao
           | id '=' ReadInt '(' ')'
           | id '[' Operacao ']' '=' Operacao
           | id '[' Operacao ']' '=' ReadInt '(' ')'
           | id '[' Operacao ',' Operacao ']' '=' Operacao
           | id '[' Operacao ',' Operacao ']' '=' ReadInt '(' ')'
           
Operacao : Operacao '+' Termo
         | Operacao '-' Termo
         | Termo

Termo : Termo '*' Fator
      | Termo '/' Fator
      | Fator

Fator : Num
      | Id
      | Id '[' Operacao ']'
      | Id '[' Operacao ',' Operacao ']'
      | '(' Operacao ')'

Condicional : Operacao '>' Operacao
            | Operacao '<' Operacao
            | Operacao '>' '=' Operacao
            | Operacao '<' '=' Operacao
            | Operacao '=' '=' Operacao
            | Operacao '!' '=' Operacao

Funcao : Write '(' String ')'
       | Write '(' Operacao ')'
       | ReadInt '(' ')'
       | Read '(' ')'
       | Repeat '(' Condicional ')' '{' Instrucoes '}'
       | If '(' Condicional ')' '{' Instrucoes '}' Else '{' Instrucoes '}'
       | If '(' Condicional ')' '{' Instrucoes '}'
"""

# Tabela de Simbolos dict{variavel : pos_stack}

ts = dict({})

# Tabela de Arrays dict{variavel : (pos_stack,tamanho)}
ta = dict({})
#variavel que aponta para a posição atual da stack
pos_stack=0
#variavel para tornar as etiquetas unicas
func_nr = 0

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

def p_Instrucao_Funcao(p):
    "Instrucao : Funcao"
    p[0] = p[1]



def p_Funcao_Write_String(p):
    "Funcao : Write '(' String ')'"
    p[3] = p[3][:-1] + "\\n\"" 
    p[0] = "\npushs " + p[3] + "\nwrites"

def p_Funcao_Write_Operacao(p):
    "Funcao : Write '(' Operacao ')'"
    p[0] = p[3] + "\nstri" + "\nwrites"

def p_Funcao_ReadInt(p):
    "Funcao : ReadInt '(' ')'"
    global pos_stack
    p[0] = "\nread \natoi" 
    pos_stack+=1

def p_Funcao_Read(p):
    "Funcao : Read '(' ')'"
    global pos_stack
    p[0] = "\nread"
    pos_stack+=1

def p_Funcao_Repeat(p):
    "Funcao : Repeat '(' Condicional ')' '{' Instrucoes '}'"
    global func_nr
    p[0] = ("\nrepeat" + str(func_nr) +":" 
        + p[3]+"\nnot\njz end" + str(func_nr)
        + p[6]
        + "\njump repeat" + str(func_nr)
        + "\nend" + str(func_nr) +":"
        )
    func_nr+=1
    
def p_Funcao_IfElse(p):
    "Funcao : If '(' Condicional ')' '{' Instrucoes '}' Else '{' Instrucoes '}'"
    global func_nr
    p[0] = (p[3]+"\njz else" + str(func_nr)
        + p[6]
        +"\njump end" + str(func_nr)
        +"\nelse" + str(func_nr) + ":"
        + p[10] 
        + "\nend" + str(func_nr) +":"
        )
    func_nr+=1

def p_Funcao_If(p):
    "Funcao : If '(' Condicional ')' '{' Instrucoes '}'"
    global func_nr
    global pos_stack
    p[0] = (p[3]+"\njz end" + str(func_nr)
        + p[6] 
        + "\nend" + str(func_nr) +":"
        )
    func_nr+=1



def p_Atribuicao_Declaracao_Zero(p):
    "Atribuicao : Int Id"
    if(p[2] not in ts):
        global pos_stack
        ts[p[2]] = pos_stack
        p[0] = "\npushi 0"
        pos_stack+=1
    else:
        #erro
        pass

def p_Atribuicao_Declaracao_Input(p):
    "Atribuicao : Int Id '=' ReadInt '(' ')'"
    if(p[2] not in ts):
        global pos_stack
        ts[p[2]] = pos_stack
        p[0] = "\nread \natoi" 
        pos_stack+=1
    else:
        #erro
        pass

def p_Atribuicao_Declaracao(p):
    "Atribuicao : Int Id '=' Operacao"
    if(p[2] not in ts):
        global pos_stack
        ts[p[2]] = pos_stack-1
        p[0] =  str(p[4])
    else:
        #erro
        pass
    
def p_Atribuicao_Declaracao_Array(p):
    "Atribuicao : Int Id '[' Num ']'"
    if(p[2] not in ta):
        global pos_stack
        ta[p[2]] = (pos_stack,int(p[4]))
        p[0] = "\npushn " + str(p[4])
        pos_stack += int(p[4])
    else:
        #erro
        pass

def p_Atribuicao_Declaracao_Matriz(p):
    "Atribuicao : Int Id '[' Num ',' Num ']'"
    if(p[2] not in ta):
        global pos_stack
        ta[p[2]] = (pos_stack,int(p[4])*int(p[6]))
        p[0] = "\npushn " + str(int(p[4])*int(p[6]))
        pos_stack += int(p[4])*int(p[6])
    else:
        #erro
        pass

def p_Atribuicao_Alt(p):
    "Atribuicao : Id '=' Operacao"
    if(p[1] in ts):
        global pos_stack
        p[0] =  str(p[3]) + "\nstoreg " + str(ts[p[1]])
        pos_stack-=1
    else:
        #erro
        pass

def p_Atribuicao_Input(p):
    "Atribuicao : Id '=' ReadInt '(' ')'"
    if(p[1] in ts):
        global pos_stack
        p[0] =  "\nread \natoi \nstoreg " + str(ts[p[1]])
        pos_stack-=1
    else:
        #erro
        pass

def p_Atribuicao_Array(p):
    "Atribuicao : Id '[' Operacao ']' '=' Operacao"
    if(p[1] in ta):
        global pos_stack
        p[0] = "\npushgp" + "\npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + p[6] + "\nstoren"
        pos_stack-=1
    else:
        #erro
        pass

def p_Atribuicao_Array_Input(p):
    "Atribuicao : Id '[' Operacao ']' '=' ReadInt '(' ')'"
    if(p[1] in ta):
        global pos_stack
        p[0] =  "\npushgp" + "\npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + "\nread \natoi \nstoren"
        pos_stack-=1
    else:
        #erro
        pass

def p_Atribuicao_Matriz(p):
    "Atribuicao : Id '[' Operacao ',' Operacao ']' '=' Operacao"
    if(p[1] in ta):
        global pos_stack
        p[0] = "\npushgp" + "\npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + p[5] + "\mul" + p[8] + "\nstoren"
        pos_stack-=1
    else:
        #erro
        pass

def p_Atribuicao_Matriz_Input(p):
    "Atribuicao : Id '[' Operacao ',' Operacao ']' '=' ReadInt '(' ')'"
    if(p[1] in ta):
        global pos_stack
        p[0] =  "\npushgp" + "\npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + p[5] + "\nmul \nread \natoi \nstoren"
        pos_stack-=1
    else:
        #erro
        pass

def p_Operacao_Mais(p):
    "Operacao : Operacao '+' Termo"
    p[0] = str(p[1]) + str(p[3]) + "\nadd"
    global pos_stack
    pos_stack-=1

def p_Operacao_Menos(p):
    "Operacao : Operacao '-' Termo"
    p[0] = str(p[1]) + str(p[3]) + "\nsub"
    global pos_stack
    pos_stack-=1

def p_Operacao_Termo(p):
    "Operacao : Termo"
    p[0] = str(p[1])



def p_Termo_Mul(p):
    "Termo : Termo '*' Fator"
    p[0] = str(p[1]) + str(p[3]) + "\nmul"
    global pos_stack
    pos_stack-=1

def p_Termo_Div(p):
    "Termo : Termo '/' Fator"
    p[0] = str(p[1]) + str(p[3]) + "\ndiv"
    global pos_stack
    pos_stack-=1

def p_Termo_Fator(p):
    "Termo : Fator"
    p[0] = str(p[1])



def p_Fator_Num(p): 
    "Fator : Num"
    p[0] = "\npushi " + str(p[1])
    global pos_stack
    pos_stack+=1

def p_Fator_Id(p):
    "Fator : Id"
    p[0] = "\npushg " + str(ts[p[1]])
    global pos_stack
    pos_stack+=1

def p_Fator_Array(p): 
    "Fator : Id '[' Operacao ']'"
    p[0] = "\npushgp" + "\npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + "\nloadn"
    global pos_stack
    pos_stack-=1

def p_Fator_Matriz(p): 
    "Fator : Id '[' Operacao ',' Operacao ']'"
    p[0] = "\npushgp" + "\npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + p[5] + "\nmul\nloadn"
    global pos_stack
    pos_stack-=1

def p_Fator_Operacao(p):
    "Fator : '(' Operacao ')'"
    p[0] = p[2]



def p_Condicional_Maior(p):
    "Condicional : Operacao '>' Operacao"
    p[0] = str(p[1]) + str(p[3]) + "\nsup"
    global pos_stack
    pos_stack-=2

def p_Condicional_Menor(p):
    "Condicional : Operacao '<' Operacao"
    p[0] = str(p[1]) + str(p[3]) + "\ninf"
    global pos_stack
    pos_stack-=2

def p_Condicional_MaiorIgual(p):
    "Condicional : Operacao '>' '=' Operacao"
    p[0] = str(p[1]) + str(p[4]) + "\nsupeq"
    global pos_stack
    pos_stack-=2

def p_Condicional_MenorIgual(p):
    "Condicional : Operacao '<' '=' Operacao"
    p[0] = str(p[1]) + str(p[4]) + "\ninfeq"
    global pos_stack
    pos_stack-=2

def p_Condicional_Igual(p):
    "Condicional : Operacao '=' '=' Operacao"
    p[0] = str(p[1]) + str(p[4]) + "\nequal"
    global pos_stack
    pos_stack-=2

def p_Condicional_Diferente(p):
    "Condicional : Operacao '!' '=' Operacao"
    p[0] = str(p[1]) + str(p[4]) + "\nequal\nnot"
    global pos_stack
    pos_stack-=2



#ERROR rule for sintax errors
def p_error(p):
    print("Syntax error in input: ",p)

#build the parser
parser = yacc.yacc()

#reading input
for linha in sys.stdin:
    result = parser.parse(linha)
    print(result)