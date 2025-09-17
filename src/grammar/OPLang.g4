grammar OPLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
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
TRUE: 'true' ;
FALSE: 'false' ;
VOID: 'void' ;
NIL: 'nil' ;
THIS: 'this' ;
FINAL: 'final' ;
STATIC: 'static' ;
TO: 'to' ;
DOWNTO: 'downto' ;

// Identifiers
// ID: [A-Za-z_] [A-Za-z_0-9]* ;

WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs 

// Lexical errors
ERROR_CHAR: .;
ILLEGAL_ESCAPE:.;
UNCLOSE_STRING:.;