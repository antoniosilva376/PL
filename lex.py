import ply.lex as lex
import sys


literals = ['(',')','+','-','*','/','=','"',';',',','>','<']

tokens = ["Num","Id","Repeat","Int","Read","Write"]

t_Num = r'\d+'
t_Repeat = r'repeat-until'
t_Int = r'int'
t_Read = r'read'
t_Write = r'write'
t_Id  = r'\w+'

t_ignore = " \t\n"

def t_error(t):
    print("Caracter ilegal " + t.value(0))
    t.lexer.skip(1)

lexer = lex.lex()
"""
for line in sys.stdin:
    lexer.input(line)
    for tok in lexer:
        print(tok)"""
