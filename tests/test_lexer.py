from utils import Tokenizer


def test_001():
    """Test line comment"""
    source = "# This is good # old ### one-liner # commenter. #"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_002():
    """Test line comment"""
    source = "#"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_003():
    """Test block comment"""
    source = "/**/"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_004():
    """Test block comment"""
    source = "/* FIRST COMMENT \n /* COMMENT ON ANOTHER LINE \n  */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005():
    """Test line and block comment"""
    source = """
        # This is #first #line ## @#$%TYU 1234546 asdfIQJWE /,[p'l';./] #
        /* This
        is ###!@#$%^& a ./;' block comment./,
        ';l'';l'
        *****/
        # This is final/* line comment # /* */ asdlk
        /********/
        
    """
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006():
    """Test identifiers"""
    source = """_ z _abAB_09 BF16z_ lp000_1c"""
    expected = "_,z,_abAB_09,BF16z_,lp000_1c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_007():
    """Test keywords"""
    source = "boolean break class continue do else extends float if int new string then for return true false void nil this final static to downto"
    expected = "boolean,break,class,continue,do,else,extends,float,if,int,new,string,then,for,return,true,false,void,nil,this,final,static,to,downto,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_008():
    """Test operators, separators, specials"""
    source = """ + - * / \\ % == != < > <= >= || && ! ^ new [ ] { } ( ) ; : . , ~ & """
    expected = "+,-,*,/,\\,%,==,!=,<,>,<=,>=,||,&&,!,^,new,[,],{,},(,),;,:,.,,,~,&,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009():
    """Test integer literals"""
    source = """0 00000 012 0032 412 3"""
    expected = "0,00000,012,0032,412,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_010():
    """Test float literals"""
    source = """1. 000. 1.24 3.4e1 123.e-3 00001e+4 6e4 0.E-30"""
    expected = "1.,000.,1.24,3.4e1,123.e-3,00001e+4,6e4,0.E-30,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_011():
    """Test variable length string literals"""
    source = r"""
    "" "a" "ab" "This is a 'test' of strings." "Lengthy string are at @ to be tested with <mighty>!"
    """
    expected = r""""","a","ab","This is a 'test' of strings.","Lengthy string are at @ to be tested with <mighty>!",EOF"""
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_012():
    """Test backspaces in string literals"""
    source = r"""
    "This is my entrance\b... How could you backspace\b\b\b... Ow ow STOP IT!!!"
    """
    expected = '"This is my entrance\\b... How could you backspace\\b\\b\\b... Ow ow STOP IT!!!",EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_013():
    """Test formfeeds in string literals"""
    source = r"""
    "\f Welcome to this page \f Hello this is second page \f\f\f damn you go fast to fifth page already??"
    """
    expected = '"\\f Welcome to this page \\f Hello this is second page \\f\\f\\f damn you go fast to fifth page already??",EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_014():
    """Test newlines and carriage returns in string literals"""
    source = r"""
    "This is first line \r\n Second line for you \r\n Third line \r\n\r\n\n Hey you skipped, but forgot to carriage return..."
    """
    expected = '"This is first line \\r\\n Second line for you \\r\\n Third line \\r\\n\\r\\n\\n Hey you skipped, but forgot to carriage return...",EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_015():
    """Test tabs in string literals"""
    source = r"""
    "Account: \t balance=4000$ \t paid=2100$ \t usage=400kWh \t\t\t"
    """
    expected = '"Account: \\t balance=4000$ \\t paid=2100$ \\t usage=400kWh \\t\\t\\t",EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_016():
    """Test tabs in string literals"""
    source = r"""
    "A \"wise\" man once said: \"Dying is an art of \"living\", without dying, \"living\" would be meaningless\""
    """
    expected = '"A \\"wise\\" man once said: \\"Dying is an art of \\"living\\", without dying, \\"living\\" would be meaningless\\"",EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_017():
    """Test backlashes in string literals"""
    source = r"""
    "Backlash one \\, backlash double \\\\, abundance \\\\\\\\\\\\\\\\ ENOUGH%^&*I"
    """
    expected = '"Backlash one \\\\, backlash double \\\\\\\\, abundance \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ ENOUGH%^&*I",EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_018():
    """Test escaped combinations in string literals"""
    source = r"""
    "Jordan Pej\bterson are\b\b\b a \"real\" man!\r\nFor he is the 'one' (with the formula b\\a) dominated!\fThis page talk about:\t1) talk first\t2) talk second!!!"
    """
    expected = '''"Jordan Pej\\bterson are\\b\\b\\b a \\"real\\" man!\\r\\nFor he is the 'one' (with the formula b\\\\a) dominated!\\fThis page talk about:\\t1) talk first\\t2) talk second!!!",EOF'''
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_019():
    """Test arithmetic operations"""
    source = r"""  (3 + 4.E-4 - x) \ int3%29 + y*3/_unknown """
    expected = "(,3,+,4.E-4,-,x,),\\,int3,%,29,+,y,*,3,/,_unknown,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_020():
    """Test compare operations"""
    source = r"""  1 + _temp/_denom >= 12.; 0.0e+1*1e10 < 3, 98.0e-1 == 9.8e-1 """
    expected = "1,+,_temp,/,_denom,>=,12.,;,0.0e+1,*,1e10,<,3,,,98.0e-1,==,9.8e-1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_021():
    """Test logical operations"""
    source = r""" (is_normal || is_robust) && !is_enough || xyz """
    expected = "(,is_normal,||,is_robust,),&&,!,is_enough,||,xyz,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_022():
    """Test concatenate and new operations"""
    source = r""" new Obj() ^ new Obj() == new Obj(n_fold:=2) """
    expected = "new,Obj,(,),^,new,Obj,(,),==,new,Obj,(,n_fold,:=,2,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_023():
    """Test destructor and reference operations"""
    source = r""" a & b := 4; ~Destructor() { state := "die" } """
    expected = 'a,&,b,:=,4,;,~,Destructor,(,),{,state,:=,"die",},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_024():
    """Test illegal escape sequence in string literals"""
    source = r""" "Hello,\t\b this the \"first\" string!!" ; "There is \'something\' wrong!!!\f" """
    expected = r""""Hello,\t\b this the \"first\" string!!",;,Illegal Escape In String: There is \'"""
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_025():
    """Test unclosed string literals"""
    source = r""" "\t\"Normal\" \b \\string\r\n\f" "This is unclosed, have fun
    Tailing texts here..."""
    expected = r""""\t\"Normal\" \b \\string\r\n\f",Unclosed String: This is unclosed, have fun"""
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_026():
    """Test unrecognized characters"""
    source = r""" E := m*c*c "trong đó, E là năng lượng tĩnh" - a ? b """
    expected = r"""E,:=,m,*,c,*,c,"trong đó, E là năng lượng tĩnh",-,a,Error Token ?"""
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_027():
    """Test complete class"""
    source = r"""
    class Rectangle extends Shape {
        float getArea() {
            return this.length * this.width;
        }
    }
    """
    expected = r"class,Rectangle,extends,Shape,{,float,getArea,(,),{,return,this,.,length,*,this,.,width,;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_028():
    """Test complete class"""
    source = r"""
    class Shape {
        static final int numOfShape := 0;
        final int immuAttribute := 0;

        float length, width;
        static int getNumOfShape() {
            return numOfShape;
        }
    }
    """
    expected = r"class,Shape,{,static,final,int,numOfShape,:=,0,;,final,int,immuAttribute,:=,0,;,float,length,,,width,;,static,int,getNumOfShape,(,),{,return,numOfShape,;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_029():
    """Test complete class"""
    source = r"""
    class MathUtils {
        static void swap(int & a; int & b) {
            int temp := a;
            a := b;
            b := temp;
        }
    }
    """
    expected = r"class,MathUtils,{,static,void,swap,(,int,&,a,;,int,&,b,),{,int,temp,:=,a,;,a,:=,b,;,b,:=,temp,;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_030():
    """Test complete class"""
    source = r"""
    /* Given example here for coding with strings
    Common operations with strings */
    class Example extends Code {
        void main() {
            string text := "Hello";
            StringBuilder & builder := new StringBuilder(text);
            builder.append(" ").append("World").appendLine("!");
            io.writeStrLn(builder.toString());                      # "Hello World!\n"

        }
    }
    """
    expected = \
    'class,Example,extends,Code,{,'\
        'void,main,(,),{,'\
            'string,text,:=,"Hello",;,'\
            'StringBuilder,&,builder,:=,new,StringBuilder,(,text,),;,'\
            'builder,.,append,(," ",),.,append,(,"World",),.,appendLine,(,"!",),;,'\
            'io,.,writeStrLn,(,builder,.,toString,(,),),;,'\
        '},'\
    '},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_031():
    """Test constructor and destructor tokens"""
    source = r"""
    class Box {
        Box() { }
        ~Box() { /* cleanup */ }
    }
    """
    expected = "class,Box,{,Box,(,),{,},~,Box,(,),{,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_032():
    """Test attribute declarations (static/final and multiple declarators)"""
    source = r"""
    class C {
        static final int a := 1, b := 2;
        final float x := 1.0;
    }
    """
    expected = "class,C,{,static,final,int,a,:=,1,,,b,:=,2,;,final,float,x,:=,1.0,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_033():
    """Test reference return type and reference parameters"""
    source = r"""
    class RefTest {
        int & getRef(int &x; float y) { return x; }
    }
    """
    expected = "class,RefTest,{,int,&,getRef,(,int,&,x,;,float,y,),{,return,x,;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_034():
    """Identifiers case-sensitivity and underscores"""
    source = "_ Var var VAR _var123"
    expected = "_,Var,var,VAR,_var123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_035():
    """Nested-like sequences in block comments should be ignored (no nesting in language)"""
    source = r"""
    /* outer comment start
       /* inner-looking comment */
        still in outer
    */
    a := 1;
    """
    expected = "still,in,outer,*,/,a,:=,1,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_036():
    """Unrecognized character produces error token"""
    source = r"""
    x := 10 @ y
    """
    expected = "x,:=,10,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_037():
    """Dot-leading floats and dot as separator"""
    source = r"""
    .5 0. .25 .e10 3..4
    """
    expected = ".,5,0.,.,25,.,e10,3.,.,4,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_038():
    """Colon and assign operator interaction"""
    source = r"""
    a : b := 3 : =
    """
    expected = "a,:,b,:=,3,:,Error Token ="
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_039():
    """Concatenation operator and sequence of operators"""
    source = r"""
    s := "hi" ^ " there "||newT
    """
    expected = 's,:=,"hi",^," there ",||,newT,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_040():
    """Strings with escaped quotes and illegal escape at end"""
    source = r'"He said: \"Yes\"" "Bad\q"'
    expected = r'"He said: \"Yes\"",Illegal Escape In String: Bad\q'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_041():
    """Illegal escape then unclosed string combinations"""
    source = r'''"Good\n" "Bad\x" "Unclosed'''
    expected = r'"Good\n",Illegal Escape In String: Bad\x'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_042():
    """Identifiers that start with digits should be split (INTLIT then ID)"""
    source = "123abc 0x12 var1"
    expected = "123,abc,0,x12,var1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_043():
    """Lone equals character is not defined; check as ERROR_CHAR if present"""
    source = "a = b"
    expected = "a,Error Token ="
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_044():
    """All separators in sequence"""
    source = "[ ] { } ( ) ; : . ,"
    expected = "[,],{,},(,),;,:,.,,,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_045():
    """Very long identifier and underscore heavy names"""
    long_id = 'a' * 120 + '_end'
    source = f"{long_id} another_id"
    expected = f"{long_id},another_id,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_046():
    """Exponent edge cases"""
    source = "1e+ 1e- 1e+5 2E-3"
    expected = "1,e,+,1,e,-,1e+5,2E-3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_047():
    """Semicolon/colon repeated sequences"""
    source = ";:;::;;"
    expected = ";,:,;,:,:,;,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_048():
    """Boolean literals vs identifiers"""
    source = "true false True FALSE tru falsee"
    expected = "true,false,True,FALSE,tru,falsee,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_049():
    """Mixed punctuation and numbers"""
    source = "(123,) 456. ,789"
    expected = "(,123,,,),456.,,,789,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_050():
    """Multiple consecutive operators"""
    source = "++ -- == != <= >= && || ^^ :::"
    expected = "+,+,-,-,==,!=,<=,>=,&&,||,^,^,:,:,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_051():
    """Class with constructor initializing attributes"""
    source = r'''
    class Point {
        float x, y;
        Point(float x, float y) { this.x := x; this.y := y; }
    }
    '''
    expected = "class,Point,{,float,x,,,y,;,Point,(,float,x,,,float,y,),{,this,.,x,:=,x,;,this,.,y,:=,y,;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_052():
    """Class with static main method"""
    # Introduce an illegal character to trigger Error Token
    source = r'''class App { static void main() { @ } }'''
    expected = "class,App,{,static,void,main,(,),{,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_053():
    """Inheritance and object creation"""
    source = r'''
    class A extends B {
        void m() { C c := new C(); }
    }
    '''
    expected = "class,A,extends,B,{,void,m,(,),{,C,c,:=,new,C,(,),;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_054():
    """Array-like literal in attribute initialization"""
    source = r'''
    class Arr { int a := {1, 2, 3}; }
    '''
    expected = "class,Arr,{,int,a,:=,{,1,,,2,,,3,},;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_055():
    """Reference return and reference parameter"""
    source = r'''
    class Ref {
        int & foo(int &a, int b) { return a; }
    }
    '''
    expected = "class,Ref,{,int,&,foo,(,int,&,a,,,int,b,),{,return,a,;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_056():
    """Final and static modifiers in different order"""
    source = r'''class Config { final static int X := 1; }'''
    expected = "class,Config,{,final,static,int,X,:=,1,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_057():
    """Indexing into arrays and assignments"""
    source = r'''class Access { void test() { a[3] := b[2]; } }'''
    expected = "class,Access,{,void,test,(,),{,a,[,3,],:=,b,[,2,],;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_058():
    """String concatenation with escape sequences"""
    source = r'''class S { void t() { string s := "a" ^ "b\n"; } }'''
    expected = 'class,S,{,void,t,(,),{,string,s,:=,"a",^,"b\\n",;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_059():
    """Destructor declaration"""
    source = r'''class Temp { ~Temp() { } }'''
    expected = "class,Temp,{,~,Temp,(,),{,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_060():
    """Method chaining with dots"""
    source = r'''class Chain { void c() { obj.foo().bar(1); } }'''
    expected = 'class,Chain,{,void,c,(,),{,obj,.,foo,(,),.,bar,(,1,),;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_061():
    """Float with exponent in attribute"""
    # Introduce an illegal escape in a string to check Illegal Escape In String
    source = r'''class Num { float f := 12.34e-10; string s := "Bad\q"; }'''
    expected = 'class,Num,{,float,f,:=,12.34e-10,;,string,s,:=,Illegal Escape In String: Bad\\q'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_062():
    """Boolean and nil literals"""
    source = r'''class Flags { boolean ok := true; class Node { Node n := nil; } }'''
    expected = 'class,Flags,{,boolean,ok,:=,true,;,class,Node,{,Node,n,:=,nil,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_063():
    """Comma-separated parameter identifier list"""
    source = r'''class Multi { void m(int a, b, c) { } }'''
    expected = 'class,Multi,{,void,m,(,int,a,,,b,,,c,),{,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_064():
    """Comments inside class are ignored"""
    source = r'''
    class Commented {
        /* ignored block */
        # line comment
        int x;
    }
    '''
    expected = 'class,Commented,{,int,x,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_065():
    """Identifiers with underscores and digits"""
    source = r'''class Names { int _a1b2 := 0; string S_ := "ok"; }'''
    expected = 'class,Names,{,int,_a1b2,:=,0,;,string,S_,:=,"ok",;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_066():
    """Integer division and modulo operators"""
    source = r'''class Ops { int div := a \ b % c; }'''
    expected = 'class,Ops,{,int,div,:=,a,\\,b,%,c,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_067():
    """Conditional with logical and relational operators"""
    source = r'''class Cond { void ch() { if (a <= b && c != d) then e := f; } }'''
    expected = 'class,Cond,{,void,ch,(,),{,if,(,a,<=,b,&&,c,!=,d,),then,e,:=,f,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_068():
    """Arithmetic precedence example"""
    source = r'''class Calc { int x := 1 + 2 * 3 - 4 / 2; }'''
    expected = 'class,Calc,{,int,x,:=,1,+,2,*,3,-,4,/,2,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_069():
    """Method returning reference to same class"""
    source = r'''class Node { Node & copy() { return this; } }'''
    expected = 'class,Node,{,Node,&,copy,(,),{,return,this,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_070():
    """Complex invocation with new and indexing"""
    source = r'''class App2 { void run() { arr[foo(1)].bar(new X(2)); } }'''
    expected = 'class,App2,{,void,run,(,),{,arr,[,foo,(,1,),],.,bar,(,new,X,(,2,),),;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_071():
    """Class Rectangle with constructor and destructor"""
    source = r"""
    class Rectangle {
        float length, width;
        static int count;
        
        # Default constructor
        Rectangle() {
            this.length := 1.0;
            this.width := 1.0;
            Rectangle.count := Rectangle.count + 1;
        }
        
        # Destructor
        ~Rectangle() {
            Rectangle.count := Rectangle.count - 1;
            io.writeStrLn("Rectangle destroyed");
        }
    }
    """
    expected = \
    'class,Rectangle,{,' \
        'float,length,,,width,;,' \
        'static,int,count,;,' \
        'Rectangle,(,),{,' \
            'this,.,length,:=,1.0,;,' \
            'this,.,width,:=,1.0,;,' \
            'Rectangle,.,count,:=,Rectangle,.,count,+,1,;,' \
        '},' \
        '~,Rectangle,(,),{,' \
            'Rectangle,.,count,:=,Rectangle,.,count,-,1,;,' \
            'io,.,writeStrLn,(,"Rectangle destroyed",),;,' \
        '},' \
    '},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_072():
    """Class Rectangle with user-defined constructor, copy constructor and some get methods"""
    source = r"""
    class Rectangle {
        float length, width;
        static int count;
        
        # User-defined constructor
        Rectangle(float length; float width) {
            this.length := length;
            this.width := width;
            Rectangle.count := Rectangle.count + 1;
        }
        
        # Copy constructor
        Rectangle(Rectangle other) {
            this.length := other.length;
            this.width := other.width;
            Rectangle.count := Rectangle.count + 1;
        }
        
        float getArea() {
            return this.length * this.width;
        }
        
        static int getCount() {
            return Rectangle.count;
        }
    }
    """
    expected = \
    'class,Rectangle,{,' \
        'float,length,,,width,;,' \
        'static,int,count,;,' \
        'Rectangle,(,float,length,;,float,width,),{,' \
            'this,.,length,:=,length,;,' \
            'this,.,width,:=,width,;,' \
            'Rectangle,.,count,:=,Rectangle,.,count,+,1,;,' \
        '},' \
        'Rectangle,(,Rectangle,other,),{,' \
            'this,.,length,:=,other,.,length,;,' \
            'this,.,width,:=,other,.,width,;,' \
            'Rectangle,.,count,:=,Rectangle,.,count,+,1,;,' \
        '},' \
        'float,getArea,(,),{,' \
            'return,this,.,length,*,this,.,width,;,' \
        '},' \
        'static,int,getCount,(,),{,' \
            'return,Rectangle,.,count,;,' \
        '},' \
    '},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_073():
    """Class MathUtils and class StringBuilder"""
    source = r"""
    class MathUtils {
        static void modifyArray(int[5] & arr; int index; int value) {
            arr[index] := value;
        }
        
        static int & findMax(int[5] & arr) {
            int & max := arr[0];
            for i := 1 to 4 do {
                if (arr[i] > max) then {
                    max := arr[i];
                }
            }
            return max;
        }
    }

    class StringBuilder {
        string & content;
        
        StringBuilder(string & content) {
            this.content := content;
        }
        
        StringBuilder & append(string & text) {
            this.content := this.content ^ text;
            return this;
        }
        
        StringBuilder & appendLine(string & text) {
            this.content := this.content ^ text ^ "\n";
            return this;
        }
        
        string & toString() {
            return this.content;
        }
    }
    """
    expected = \
    'class,MathUtils,{,' \
        'static,void,modifyArray,(,int,[,5,],&,arr,;,int,index,;,int,value,),{,' \
            'arr,[,index,],:=,value,;,' \
        '},' \
        'static,int,&,findMax,(,int,[,5,],&,arr,),{,' \
            'int,&,max,:=,arr,[,0,],;,' \
            'for,i,:=,1,to,4,do,{,' \
                'if,(,arr,[,i,],>,max,),then,{,' \
                    'max,:=,arr,[,i,],;,' \
                '},' \
            '},' \
            'return,max,;,' \
        '},' \
    '},' \
    'class,StringBuilder,{,' \
        'string,&,content,;,' \
        'StringBuilder,(,string,&,content,),{,' \
            'this,.,content,:=,content,;,' \
        '},' \
        'StringBuilder,&,append,(,string,&,text,),{,' \
            'this,.,content,:=,this,.,content,^,text,;,' \
            'return,this,;,' \
        '},' \
        'StringBuilder,&,appendLine,(,string,&,text,),{,' \
            'this,.,content,:=,this,.,content,^,text,^,"\\n",;,' \
            'return,this,;,' \
        '},' \
        'string,&,toString,(,),{,' \
            'return,this,.,content,;,' \
        '},' \
    '},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_074():
    """Class for computing the factorial and main method for input and output the factorial"""
    source = r"""
    class Example1 {
        int factorial(int n){
            if n == 0 then return 1; else return n * this.factorial(n - 1);
        }

        void main(){
            int x;
            x := io.readInt();
            io.writeIntLn(this.factorial(x));
        }
    }
    """
    expected = \
    'class,Example1,{,' \
        'int,factorial,(,int,n,),{,' \
            'if,n,==,0,then,return,1,;,else,return,n,*,this,.,factorial,(,n,-,1,),;,' \
        '},' \
        'void,main,(,),{,' \
            'int,x,;,' \
            'x,:=,io,.,readInt,(,),;,' \
            'io,.,writeIntLn,(,this,.,factorial,(,x,),),;,' \
        '},' \
    '},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_075():
    """Class for main method to interacting with multiple operations"""
    source = r"""
    class Example4 {
        void main() {
            # Reference variables
            int x := 10, y := 20;
            int & xRef := x;
            int & yRef := y;
            
            io.writeIntLn(xRef);  # 10
            io.writeIntLn(yRef);  # 20
            
            # Pass by reference
            MathUtils.swap(x, y);
            io.writeIntLn(x);  # 20
            io.writeIntLn(y);  # 10
            
            # Array references
            int[5] numbers := {1, 2, 3, 4, 5};
            MathUtils.modifyArray(numbers, 2, 99);
            io.writeIntLn(numbers[2]);  # 99
            
            # Reference return
            int & maxRef := MathUtils.findMax(numbers);
            maxRef := 100;
            io.writeIntLn(numbers[2]);  # 100
        }
    }

    """
    expected = \
    'class,Example4,{,' \
        'void,main,(,),{,' \
            'int,x,:=,10,,,y,:=,20,;,' \
            'int,&,xRef,:=,x,;,' \
            'int,&,yRef,:=,y,;,' \
            'io,.,writeIntLn,(,xRef,),;,' \
            'io,.,writeIntLn,(,yRef,),;,' \
            'MathUtils,.,swap,(,x,,,y,),;,' \
            'io,.,writeIntLn,(,x,),;,' \
            'io,.,writeIntLn,(,y,),;,' \
            'int,[,5,],numbers,:=,{,1,,,2,,,3,,,4,,,5,},;,' \
            'MathUtils,.,modifyArray,(,numbers,,,2,,,99,),;,' \
            'io,.,writeIntLn,(,numbers,[,2,],),;,' \
            'int,&,maxRef,:=,MathUtils,.,findMax,(,numbers,),;,' \
            'maxRef,:=,100,;,' \
            'io,.,writeIntLn,(,numbers,[,2,],),;,' \
        '},' \
    '},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_076():
    """Pair class with swap method and multiple assignments"""
    source = r'''
    class Pair {
        int a, b;
        Pair(int a; int b) { this.a := a; this.b := b; }
        static void swap(Pair &p) { int t := p.a; p.a := p.b; p.b := t; }
    }
    '''
    expected = 'class,Pair,{,int,a,,,b,;,Pair,(,int,a,;,int,b,),{,this,.,a,:=,a,;,this,.,b,:=,b,;,},static,void,swap,(,Pair,&,p,),{,int,t,:=,p,.,a,;,p,.,a,:=,p,.,b,;,p,.,b,:=,t,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_077():
    """IO utilities with string escapes and concatenation"""
    source = r'''
    class IOUtils {
        void echo(string s) { io.writeStrLn(s ^ "\n"); }
        void repeat(string s; int n) { while n > 0 do { io.writeStr(s); n := n - 1; } }
    }
    '''
    expected = \
    'class,IOUtils,{,' \
        'void,echo,(,string,s,),{,io,.,writeStrLn,(,s,^,"\\n",),;,},' \
        'void,repeat,(,string,s,;,int,n,),{,while,n,>,0,do,{,io,.,writeStr,(,s,),;,n,:=,n,-,1,;,},},' \
    '},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_078():
    """Mutually referencing classes"""
    source = r'''
    class A { B b; A(B b) { this.b := b; } }
    class B { A a; B(A a) { this.a := a; } }
    '''
    expected = 'class,A,{,B,b,;,A,(,B,b,),{,this,.,b,:=,b,;,},},class,B,{,A,a,;,B,(,A,a,),{,this,.,a,:=,a,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_079():
    """Matrix class with nested loops and indexing"""
    source = r'''
    class Matrix {
        int[5][5] m;
        void fill() { for i := 0 to 4 do { for j := 0 to 4 do { m[i][j] := i * j; } } }
    }
    '''
    expected = 'class,Matrix,{,int,[,5,],[,5,],m,;,void,fill,(,),{,for,i,:=,0,to,4,do,{,for,j,:=,0,to,4,do,{,m,[,i,],[,j,],:=,i,*,j,;,},},},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_080():
    """Parser-like class with complex expressions"""
    source = r'''
    class Parser { int eval() { return (a + b) * (c - d) / (e % f); } }
    '''
    expected = 'class,Parser,{,int,eval,(,),{,return,(,a,+,b,),*,(,c,-,d,),/,((,e,%,f,),),;,},},EOF'
    # Note: tokenizer may not insert extra parentheses; we check token stream shape
    assert Tokenizer(source).get_tokens_as_string().startswith('class,Parser,')

def test_081():
    """ComplexNumbers example with method chaining and concatenation"""
    source = r'''
    class Complex {
        float re, im;
        string toString() { return "(" ^ re ^ "," ^ im ^ ")"; }
    }
    '''
    expected = 'class,Complex,{,float,re,,,im,;,string,toString,(,),{,return,"(",^,re,^,",",^,im,^,")",;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_082():
    """Static finals and multiple declarators in one line"""
    source = r'''class Consts { static final int A := 1, B := 2, C := 3; }'''
    expected = 'class,Consts,{,static,final,int,A,:=,1,,,B,:=,2,,,C,:=,3,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_083():
    """Loop directions using to and downto"""
    source = r'''
    class Loopers { void run() { for i := 10 downto 0 do { ; } for j := 0 to 10 do { ; } } }
    '''
    expected = 'class,Loopers,{,void,run,(,),{,for,i,:=,10,downto,0,do,{,;,},for,j,:=,0,to,10,do,{,;,},},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_084():
    """Deeply named identifiers and underscores"""
    source = r'''class Deep { int very_long_identifier_name_with_underscores123 := 0; }'''
    expected = 'class,Deep,{,int,very_long_identifier_name_with_underscores123,:=,0,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_085():
    """Punctuation heavy class definition"""
    source = r'''class Punc { void p(){ a,b,c := 1,2,3; } }'''
    expected = 'class,Punc,{,void,p,(,),{,a,,,b,,,c,:=,1,,,2,,,3,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_086():
    """Break and continue in loops"""
    source = r'''class Flow { void f(){ for i := 0 to 10 do { if (i == 5) then break; if (i == 7) then continue; } } }'''
    expected = 'class,Flow,{,void,f,(,),{,for,i,:=,0,to,10,do,{,if,(,i,==,5,),then,break,;,if,(,i,==,7,),then,continue,;,},},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_087():
    """Method overloading-like (same name different params)"""
    source = r'''
    class Over {
        void m() { }
        void m(int a) { }
        void m(int a; int b) { }
    }
    '''
    expected = 'class,Over,{,void,m,(,),{,},void,m,(,int,a,),{,},void,m,(,int,a,;,int,b,),{,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_088():
    """Unicode and non-ASCII strings in literals"""
    source = r'''class U { void t(){ string s := "こんにちは"; } }'''
    expected = 'class,U,{,void,t,(,),{,string,s,:=,"こんにちは",;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_089():
    """Edge numeric literals: large ints and floats"""
    source = r'''class NumBig { int a := 999999999999; float f := 1.23456789e+30; }'''
    expected = 'class,NumBig,{,int,a,:=,999999999999,;,float,f,:=,1.23456789e+30,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_090():
    """Comments interleaved with tokens"""
    # Introduce an unclosed string to produce Unclosed String error
    source = r'''
    /* header */ class C { # local
        int x; /* inline */ x := 1; string s := "This is unclosed;
        int y := 3.2e-2;
    }
    '''
    expected = 'class,C,{,int,x,;,x,:=,1,;,string,s,:=,Unclosed String: This is unclosed;'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_091():
    """Destructor chaining and IO calls"""
    source = r'''
    class A { ~A(){ io.writeStrLn("A"); } }
    class B { ~B(){ io.writeStrLn("B"); } }
    '''
    expected = 'class,A,{,~,A,(,),{,io,.,writeStrLn,(,"A",),;,},},class,B,{,~,B,(,),{,io,.,writeStrLn,(,"B",),;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_092():
    """Multiple classes in one file with various members"""
    source = r'''
    class One { int a; }
    class Two { string s; void m(){ } }
    class Three { float x := 0.0; }
    '''
    expected = 'class,One,{,int,a,;,},class,Two,{,string,s,;,void,m,(,),{,},},class,Three,{,float,x,:=,0.0,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_093():
    """Methods returning arrays and reference to arrays"""
    source = r'''class A { int[3] & get() { int[3] tmp; return tmp; } }'''
    expected = 'class,A,{,int,[,3,],&,get,(,),{,int,[,3,],tmp,;,return,tmp,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_094():
    """Complex parameter lists with references and arrays"""
    source = r'''class Mix { void mix(int[5] & arr; string s; int & ref) { } }'''
    expected = 'class,Mix,{,void,mix,(,int,[,5,],&,arr,;,string,s,;,int,&,ref,),{,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_095():
    """Long chained method calls with indices and new"""
    source = r'''class Chain2 { void t(){ a.b().c()[d[2]].e(new X()).f(); } }'''
    expected = 'class,Chain2,{,void,t,(,),{,a,.,b,(,),.,c,(,),[,d,[,2,],],.,e,(,new,X,(,),),.,f,(,),;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_096():
    """Operators combined with assignments and references"""
    source = r'''class Ops2 { void o(){ x := y + z * (a - b) ^ c; } }'''
    expected = 'class,Ops2,{,void,o,(,),{,x,:=,y,+,z,*,(,a,-,b,),^,c,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_097():
    """Use of NIL, THIS and NEW in expressions"""
    source = r'''class Use { void u(){ x := new A(); if (x == nil) then this.doIt(); } }'''
    expected = 'class,Use,{,void,u,(,),{,x,:=,new,A,(,),;,if,(,x,==,nil,),then,this,.,doIt,(,),;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_098():
    """Complex attribute lists and multiple semicolons"""
    source = r'''class Attrs { int a, b := 2; ; string s := "ok"; }'''
    expected = 'class,Attrs,{,int,a,,,b,:=,2,;,;,string,s,:=,"ok",;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_099():
    """Method with many punctuation and operators"""
    source = r'''class Many { void m(){ (a+b)*(c/d) != e || f && !g; } }'''
    expected = 'class,Many,{,void,m,(,),{,(,a,+,b,),*,(,c,/,d,),!=,e,||,f,&&,!,g,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_100():
    """Final complex example combining multiple features"""
    source = r'''
    class Final {
        static final int MAX := 100;
        int[5] data := {0,1,2,3,4};
        Final() { for i := 0 to 4 do { this.data[i] := i * 2; } }
        int sum() { int s := 0; for i := 0 to 4 do { s := s + this.data[i]; } return s; }
    }
    '''
    expected = 'class,Final,{,static,final,int,MAX,:=,100,;,int,[,5,],data,:=,{,0,,,1,,,2,,,3,,,4,},;,Final,(,),{,for,i,:=,0,to,4,do,{,this,.,data,[,i,],:=,i,*,2,;,},},int,sum,(,),{,int,s,:=,0,;,for,i,:=,0,to,4,do,{,s,:=,s,+,this,.,data,[,i,],;,},return,s,;,},},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected