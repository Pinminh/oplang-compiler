from utils import Parser


def test_001():
    """Test basic class with main method"""
    source = """class Program { static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_002():
    """Test method with parameters"""
    source = """class Math { int add(int a; int b) { return a + b; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_003():
    """Test class with attribute declaration"""
    source = """class Test { int x; static void main() { x := 42; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_004():
    """Test class with string attribute"""
    source = """class Test { string name; static void main() { name := "Alice"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_005():
    """Test final attribute declaration"""
    source = """class Constants { final float PI := 3.14159; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    """Test if-else statement"""
    source = """class Test { 
        static void main() { 
            if (x > 0) then { 
                io.writeStrLn("positive"); 
            } else { 
                io.writeStrLn("negative"); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_007():
    """Test for loop with to keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 1 to 10 do { 
                i := i + 1; 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_008():
    """Test for loop with downto keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 10 downto 1 do { 
                io.writeInt(i); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_009():
    """Test array declaration and access"""
    source = """class Test { 
        static void main() { 
            int[3] arr := {1, 2, 3};
            int first;
            first := arr[0];
            arr[1] := 42;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_010():
    """Test string concatenation and object creation"""
    source = """class Test { 
        static void main() { 
            string result;
            Test obj;
            result := "Hello" ^ " " ^ "World";
            obj := new Test();
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_011():
    """Test parser error: missing closing brace in class declaration"""
    source = """class Test { int x := 1; """  # Thiếu dấu }
    expected = "Error on line 1 col 25: <EOF>"
    assert Parser(source).parse() == expected


def test_012():
    """Constructors: default, copy and user-defined"""
    source = '''class C { C() {} C(C other) { this.x := other.x; } C(int a; float b) { this.x := a; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_013():
    """Destructor and attribute initialization"""
    source = '''class T { int x := 0; ~T() { this.x := 1; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_014():
    """Reference return type and reference parameters"""
    source = '''class Ref { int & swap(int & a; int & b) { int t := a; a := b; b := t; return a; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_015():
    """Array declarations and array literal initializers"""
    source = '''class A { void main() { int[3] arr := {1,2,3}; int v; v := arr[1]; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_016():
    """Static method and attribute access; inheritance"""
    source = '''class Shape { static int count := 0; } class Rect extends Shape { static void main() { Rect.count := Rect.count + 1; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_017():
    """Complex arithmetic: precedence and integer division/modulo"""
    source = r'''class Calc { void main() { int x := 1 + 2 * 3 - 4 \ 2 % 5; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_018():
    """String concatenation and escape sequences"""
    source = '''class S { void main() { string s := "Hello" ^ "\\n" ^ "World"; io.writeStrLn(s); } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_019():
    """Multiple classes in one file and mixed members"""
    source = '''class One { int a; } class Two { static void main() { One o; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_020():
    """Attributes with multiple declarators and initializers"""
    source = '''class C { static final int A := 1, B := 2; float x, y := 1.0; }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_021():
    """Nested loops using to and downto"""
    source = '''
    class L {
        void run() {
            for i := 0 to 3 do {
                for j := 10 downto 8 do { }
            }
        }
    }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_022():
    """If-then-else in both match and open forms"""
    source = '''
    class Ifs {
        void test() {
            if x == 0 then return x; else return 0; if x > 0 then a := 1;
        }
    }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_023():
    """Parameters: arrays, references and comma-separated ids"""
    source = '''class P { void m(int[5] arr; int a, b; int & r) { arr[0] := a; r := b; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_024():
    """Final and static modifiers in reversed order"""
    source = '''class M { final static int X := 42; static final float Y := 3.14; }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_025():
    """Method chaining and postfix calls"""
    source = '''class Ch { void t() { obj.foo().bar(1); } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_026():
    """Complex indexing and nested access"""
    source = '''
    class X extends Y {
        void f() {
            a[c.foo(1)].bar(new T(x, y)).baz := 5;
        }
    }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_027():
    """Assignment LHS can be uniexpr (array and member access)"""
    source = '''class AS { void test() { this.arr[0] := this.arr[0] + 1; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_028():
    """Return statements with expressions and nil"""
    source = '''class R { int foo() { return 1; } void bar() { return nil; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_029():
    """Object creation with parameters and assignment"""
    source = '''class New { void main() { Point p := new Point(1.0, 2.0); } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_030():
    """Static attribute access and modification"""
    source = '''class Counter { static int c := 0; static void inc() { Counter.c := Counter.c + 1; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_031():
    """Boolean and logical expressions with precedence"""
    source = '''class B { void t() { if (a <= b && !c) then d := 1; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_032():
    """Parameters declared together using comma-separated ids"""
    source = '''class Sum { int add(int a, b, c) { return a + b + c; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_033():
    """Copy constructor usage with object creation"""
    source = '''class C { C(C other) { } void main() { C a := new C(); C b := new C(a); } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_034():
    """Method returning reference to primitive or class"""
    source = '''class Out { int & getRef(int & x) { return x; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_035():
    """Static method invocation on class qualifiers and io calls"""
    source = '''class Demo { void main() { io.writeStrLn("ok"); Helper.doIt(); } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_036():
    """Attribute initialization using expressions referencing static members"""
    source = '''class A { static int n := 0; int x := A.n + 5; }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_037():
    """Comments: block and line comments should be ignored"""
    source = '''/* header */ class C { # a comment\n int x; /* inline */ x := 1; }'''
    expected = "Error on line 2 col 23: :="
    assert Parser(source).parse() == expected


def test_038():
    """Whitespace and comment robustness across tokens"""
    source = '''# start\nclass W { void m() { /* mid */ x := 1; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_039():
    """Break and continue statements inside loops"""
    source = '''class Flow { void test() { for i := 0 to 10 do { if i == 5 then break; if i == 7 then continue; } } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_040():
    """Complex for loop body with nested statements"""
    source = '''class ComplexFor { void run() { for i := 1 to 3 do { int t; for j := 0 to 2 do { t := i * j; } } } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_041():
    """Long identifiers and underscore handling"""
    source = '''class Long { void main() { very_long_identifier_name_with_underscores123 := 0; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_042():
    """Float literals and exponents in declarations"""
    source = '''class F { float a := 1.0e3; float b := 0.5; }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_043():
    """Strings with escape sequences are valid tokens"""
    source = '''class Str { void s() { string t := "Line\\nTab\\tQuote\\\""; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_044():
    """Multiple attributes and methods combined"""
    source = '''class Multi { static int s; final float PI := 3.14; void m() { s := s + 1; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_045():
    """Object creation with nested new expressions"""
    source = '''class Nest { void t() { A a := new A(new B(), 3); } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_046():
    """Method that returns an array reference type"""
    source = '''class AR { int[5] & getArr() { int[5] tmp; return tmp; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_047():
    """Constructor assigning to this.x and using parameters"""
    source = '''class Point { float x, y; Point(float x; float y) { this.x := x; this.y := y; } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_048():
    """IO method invocation and string literal printing"""
    source = '''class IOTest { void main() { io.writeStrLn("Hello World"); } }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_049():
    """Large class with many members (attributes, methods, constructor)"""
    source = r'''
    class Big {
        static int cnt;
        final int MAX := 10;
        Big() { cnt := cnt + 1; }
        void doIt() {
            int i;
            for i := 0 to MAX do { }
        }
    }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_050():
    """Comprehensive example combining features: new, arrays, refs, loops"""
    source = r'''class Full {
        int[3] data;
        static void main() {
            Full f := new Full();
            int i;
            int & r := f.data[0];
            r := 42;
            for i := 0 to 2 do { f.data[i] := i; }
        }
    }'''
    expected = "success"
    assert Parser(source).parse() == expected


def test_051():
    """Syntax error: missing closing parenthesis in method declaration"""
    source = '''
    class BadParen {
        void main( {
            int x := 1;
            io.writeInt(x);
        }
    }
    '''
    expected = "Error on line 3 col 19: {"
    assert Parser(source).parse() == expected


def test_052():
    """Lexical error: unexpected character in body"""
    source = '''
    class WeirdChar {
        static void main() {
            int a := 10;
            a := a @ 2;  # illegal '@' char
        }
    }
    '''
    expected = "Error Token @"
    assert Parser(source).parse() == expected


def test_053():
    """Syntax error: missing semicolon between statements in block"""
    source = '''
    class MissSemi {
        void foo() {
            int t := 0
            for i := 0 to 2 do { t := t + i; }
        }
    }
    '''
    expected = "Error on line 5 col 12: for"
    assert Parser(source).parse() == expected


def test_054():
    """Lexical error: illegal escape sequence inside string literal"""
    source = '''
    class BadString {
        void main() {
            string s := "This has bad escape \\q in it";
            io.writeStrLn(s);
        }
    }
    '''
    expected = "Illegal Escape In String: This has bad escape \\q"
    assert Parser(source).parse() == expected


def test_055():
    """Syntax error: unexpected token (extra comma in parameter list)"""
    source = '''
    class ExtraComma {
        void m(int a, , int b) { 
            a := a + b;
        }
    }
    '''
    expected = "Error on line 3 col 22: ,"
    assert Parser(source).parse() == expected


def test_056():
    """Syntax error: unclosed block (missing closing brace for class)"""
    source = '''
    class Unclosed {
        void main() {
            int x := 1;
        }
    '''
    expected = "Error on line 6 col 4: <EOF>"
    assert Parser(source).parse() == expected


def test_057():
    """Syntax error: using reserved keyword as identifier (e.g., 'for' as var)"""
    source = '''
    class KwId {
        void t() {
            int for := 1;
            io.writeInt(for);
        }
    }
    '''
    expected = "Error on line 4 col 16: for"
    assert Parser(source).parse() == expected


def test_058():
    """Syntax error: malformed array type (missing size literal)"""
    source = '''
    class ArrBad {
        void main() {
            int[] a;  # missing size literal between brackets
            a := {1,2,3};
        }
    }
    '''
    expected = "Error on line 4 col 16: ]"
    assert Parser(source).parse() == expected


def test_059():
    """Syntax error: malformed constructor (extra token)"""
    source = '''
    class Constr {
        Constr() extra { }
        void main() { Constr c := new Constr(); }
    }
    '''
    expected = "Error on line 3 col 17: extra"
    assert Parser(source).parse() == expected


def test_060():
    """Lexical error: unclosed string across lines (newline in string)"""
    source = '''
    class MultiLineStr {
        void main() {
            string s := "This string
continues on new line";
            io.writeStrLn(s);
        }
    }
    '''
    expected = "Unclosed String: This string"
    assert Parser(source).parse() == expected
