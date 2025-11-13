from utils import Checker
from utils import *


def test_001():
    source = """
class Base { static void main(boolean z) { } }
class Base extends Base {
    int a, b;
    final string CC := 1;

}
"""
    expected = "Redeclared(Class, Base)"
    assert Checker(source).check_from_source() == expected

def test_002():
    source = """
class Base { static void main(boolean z) { } }
class Test extends Base {
    int a, b, c := 1;
    final string c := 1;

}
"""
    expected = "Redeclared(Constant, c)"
    assert Checker(source).check_from_source() == expected

def test_003():
    source = """
class Weight {
    static int x := 0, y := 0;
    Weight(float x, y, z; int z) { }
}
"""
    expected = "Redeclared(Parameter, z)"
    assert Checker(source).check_from_source() == expected

def test_004():
    source = """
class Weight {
    static int x := 0, y := 0;
    Weight(float x, y, z; int t) { }
    ~Weight() { }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_005():
    source = """
class Weight {
    static int x := 0, y := 0;
    Weight(float x, y, z; int t) { }
    ~Weight() { }
    
    static void Weight(float x; boolean z) {
        int a := 1;
    }
}
"""
    expected = "Redeclared(Method, Weight)"
    assert Checker(source).check_from_source() == expected

def test_006():
    source = """
class Weight {
    static int x := 0, y := 0;
    Weight(float x, y, z; int t) { }
    ~Weight() { }
    
    static void main() {
        final int a := 1;
        final float a;
    }
}
"""
    expected = "Redeclared(Constant, a)"
    assert Checker(source).check_from_source() == expected

def test_007():
    source = """
class Weight {
    static int x := 0, y := 0;
    Weight(float x, y, z; int t) { }
    ~Weight() { }
    
    static void main() {
        final int a := 1;
        float b, c, f, d, b;
    }
}
"""
    expected = "Redeclared(Variable, b)"
    assert Checker(source).check_from_source() == expected


def test_008():
    source = """
class Base { static void main(boolean z) { int a := 3; } }
class Weight extends Base {
    static int x := 0, y := 0;
    Weight(float x, y, z; int t) { }
    ~Weight() { }
    
    static void main() {
        final int a := 1;
        {
            float a, b;
            {
                boolean a;
            }
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_009():
    source = """
class Base { static void main(boolean z) { int a := 3; } }
class Weight extends Base {
    static int x := 0, y := 0;
    Weight(float x, y, z; int t) { }
    ~Weight() { }
    
    static void main() {
        final int a := 1;
        {
            float a, b;
            {
                boolean a, a;
            }
        }
    }
}
"""
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected

def test_010():
    source = """
class Base {
    final int X := 11 + 33*2 \\ 5;
    final float PI;
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected

def test_011():
    source = """
class Base {
    final int Y := 10 % 3, X := 11 + 5 / 2;
    final float PI;
}
"""
    expr = AttributeDecl(
        False, True, PrimitiveType("int"), [
            Attribute("Y", BinaryOp(IntLiteral(10), "%", IntLiteral(3))),
            Attribute("X", BinaryOp(IntLiteral(11), "+", BinaryOp(IntLiteral(5), "/", IntLiteral(2)))),
        ]
    )
    expected = f"TypeMismatchInConstant({expr})"
    assert Checker(source).check_from_source() == expected

def test_012():
    source = """
class Base {
    final int[5] test := { 100232, 34123, 235346, 2324232, 12 };
    final int[2] empty := { 1, 2, 3 };
}
"""
    expr = AttributeDecl(
        False, True, ArrayType(PrimitiveType("int"), 2), [Attribute("empty",
            ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)])
        )]
    )
    expected = f"TypeMismatchInConstant({expr})"
    assert Checker(source).check_from_source() == expected

def test_013():
    source = """
class Base {
    final int[5] test := { 100232, 34123, 235346, 2324232, 12 };
    
    boolean is_bad(string apple) {
        final string s := "hello, world!", test_str := 3;
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(string), [Variable(s = StringLiteral('hello, world!')), Variable(test_str = IntLiteral(3))]))"
    assert Checker(source).check_from_source() == expected

def test_014():
    source = """
class VeryBase { int x, y, z; }
class Base extends VeryBase{
    final int[5] test := { 100232, 34123, 235346, 2324232, 12 };
    
    boolean is_bad(string apple) {
        final string s := "hello, world!";
        final float[0] num_list := { };
        final VeryBase[999] obj_list := { };
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final ArrayType(ClassType(VeryBase)[999]), [Variable(obj_list = ArrayLiteral({}))]))"
    assert Checker(source).check_from_source() == expected

def test_015():
    source = """
class VeryBase { int x, y, z; }
class Base extends VeryBase{
    final int[5] test := { 100232, 34123, 235346, 2324232, 12 };
    
    boolean is_bad(string apple) {
        final string s := "hello, world!";
        final float[0] num_list := { };
        final _VeryBase[999] obj_list := { };
    }
}
"""
    expected = "UndeclaredClass(_VeryBase)"
    assert Checker(source).check_from_source() == expected

def test_016():
    source = """
class VeryBase {
    int x, y, z;
    float compute_area(Shape s; float dA) { }
}
"""
    expected = "UndeclaredClass(Shape)"
    assert Checker(source).check_from_source() == expected

def test_017():
    source = """
class Shape { }
class VeryBase {
    int x, y, z;
    float compute_area(Shape s; float dA) { }
    VeryBase(float x, y, z; Shape x) { }
}
"""
    expected = "Redeclared(Parameter, x)"
    assert Checker(source).check_from_source() == expected

def test_018():
    source = """
class Shape { }
class VeryBase {
    int x, y, z;
    float compute_area(Shape s; float dA) { }
    VeryBase(float x, y, z; Shape s) {
        int[2] nums := {1, "hello"};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), StringLiteral('hello')}))"
    assert Checker(source).check_from_source() == expected

def test_019():
    source = """
class Shape { static int length := 10; }
class Test {
    int t := Shape.length;
    final float s := Shape.length;
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(Shape).length))"
    assert Checker(source).check_from_source() == expected

def test_020():
    source = """
class Shape { float width := 5, height := 4; static float depth := 1; }
class Test {
    float z := (new Shape()).width, y := Shape.depth;
    int t := Shape.width;
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Shape).width))"
    assert Checker(source).check_from_source() == expected

def test_021():
    source = """
class Shape {
    int get_random(int low, high; float state) { }
}
class Test {
    float z;
    static void main() {
        Shape obj := new Shape();
        z := obj.get_random(0, 5.0, 42);
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(obj).get_random(IntLiteral(0), FloatLiteral(5.0), IntLiteral(42))))"
    assert Checker(source).check_from_source() == expected

def test_022():
    source = """
class Shape {
    int get_random(int low, high; float state) { }
}
class Test {
    final float z := 3.14;
    static void main() {
        Shape obj := new Shape();
        float random_num := obj.get_random(obj.get_random(0, 1, 1), 12 \\ 4 % (-1 + obj.get_random(0, 2, 42)), 42.5);
        z := random_num;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(z) := Identifier(random_num)))"
    assert Checker(source).check_from_source() == expected

def test_023():
    source = """
class Shape {
    int get_random(int low, high; float state) { }
}
class Test {
    float z := 3.14;
    static void main() {
        Shape obj := new Shape();
        float random_num := obj.get_random(obj.get_random(0, 1, 1), 12 \\ 4 % (-1 + obj.get_random(0, 2, 42)), 42.5);
        z := true;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(z) := BoolLiteral(True)))"
    assert Checker(source).check_from_source() == expected

def test_024():
    source = """
class Test {
    static void main() {
        final boolean x := true, y := false, z := true;
        if (!z || y && x) then {
            z := true;
        }
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(z) := BoolLiteral(True)))"
    assert Checker(source).check_from_source() == expected

def test_025():
    source = """
class Test {
    int state;
    static int get_random() { }
    
    static void main() {
        final boolean x := true, y := false, z := true;
        final int a := 5, b := 10, c := 15;
        if (Test.get_random() > c + b * a) then {
            state := 30;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_026():
    source = """
class Test {
    int state;
    static int get_random() { }

    static void main() {
        final boolean x := true, y := false, z := true;
        final int a := 5, b := 10, c := 15;
        if (this.get_random() > c + b * a) then {
            state := 30;
        }
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(ThisExpression(this).get_random()))"
    assert Checker(source).check_from_source() == expected

def test_027():
    source = """
class Base {
    final float PI := 3.14;
    float area(float r) {  }
}
class Test extends Base {
    int state;
    static int get_random() { }
    
    static void main() {
        final float a := this.area(5.9);
    }
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).area(FloatLiteral(5.9))))"
    assert Checker(source).check_from_source() == expected

def test_028():
    source = """
class Base {
    int x := 1;
    final float PI := 3.14;
    float area(float r) {  }
}
class Test extends Base {
    int x := 10;
    static int get_random() { }
    
    static void main() {
        float a := this.area(5.9);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_029():
    source = """
class ForLoopError {
    void loop() {
        float f := 1.5;
        boolean condition := true;
        
        for i := condition to 10 do {
            f := 1;
        }
    }
}

"""
    expected = "TypeMismatchInStatement(ForStatement(for i := Identifier(condition) to IntLiteral(10) do BlockStatement(stmts=[AssignmentStatement(IdLHS(f) := IntLiteral(1))])))"
    assert Checker(source).check_from_source() == expected

def test_030():
    source = """
class ForLoopError {
    void loop() {
        float f := 1.5;
        final int start := 0;
        final int end := 999;
        
        for i := (start - end % 3 + start \\ 2) to (end - end) do {
            for f := start to end do { }
        }
    }
}

"""
    expected = "TypeMismatchInStatement(ForStatement(for f := Identifier(start) to Identifier(end) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_031():
    source = """
class ForLoopError {
    void loop() {
        final int start := 0;
        final int end := 999;
        
        for i := (start - end % 3 + start \\ 2) to (end - end) do {
            for f := start to end do {
                continue;
            }
            continue;
        }
        break;
    }
}

"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_032():
    source = """
class ForLoopError {
    void loop() {
        float f := nil;
        final int start := 0;
        final int end := 999;
        
        for i := (start - end % 3 + start \\ 2) to (end - end) do {
            for f := start to end do { }
        }
    }
}

"""
    expected = "TypeMismatchInStatement(ForStatement(for f := Identifier(start) to Identifier(end) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_033():
    source = """
class Test {
    static void main() {
        int x := 5;
        int y := x + 1;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_034():
    """Test redeclared variable error"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int x := 10;
    }
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_035():
    """Test undeclared identifier error"""
    source = """
class Test {
    static void main() {
        int x := y + 1;
    }
}
"""
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected

def test_036():
    """Test type mismatch error"""
    source = """
class Test {
    static void main() {
        int x := "hello";
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = StringLiteral('hello'))]))"
    assert Checker(source).check_from_source() == expected

def test_037():
    """Test break not in loop error"""
    source = """
class Test {
    static void main() {
        break;
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_038():
    """Test cannot assign to constant error"""
    source = """
class Test {
    static void main() {
        final int x := 5;
        x := 10;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(10)))"
    assert Checker(source).check_from_source() == expected

def test_039():
    """Test illegal array literal error - alternative case"""
    source = """
class Test {
    static void main() {
        boolean[2] flags := {true, 42};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected
