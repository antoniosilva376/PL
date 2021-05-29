#coding:utf-8
import ply.yacc as yacc
from lex import tokens
from lex import literals
import sys
from os import write

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
           | id '+' '+'  
           | id '-' '-' 
           | id '+' '=' Operacao 
           | id '-' '=' Operacao  

Operacao : Operacao '+' Termo
         | Operacao '-' Termo
         | Termo

Termo : Termo '*' Fator
      | Termo '/' Fator
      | Termo '%' Fator
      | Fator

Fator : Num
      | Id
      | Id '[' Operacao ']'
      | Id '[' Operacao ',' Operacao ']'
      | '(' Operacao ')'


Condicional : Condicional OR Cond                                       
            | Cond

Cond : Cond AND Cond2
     | Cond2

Cond2 :  NOT Cond
      | ExpRel
      | '(' Condicional ')'

ExpRel : Operacao '>' Operacao 
       | Operacao '<' Operacao
       | Operacao '>' '=' Operacao     
       | Operacao '<' '=' Operacao      
       | Operacao '=' '=' Operacao  
       | Operacao '!' '=' Operacao  
       | Operacao   

Funcao : Write '(' String ')'
       | Write '(' Operacao ')'
       | ReadInt '(' ')'
       | Read '(' ')'
       | Repeat '(' Condicional ')' '{' Instrucoes '}'
       | If '(' Condicional ')' '{' Instrucoes '}' Else '{' Instrucoes '}'
       | If '(' Condicional ')' '{' Instrucoes '}'
       | For '(' Atribuicao ';' Condicional ';' Atribuicao ')' '{' Instrucoes '}' 
"""

# Tabela de Simbolos dict{variavel : pos_stack}
ts = dict({})
# Tabela de Arrays dict{variavel : (pos_stack,tamanho)}
ta = dict({})
# Tabela de Arrays2D dict{variavel : (pos_stack,tamanho_linha,tamnho_coluna)}
tm = dict({})
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


           
def p_Funcao_For(p):
    "Funcao : For '(' Atribuicao ';' Condicional ';' Atribuicao ')' '{' Instrucoes '}'"
    global func_nr
    p[0] = (str(p[3]) + "\nfor_" + str(func_nr) + ":\n" + str(p[5]) + "\njz fim_for_" 
            + str(func_nr) + str(p[10]) + str(p[7]) + "\njump for_" + str(func_nr) 
            + "\nfim_for_" + str(func_nr) + ":")
    func_nr += 1        

def p_Funcao_Write_String(p):
    "Funcao : Write '(' String ')'"
    p[3] = p[3][:-1] + "\\n\"" 
    p[0] = "\npushs " + p[3] + "\nwrites"

def p_Funcao_Write_Operacao(p):
    "Funcao : Write '(' Operacao ')'"
    p[0] = p[3] + "\nstri" + "\nwrites \npushs " + "\"\\n\"" + "\nwrites" 

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
        + p[3]+"\npushi 0\nequal \njz end" + str(func_nr)
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



def p_Atribuicao_Inc_Id(p):
    "Atribuicao : Id '+' '+'"
    if(p[1] in ts):
        p[0] = "\npushg " + str(ts[p[1]]) + "\npushi 1\nadd\nstoreg " + str(ts[p[1]])

def p_Atribuicao_Dec_Id(p):
    "Atribuicao : Id '-' '-'"
    if(p[1] in ts):
        p[0] = "\npushi 1\npushg " + str(ts[p[1]]) + "\nsub\nstoreg" + str(ts[p[1]])

def p_Atribuicao_Inc_Id_Op(p):
    "Atribuicao : Id '+' '=' Operacao"
    if(p[1] in ts):
        p[0] = "\npushg " + str(ts[p[1]]) + str(p[4]) + "\nadd\nstoreg " + str(ts[p[1]])

def p_Atribuicao_Dec_Id_Op(p):
    "Atribuicao : Id '-' '=' Operacao"
    if(p[1] in ts):
        p[0] = str(p[4]) + "\npushg " + str(ts[p[1]]) + "\nsub\nstoreg " + str(ts[p[1]])

def p_Atribuicao_Declaracao_Zero(p):
    "Atribuicao : Int Id"
    if(p[2] not in ts and p[2] not in ta and p[2] not in tm):
        global pos_stack
        ts[p[2]] = pos_stack
        p[0] = "\npushi 0"
        pos_stack+=1

def p_Atribuicao_Declaracao_Input(p):
    "Atribuicao : Int Id '=' ReadInt '(' ')'"
    if(p[2] not in ts and p[2] not in ta and p[2] not in tm):
        global pos_stack
        ts[p[2]] = pos_stack
        p[0] = "\nread \natoi" 
        pos_stack+=1

def p_Atribuicao_Declaracao(p):
    "Atribuicao : Int Id '=' Operacao"
    if(p[2] not in ts and p[2] not in ta and p[2] not in tm):
        global pos_stack
        ts[p[2]] = pos_stack-1
        p[0] =  str(p[4])
    
def p_Atribuicao_Declaracao_Array(p):
    "Atribuicao : Int Id '[' Num ']'"
    if(p[2] not in ts and p[2] not in ta and p[2] not in tm):
        global pos_stack
        ta[p[2]] = (pos_stack,int(p[4]))
        p[0] = "\npushn " + str(p[4])
        pos_stack += int(p[4])

def p_Atribuicao_Declaracao_Matriz(p):
    "Atribuicao : Int Id '[' Num ',' Num ']'"
    if(p[2] not in ts and p[2] not in ta and p[2] not in tm):
        global pos_stack
        tm[p[2]] = (pos_stack,int(p[4]),int(p[6]))
        p[0] = "\npushn " + str(int(p[4])*int(p[6]))
        pos_stack += int(p[4])*int(p[6])

def p_Atribuicao_Alt(p):
    "Atribuicao : Id '=' Operacao"
    if(p[1] in ts):
        global pos_stack
        p[0] =  str(p[3]) + "\nstoreg " + str(ts[p[1]])
        pos_stack-=1

def p_Atribuicao_Input(p):
    "Atribuicao : Id '=' ReadInt '(' ')'"
    if(p[1] in ts):
        global pos_stack
        p[0] =  "\nread \natoi \nstoreg " + str(ts[p[1]])
        pos_stack-=1

def p_Atribuicao_Array(p):
    "Atribuicao : Id '[' Operacao ']' '=' Operacao"
    if(p[1] in ta):
        global pos_stack
        p[0] = "\npushgp \npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + p[6] + "\nstoren"
        pos_stack-=1

def p_Atribuicao_Array_Input(p):
    "Atribuicao : Id '[' Operacao ']' '=' ReadInt '(' ')'"
    if(p[1] in ta):
        global pos_stack
        p[0] = "\npushgp \npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + "\nread \natoi \nstoren"
        pos_stack-=1

def p_Atribuicao_Matriz(p):
    "Atribuicao : Id '[' Operacao ',' Operacao ']' '=' Operacao"
    if(p[1] in tm):
        global pos_stack  
        p[0] = "\npushgp" + "\npushi " + str(tm[p[1]][0]) + "\npadd" + p[3] + "\npushi " + str(tm[p[1]][2]) + "\nmul" + p[5] + "\nadd" + p[8] + "\nstoren"
        pos_stack-=1

def p_Atribuicao_Matriz_Input(p):
    "Atribuicao : Id '[' Operacao ',' Operacao ']' '=' ReadInt '(' ')'"
    if(p[1] in tm):
        global pos_stack  
        p[0] = "\npushgp" + "\npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + "\npushi " + str(tm[p[1]][1]) + "\nmul" + p[5] + "\nadd \nread \natoi \nstoren"
        pos_stack-=1



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

def p_Termo_Mod(p):
    "Termo : Termo '%' Fator"
    p[0] = str(p[1]) + str(p[3]) + "\nmod"
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
    global pos_stack
    p[0] = "\npushgp" + "\npushi " + str(ta[p[1]][0]) + "\npadd" + p[3] + "\nloadn"
    pos_stack-=1

def p_Fator_Matriz(p): 
    "Fator : Id '[' Operacao ',' Operacao ']'"
    global pos_stack
    p[0] = "\npushgp" + "\npushi " + str(tm[p[1]][0]) + "\npadd" + p[3] + p[5] + "\nmul\nloadn"
    pos_stack-=1
    func_nr+=1

def p_Fator_Operacao(p):
    "Fator : '(' Operacao ')'"
    p[0] = p[2]



def p_ExpRel_Maior(p):
    "ExpRel : Operacao '>' Operacao"
    p[0] = str(p[1]) + str(p[3]) + "\nsup"
    global pos_stack
    pos_stack-=2

def p_ExpRel_Menor(p):
    "ExpRel : Operacao '<' Operacao"
    p[0] = str(p[1]) + str(p[3]) + "\ninf"
    global pos_stack
    pos_stack-=2

def p_ExpRel_MaiorIgual(p):
    "ExpRel : Operacao '>' '=' Operacao"
    p[0] = str(p[1]) + str(p[4]) + "\nsupeq"
    global pos_stack
    pos_stack-=2

def p_ExpRel_MenorIgual(p):
    "ExpRel : Operacao '<' '=' Operacao"
    p[0] = str(p[1]) + str(p[4]) + "\ninfeq"
    global pos_stack
    pos_stack-=2

def p_ExpRel_Igual(p):
    "ExpRel : Operacao '=' '=' Operacao"
    p[0] = str(p[1]) + str(p[4]) + "\nequal"
    global pos_stack
    pos_stack-=2

def p_ExpRel_Diferente(p):
    "ExpRel : Operacao '!' '=' Operacao"
    p[0] = str(p[1]) + str(p[4]) + "\nequal \npushi 0\nequal"
    global pos_stack
    pos_stack-=2

def p_ExpRel_Exp(p):
    "ExpRel : Operacao"
    p[0] = str(p[1])



def p_Condicional_Or_Cond(p):
    "Condicional : Condicional Or Cond"
    p[0] = p[1] + p[3] + "\nadd" + p[1] + p[3] + "\nmul\nsub"

def p_Condicional_Cond(p):
    "Condicional : Cond"
    p[0] = p[1]

def p_Cond_And_Cond2(p):
    "Cond : Cond And Cond2"
    p[0] = p[1] + p[3] + "\nmul"
   
def p_Cond_Cond2(p):
    "Cond : Cond2"
    p[0] = p[1]
   
def p_Cond2_Not(p):
    "Cond2 : Not Condicional"
    p[0] = p[2] + "\npushi 0 \nequal"
   
def p_Cond2_ExpRel(p):
    "Cond2 : ExpRel"
    p[0] = p[1]
  
def p_Cond2_Condicional(p):
    "Cond2 : '(' Condicional ')'"
    p[0] = p[2]


           
def p_error(p):
    print("Syntax error in input: ",p)

#build the parser
parser = yacc.yacc()

#reading input
linhas = ""
for line in sys.stdin:
    linhas += line
#writing to file the result
f = open("codigo.vm", "a")
result = parser.parse(linhas)
f.write(result)
f.close()
