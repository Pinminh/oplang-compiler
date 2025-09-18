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

////////////////////////////////////////////////////////////////////////////////
/////////////////////////////    PARSER RULES     //////////////////////////////
////////////////////////////////////////////////////////////////////////////////

// Class list
program: ne_cls_decl_list EOF;
ne_cls_decl_list: cls_decl ne_cls_decl_list | cls_decl ;

// Class declaration
cls_decl: CLASS ID cls_extension LB mem_decl_list RB ;
cls_extension: EXTENDS ID |  ;

// Class member list
mem_decl_list: mem_decl mem_decl_list |  ;

// Class member declaration
mem_decl: attr_decl | method_decl | constructor_decl | destructor_decl ;

// Class attribute declaration
attr_decl: attr_modifier dtype ne_cm_asgn_id_list SEMI ;
attr_modifier: FINAL | STATIC | FINAL STATIC | STATIC FINAL |  ;
ne_cm_asgn_id_list: asgn_id COMMA ne_cm_asgn_id_list | asgn_id ;
asgn_id: ID asgn_expr ;
asgn_expr: ASSIGN expr |  ;

// Class method declaration
method_decl: method_modifier dtype ID LP sm_param_decl_list RP block_stmt ;
method_modifier: STATIC |  ;
sm_param_decl_list: ne_sm_param_decl_list |  ;
ne_sm_param_decl_list: param_decl SEMI sm_param_decl_list | param_decl ;
param_decl: dtype ne_cm_id_list ;
ne_cm_id_list: ID COMMA ne_cm_id_list | ID ;

// Class constructor declaration
constructor_decl: default_constructor_decl
                | copy_constructor_decl
                | user_constructor_decl ;

default_constructor_decl: ID LP RP block_stmt ;
copy_constructor_decl: ID LP ID ID RP block_stmt ;
user_constructor_decl: ID LP sm_param_decl_list RP block_stmt ;

// Class destructor declaration
destructor_decl: TILDE ID LP RP block_stmt ;

// Data types
dtype: ptype | atype | ctype | rtype | VOID ;
ptype: INT | FLOAT | BOOLEAN | STRING ;
atype: (ptype | ctype) LSB INTLIT RSB ;
ctype: ID ;
rtype: (ptype | atype | ctype) AMPERSAND ;

// Expressions
expr    : gtexpr (LT | GT | LTE | GTE) gtexpr | gtexpr ;
gtexpr  : eqexpr (EQ | NEQ) eqexpr | eqexpr ;
eqexpr  : eqexpr (AND | OR) lgexpr | lgexpr ;
lgexpr  : lgexpr (ADD | SUB) addexpr | addexpr ;
addexpr : addexpr (MUL | FLTDIV | INTDIV | MOD) mulexpr | mulexpr ;
mulexpr : mulexpr CONCAT conexpr | conexpr ;
conexpr : NOT conexpr | notexpr ;
notexpr : (ADD | SUB) notexpr | uniexpr ;
uniexpr : uniexpr LSB expr RSB | uniexpr DOT ID callargs | idxexpr ;
idxexpr : NEW idxexpr LP cm_expr_list RP | newexpr ;
newexpr : LP expr RP | parexpr ;
parexpr : lit | ID | THIS | NIL ;

callargs: LP cm_expr_list RP |  ;
cm_expr_list: ne_cm_expr_list |  ;
ne_cm_expr_list: expr COMMA cm_expr_list | expr ;

lit: plit | alit ;
plit: INTLIT | FLOATLIT | BOOLLIT | STRINGLIT ;
alit: LB ne_cm_plit_list RB ;
ne_cm_plit_list: plit COMMA ne_cm_plit_list | plit ;

// Statements
stmt: match_stmt | open_stmt ;

other_stmt: block_stmt | asgn_stmt | for_stmt
          | break_stmt | cont_stmt | ret_stmt | invk_stmt ;

// Block statement
block_stmt: LB vardecl_list stmt_list RB ;

vardecl_list: vardecl vardecl_list |  ;
vardecl: var_modifier dtype ne_cm_asgn_id_list SEMI ;
var_modifier: FINAL |  ;

stmt_list: stmt stmt_list |  ;

// Assignment statement
asgn_stmt: asgnlhs ASSIGN expr SEMI ;
asgnlhs: uniexpr ;

// If statement
match_stmt: IF expr THEN match_stmt ELSE match_stmt | other_stmt ;
open_stmt: IF expr THEN stmt | IF expr THEN match_stmt ELSE open_stmt ;

// For statement
for_stmt: FOR ID ASSIGN expr (TO | DOWNTO) expr DO stmt ;

// Break statement
break_stmt: BREAK SEMI ;

// Continue statement
cont_stmt: CONTINUE SEMI ;

// Return statement
ret_stmt: RETURN expr SEMI ;

// Invoke statement
invk_stmt: uniexpr SEMI ;

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
LTE: '<=' ;
GTE: '>=' ;
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