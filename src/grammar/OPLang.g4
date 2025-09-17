grammar OPLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text[1:]);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text[1:]);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

program: EOF; // write for program rule here using vardecl and funcdecl


////////////////////////////////////////////////////////////////////////////////
//////////////////////////////    LEXER RULES     //////////////////////////////
////////////////////////////////////////////////////////////////////////////////

// Skipping comments
LINE_COMMENT : '#' ~[\r\n\f]* -> skip ;
BLOCK_COMMENT: '/*' .*? '*/' -> skip ;

// Keywords
BOOLEAN: 'boolean' ;
BREAK: 'break' ;
CLASS: 'class' ;
CONTINUE: 'continue' ;
DO: 'do' ;
ELSE: 'else' ;
EXTENDS: 'extends' ;
FLOAT: 'float' ;
IF: 'if' ;
INT: 'int' ;
NEW: 'new' ;
STRING: 'string' ;
THEN: 'then' ;
FOR: 'for' ;
RETURN: 'return' ;
fragment TRUE: 'true' ;
fragment FALSE: 'false' ;
VOID: 'void' ;
NIL: 'nil' ;
THIS: 'this' ;
FINAL: 'final' ;
STATIC: 'static' ;
TO: 'to' ;
DOWNTO: 'downto' ;

// Operators
ADD: '+' ;
SUB: '-' ;
MUL: '*' ;
FLTDIV: '/' ;
INTDIV: '\\' ;
MOD: '%' ;
NEQ: '!=' ;
EQ: '==' ;
LT: '<' ;
GT: '>' ;
LEQ: '<=' ;
GEQ: '>=' ;
OR: '||' ;
AND: '&&' ;
NOT: '!' ;
CONCAT: '^' ;
ASSIGN: ':=' ;

// Separators
LSB: '[' ;
RSB: ']' ;
LB: '{' ;
RB: '}' ;
LP: '(' ;
RP: ')' ;
SEMI: ';' ;
COLON: ':' ;
DOT: '.' ;
COMMA: ',' ;

// Specials
TILDE: '~' ;        // for destructor declaration
AMPERSAND: '&' ;    // for reference declaration

// Integer literals
INTLIT: [0-9]+ ;

// Float literals
FLOATLIT: INTPART DECPART? EXPPART | INTPART DECPART ;
fragment INTPART: [0-9]+ ;
fragment DECPART: '.' [0-9]* ;
fragment EXPPART: [eE] [+-]? [0-9]+ ;

// Boolean literals
BOOLLIT: TRUE | FALSE ;

// String literals
STRINGLIT: '"' (ESC | ~["\\\r\n\f])* '"' ;
fragment ESC: '\\' [bfrnt"\\];

// Identifiers
ID: [A-Za-z_] [A-Za-z_0-9]* ;

WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs, newlines, formfeeds

// Lexical errors
ILLEGAL_ESCAPE: '"' (ESC | ~["\\\r\n\f])* '\\' ~[bfrnt"\\] ;
UNCLOSE_STRING: '"' (ESC | ~["\\\r\n\f])* ;
ERROR_CHAR: . ;