from app.scanner import Scanner
from app.tokens import  Token


""" 
---------------------------------------------
Statements              |         Retrun
---------------------------------------------
{ True , False }        |        self.value 
---------------------------------------------
""" 
def is_bool(token:Token): 
    return token._token_type=="TRUE" or token._token_type=="FALSE"

def is_nil(token:Token):
    return token._token_type== "NIL"

def is_number(token:Token):
    return token._token_type=="NUMBER"

def is_string(token:Token):
    return token._token_type=="STRING"




"""
Group Method : group

P' :  P
   ;

P : LSR 

L : LEFT_PAREN
  ;

R : RIGHT_PAREN
  ;

S : STRING
  ;

P is Group
"""
class Group:
    
    def __init__(self,token):
        self.token  = token

    def is_group(self):

        ...
        

class Parser:

    def __init__(self,file_contents):
        self.tokens =Scanner(file_contents).scan_tokens()
    
    def parse_expression(self,token):

        if Group().is_group():
            ...

        if is_bool(token):
            return token._lexeme

        if is_nil(token) :
            return token._lexeme
        
        if is_number(token):
            return token._literal
        
        if is_string(token):
            return token._literal

    def parse(self):
        parsed_tokens= []
        for token in self.tokens:
            expr = self.parse_expression(token)
            if expr:
                parsed_tokens.append(expr)
        return parsed_tokens
