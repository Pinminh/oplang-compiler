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