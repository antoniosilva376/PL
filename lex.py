#coding:utf-8
import ply.lex as lex
import sys

literals = ['(',')','+','-','*','/','=',',','>','<','!','{','}','[',']',';','%']

tokens = ["Num","If","Else","Id","Repeat","Int","Read","ReadInt","Write","String","For","And","Or","Not"]

def t_And(t):
    r'and'
    return(t)
def t_Or(t):
    r'or'
    return(t)
def t_Not(t):
    r'not'
    return(t)
def t_For(t):
    r'for'
    return(t)
def t_If(t):
    r'if'
    return(t)
def t_Num(t): 
    r'\d+'
    return(t)
def t_Repeat(t): 
    r'repeat_until'
    return(t)
def t_ReadInt(t): 
    r'readInt'
    return(t)
def t_Read(t): 
    r'read'
    return(t)
def t_Int(t): 
    r'int'
    return(t)
def t_Write(t): 
    r'write'
    return(t)
def t_Else(t): 
    r'else'
    return(t)
def t_Id(t):
    r'\w+'
    return(t)
def t_String(t):
    r'"[^"]*"'
    return(t)

t_ignore = " \t\n"

def t_error(t):
    print("Caracter ilegal " + t.value(0))
    t.lexer.skip(1)

lexer = lex.lex()
