from app.scanner import Scanner
from app.tokens import Token
from typing import Optional
from typing import Callable
from typing import List
from app.expression import Group


""" 
---------------------------------------------
Statements              |         Retrun
---------------------------------------------
{ True , False }        |        self.value 
---------------------------------------------
"""


def is_bool(token: Token) -> bool:
    return token.token_type_ == "TRUE" or token.token_type_ == "FALSE"


def is_nil(token: Token) -> bool:
    return token.token_type_ == "NIL"


def is_number(token: Token) -> bool:
    return token.token_type_ == "NUMBER"


def is_string(token: Token) -> bool:
    return token.token_type_ == "STRING"


def is_left_paren(token: Token) -> bool:
    return token.token_type_ == "LEFT_PAREN"


def is_right_paren(token: Token) -> bool:
    return token.token_type_ == "RIGHT_PAREN"


def eof(token: Token) -> bool:
    return token.token_type_ == "EOF"


class ScannedTokens:
    def __init__(self, token_contents: List[str]):
        self.tokens = Scanner(token_contents).scan_tokens()
        self.current_token = 0
        self._token_status = None

    def is_not_end(self, index: Optional[int] = None):
        if not index:
            index = self.current_token
        return len(self.tokens) > index

    def save_token_status(self):
        self._token_status = self.current_token

    def reset_token_status(self):
        if self._token_status:
            self.current_token = self._token_status
        self._token_status = None

    def get_current_token(self):
        return self.tokens[self.current_token]

    def token_lookahead(self):
        if self.is_not_end(self.current_token + 1):
            return self.tokens[self.current_token + 1]


class Parser(ScannedTokens):
    def __init__(self, file_contents: List[str]):
        super().__init__(file_contents)

    def parse_expression(self, token: Token) -> str:
        exp_obj = EvaluateExpression(self)
        if exp_obj.is_group():
            return str(exp_obj)

        if is_bool(token):
            return token.lexeme_

        if is_nil(token):
            return token.lexeme_

        if is_number(token):
            return str(token.literal_)

        if is_string(token):
            return str(token.literal_)

        if eof(token):
            return ""

        raise Exception(f"Error during parsing:{token}")

    def parse(self) -> List[str]:
        parsed_tokens: List[str] = []
        while self.get_current_token():
            expr = self.parse_expression(self.get_current_token())
            if expr:
                parsed_tokens.append(expr)
            self.current_token += 1
            if not self.is_not_end(self.current_token):
                break
        return parsed_tokens


def is_match(
    token_object: Parser,
    method_1: Callable[[Token], bool],
    method_2: Callable[[Token], bool],
) -> bool:
    """Match two linear methods  and return true if they are"""
    current_token = token_object.get_current_token()
    next_token = token_object.token_lookahead()
    return (
        True
        if current_token
        and next_token
        and method_1(current_token)
        and method_2(next_token)
        else False
    )


"""
The common methods during parsing expression  , we will be using Recurssive Descent parser to Parse Expressions

EvaluateExpression Method : group

P' :  P
   ;

P : LPR   [ Parenthinsised L and R ] => Output "(group Q)"
   | X
   ;

X : U' 
  | B
  | NumericalExpression  after Postfix
  | O
  ;

U' : UB     => Output "(! true)"

U : !  
  | - 
  ; 
  
C : O N N   [comparision] => Output "(O N N)"
  :

O : < 
  | >
  | <= i.e LESS_EQUAL
  | >= i.e GREATER_EQUAL


E' : S E S  [Equality] => Output "( === S S)"
   ;

L : LEFT_PAREN
  ;

R : RIGHT_PAREN
  ;

S : STRING
  ;

N : NUMBER ( Number and lookahead is Operator)
  ;

B : BOOLEAN 
  ;

E : === 
  ;


U = > UNIIARY  OPERATOR ( '-' ,'!' )

INPUT: !true
OUTPUT : (! true)

Arthmetic Operator( '+','-','/' ) => POSTFIX and EvaluateExpression Operator

Comparasion Operator ('>','<','<=','<=')

Equality Operator ("baz" === "baz" ) => ( === baz baz)

"""


class EvaluateExpression:
    def __init__(self, token_object: Parser) -> None:
        self.token_object: Parser = token_object
        self.tok = None
        self.string = ""

    """

        S' : LQR   [ Parenthinsised L and R ] => Output "(group Q)"
           ;

        Q : S'
          | eplision; 
          ;

        S': S
          | N
          | B
          | U'
          ;

    """

    def is_group(self) -> bool:
        if is_left_paren(self.token_object.get_current_token()):
            self.token_object.current_token += 1
            next_token = ""
            while not is_right_paren(self.token_object.get_current_token()):
                next_token = self.token_object.parse_expression(
                    self.token_object.get_current_token()
                )
                self.token_object.current_token += 1
            self.string += str(Group(next_token))
            return True
        return False

    def __str__(self):
        return str(self.string)
