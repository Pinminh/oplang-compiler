from tests.utils import ASTGenerator
from src.utils.nodes import *

def test_001():
    """Test basic class declaration AST generation"""
    source = """class TestClass {
        int x;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)])])])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected


def test_002():
    """Test class with method declaration AST generation"""
    source = """class TestClass {
        void main() {
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_003():
    """Test class with constructor AST generation"""
    source = """class TestClass {
        int x;
        TestClass(int x) {
            this.x := x;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)]), ConstructorDecl(TestClass([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_004():
    """Test class with inheritance AST generation"""
    source = """class Child extends Parent {
        int y;
    }"""
    expected = "Program([ClassDecl(Child, extends Parent, [AttributeDecl(PrimitiveType(int), [Attribute(y)])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_005():
    """Test static and final attributes AST generation"""
    source = """class TestClass {
        static final int MAX_SIZE := 100;
        final float PI := 3.14;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(static final PrimitiveType(int), [Attribute(MAX_SIZE = IntLiteral(100))]), AttributeDecl(final PrimitiveType(float), [Attribute(PI = FloatLiteral(3.14))])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_006():
    """Test if-else statement AST generation"""
    source = """class TestClass {
        void main() {
            if x > 0 then {
                return x;
            } else {
                return 0;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[ReturnStatement(return Identifier(x))]), else BlockStatement(stmts=[ReturnStatement(return IntLiteral(0))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007():
    """Test for loop AST generation"""
    source = """class TestClass {
        void main() {
            int sum := 0;
            for i := 1 to 10 do {
                sum := sum + i;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(sum = IntLiteral(0))])], stmts=[ForStatement(for i := IntLiteral(1) to IntLiteral(10) do BlockStatement(stmts=[AssignmentStatement(IdLHS(sum) := BinaryOp(Identifier(sum), +, Identifier(i)))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_008():
    """Test array operations AST generation"""
    source = """class TestClass {
        void main() {
            int[5] arr;
            arr[0] := 42;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ArrayType(PrimitiveType(int)[5]), [Variable(arr)])], stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[IntLiteral(0)])) := IntLiteral(42))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_009():
    """Test object creation and method call AST generation"""
    source = """class TestClass {
        void main() {
            Rectangle r := new Rectangle(5.0, 3.0);
            float area := r.getArea();
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(Rectangle), [Variable(r = ObjectCreation(new Rectangle(FloatLiteral(5.0), FloatLiteral(3.0))))]), VariableDecl(PrimitiveType(float), [Variable(area = PostfixExpression(Identifier(r).getArea()))])], stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_010():
    """Test reference type AST generation"""
    source = """class TestClass {
        void swap(int & a; int & b) {
            int temp := a;
            a := b;
            b := temp;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) swap([Parameter(ReferenceType(PrimitiveType(int) &) a), Parameter(ReferenceType(PrimitiveType(int) &) b)]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(temp = Identifier(a))])], stmts=[AssignmentStatement(IdLHS(a) := Identifier(b)), AssignmentStatement(IdLHS(b) := Identifier(temp))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_011():
    """Test destructor AST generation"""
    source = """class TestClass {
        ~TestClass() {
            int x := 0;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [DestructorDecl(~TestClass(), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(x = IntLiteral(0))])], stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_012():
    """Test compound expressions and operator precedence"""
    source = """class TestClass {
        int calculate() {
            return (a + b) * c + x % y;
        }
    }"""
    program = Program([
        ClassDecl("TestClass", superclass=None, members=[
            MethodDecl(False, PrimitiveType("int"), "calculate", [], BlockStatement(
                var_decls=[],
                statements=[ReturnStatement(
                    BinaryOp(
                        BinaryOp(ParenthesizedExpression(BinaryOp(Identifier("a"), "+", Identifier("b"))), "*", Identifier("c")),
                        "+",
                        BinaryOp(Identifier("x"), "%", Identifier("y"))
                    )
                )]
            ))
        ])
    ])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_013():
    """Test array operations and array literals"""
    source = """class TestClass {
        int[3] numbers := {1, 2, 3};
        void processArray() {
            numbers[0] := numbers[1] + numbers[2];
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(ArrayType(PrimitiveType(int)[3]), [Attribute(numbers = ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3)}))]), MethodDecl(PrimitiveType(void) processArray([]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(numbers)[IntLiteral(0)])) := BinaryOp(PostfixExpression(Identifier(numbers)[IntLiteral(1)]), +, PostfixExpression(Identifier(numbers)[IntLiteral(2)])))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_014():
    """Test reference parameters and return types"""
    source = """class TestClass {
        int & getMaxRef(int & a; int & b) {
            if a > b then {
                return a;
            } else {
                return b;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(ReferenceType(PrimitiveType(int) &) getMaxRef([Parameter(ReferenceType(PrimitiveType(int) &) a), Parameter(ReferenceType(PrimitiveType(int) &) b)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(a), >, Identifier(b)) then BlockStatement(stmts=[ReturnStatement(return Identifier(a))]), else BlockStatement(stmts=[ReturnStatement(return Identifier(b))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_015():
    """Test complex class hierarchy with all constructor types"""
    source = """class Shape {
        float width;
        Shape(float w) {
            this.width := w;
        }
        Shape(Shape other) {
            this.width := other.width;
        }
    }
    class Circle extends Shape {
        static final float PI := 3.14159;
        Circle() {
            width := 1.0;
        }
    }"""
    expected = "Program([ClassDecl(Shape, [AttributeDecl(PrimitiveType(float), [Attribute(width)]), ConstructorDecl(Shape([Parameter(PrimitiveType(float) w)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).width)) := Identifier(w))])), ConstructorDecl(Shape([Parameter(ClassType(Shape) other)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).width)) := PostfixExpression(Identifier(other).width))]))]), ClassDecl(Circle, extends Shape, [AttributeDecl(static final PrimitiveType(float), [Attribute(PI = FloatLiteral(3.14159))]), ConstructorDecl(Circle([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(width) := FloatLiteral(1.0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_016():
    """Test different literal types and expressions"""
    source = """class TestClass {
        boolean testLiterals() {
            string str := "Hello" ^ " World";
            boolean b := true && !false;
            final float f := 1.23e-4, g := 3.14;
            Shape s := nil;
            return b;
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        MethodDecl(False, PrimitiveType("boolean"), "testLiterals", [], BlockStatement(
            var_decls=[
                VariableDecl(False, PrimitiveType("string"), [Variable("str", BinaryOp(StringLiteral("Hello"), "^", StringLiteral(" World")))]),
                VariableDecl(False, PrimitiveType("boolean"), [Variable("b", BinaryOp(BoolLiteral(True), "&&", UnaryOp("!", BoolLiteral("False"))))]),
                VariableDecl(True, PrimitiveType("float"), [Variable("f", FloatLiteral(1.23e-4)), Variable("g", FloatLiteral(3.14))]),
                VariableDecl(False, ClassType("Shape"), [Variable("s", NilLiteral())])
            ],
            statements=[ReturnStatement(Identifier("b"))]
        ))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_017():
    """Test static and instance method combinations"""
    source = """class TestClass {
        static void printStatic() {
            return "static";
        }
        void printInstance() {
            this.printStatic();
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        MethodDecl(True, PrimitiveType("void"), "printStatic", [], BlockStatement(
            var_decls=[],
            statements=[ReturnStatement(StringLiteral("static"))]
        )),
        MethodDecl(False, PrimitiveType("void"), "printInstance", [], BlockStatement(
            var_decls=[],
            statements=[MethodInvocationStatement(PostfixExpression(
                ThisExpression(),
                [MethodCall("printStatic", [])]
            ))]
        ))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_018():
    """Test complex object creation and method chaining"""
    source = """class TestClass {
        Shape createAndModify() {
            Shape s := new Circle(5.0);
            return s.setColor("red").move(1, 2);
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        MethodDecl(False, ClassType("Shape"), "createAndModify", [], BlockStatement(
            var_decls=[VariableDecl(False, ClassType("Shape"), [Variable("s", ObjectCreation("Circle", [FloatLiteral(5.0)]))])],
            statements=[ReturnStatement(
                PostfixExpression(Identifier("s"), [
                    MethodCall("setColor", [StringLiteral("red")]),
                    MethodCall("move", [IntLiteral(1), IntLiteral(2)])
                ])
            )]
        ))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_019():
    """Test nested if-then-else statements"""
    source = """class TestClass {
        void testNested() {
            if x > 0 then {
                if y > 0 then {
                    return x;
                } else {
                    return y;
                }
            } else {
                return 0;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) testNested([]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(y), >, IntLiteral(0)) then BlockStatement(stmts=[ReturnStatement(return Identifier(x))]), else BlockStatement(stmts=[ReturnStatement(return Identifier(y))]))]), else BlockStatement(stmts=[ReturnStatement(return IntLiteral(0))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_020():
    """Test for loops with array operations"""
    source = """class TestClass {
        void processArrays() {
            int[5] arr;
            for i := 0 to 4 do {
                arr[i] := i * i;
            }
            for i := 4 downto 0 do {
                arr[i] := arr[i] * 2;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) processArrays([]), BlockStatement(vars=[VariableDecl(ArrayType(PrimitiveType(int)[5]), [Variable(arr)])], stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(4) do BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[Identifier(i)])) := BinaryOp(Identifier(i), *, Identifier(i)))])), ForStatement(for i := IntLiteral(4) downto IntLiteral(0) do BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[Identifier(i)])) := BinaryOp(PostfixExpression(Identifier(arr)[Identifier(i)]), *, IntLiteral(2)))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_021():
    """Test multi-dimensional array types and operations"""
    source = """class TestClass {
        int[2] matrix;
        void initMatrix() {
            matrix[0][0] := 1;
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        AttributeDecl(False, False, ArrayType(PrimitiveType("int"), 2), [Attribute("matrix")]),
        MethodDecl(False, PrimitiveType("void"), "initMatrix", [], BlockStatement(
            var_decls=[],
            statements=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier("matrix"), [ArrayAccess(IntLiteral(0)), ArrayAccess(IntLiteral(0))])), IntLiteral(1))]
        ))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_022():
    """Test complex string operations and concatenation"""
    source = """class TestClass {
        string buildMessage() {
            string prefix := "Hello";
            string suffix := "World";
            return prefix ^ " " ^ suffix ^ "!";
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        MethodDecl(False, PrimitiveType("string"), "buildMessage", [], BlockStatement(
            var_decls=[
                VariableDecl(False, PrimitiveType("string"), [Variable("prefix", StringLiteral("Hello"))]),
                VariableDecl(False, PrimitiveType("string"), [Variable("suffix", StringLiteral("World"))])
            ],
            statements=[ReturnStatement(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            Identifier("prefix"),
                            "^",
                            StringLiteral(" ")
                        ),
                        "^",
                        Identifier("suffix")
                    ),
                    "^",
                    StringLiteral("!")
                )
            )]
        ))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_023():
    """Test all arithmetic operators and operator precedence"""
    source = """class TestClass {
        float calculate() {
            return -a * b \\ 3 + (c - d) % e;
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        MethodDecl(False, PrimitiveType("float"), "calculate", [], BlockStatement(
            var_decls=[],
            statements=[ReturnStatement(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            UnaryOp("-", Identifier("a")),
                            "*",
                            Identifier("b")
                        ),
                        "\\",
                        IntLiteral(3)
                    ),
                    "+",
                    BinaryOp(
                        ParenthesizedExpression(BinaryOp(
                            Identifier("c"),
                            "-",
                            Identifier("d")
                        )),
                        "%",
                        Identifier("e")
                    )
                )
            )]
        ))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_024():
    """Test all comparison operators"""
    source = """class TestClass {
        boolean compare() {
            return (a < b) && (c > d) || (e <= f) && (g >= h) || (i == j) && (k != l);
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        MethodDecl(False, PrimitiveType("boolean"), "compare", [], BlockStatement([], [ReturnStatement(
            BinaryOp(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            BinaryOp(
                                ParenthesizedExpression(BinaryOp(
                                    Identifier("a"), "<", Identifier("b")
                                )),
                                "&&",
                                ParenthesizedExpression(BinaryOp(
                                    Identifier("c"), ">", Identifier("d")
                                ))
                            ),
                            "||",
                            ParenthesizedExpression(BinaryOp(
                                Identifier("e"), "<=", Identifier("f")
                            ))
                        ),
                        "&&",
                        ParenthesizedExpression(BinaryOp(
                            Identifier("g"), ">=", Identifier("h")
                        ))
                    ),
                    "||",
                    ParenthesizedExpression(BinaryOp(
                        Identifier("i"), "==", Identifier("j")
                    ))
                ),
                "&&",
                ParenthesizedExpression(BinaryOp(
                    Identifier("k"), "!=", Identifier("l")
                ))
            )
        )]))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_025():
    """Test complex array and object initialization"""
    source = """
    class Shape {
        static string print() { return "shape"; }
    }
    class Circle extends Shape { float r; }
    class Rectangle extends Shape { float x, y; }
    class TestClass {
        static final int[2] shapes := {1.0, "haha", true};
    }"""
    program = Program([
        ClassDecl("Shape", None, [
            MethodDecl(True, PrimitiveType("string"), "print", [], BlockStatement([], [ReturnStatement(StringLiteral("shape"))]))
        ]),
        ClassDecl("Circle", "Shape", [
            AttributeDecl(False, False, PrimitiveType("float"), [Attribute("r")])
        ]),
        ClassDecl("Rectangle", "Shape", [
            AttributeDecl(False, False, PrimitiveType("float"), [Attribute("x"), Attribute("y")])
        ]),
        ClassDecl("TestClass", None, [
            AttributeDecl(True, True, ArrayType(PrimitiveType("int"), 2), [
                Attribute("shapes", ArrayLiteral([
                    FloatLiteral(1.0),
                    StringLiteral("haha"),
                    BoolLiteral(True)
                ]))
            ])
        ])
    ])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_026():
    """Test all three constructor types in one class"""
    source = """class TestClass {
        int x;
        float y;
        TestClass() {
            x := 0;
            y := 0.0;
        }
        TestClass(TestClass other) {
            x := other.x;
            y := other.y;
        }
        TestClass(int x; float y) {
            this.x := x;
            this.y := y;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)]), AttributeDecl(PrimitiveType(float), [Attribute(y)]), ConstructorDecl(TestClass([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := IntLiteral(0)), AssignmentStatement(IdLHS(y) := FloatLiteral(0.0))])), ConstructorDecl(TestClass([Parameter(ClassType(TestClass) other)]), BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := PostfixExpression(Identifier(other).x)), AssignmentStatement(IdLHS(y) := PostfixExpression(Identifier(other).y))])), ConstructorDecl(TestClass([Parameter(PrimitiveType(int) x), Parameter(PrimitiveType(float) y)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x)), AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).y)) := Identifier(y))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_027():
    """Test static block with complex initialization"""
    source = """class TestClass {
        static final int MAX_SIZE := 100;
        static int[256] cache;
        void initCache() {
            for i := 0 to MAX_SIZE - 1 do {
                cache[i] := i * i;
            }
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        AttributeDecl(True, True, PrimitiveType("int"), [Attribute("MAX_SIZE", IntLiteral(100))]),
        AttributeDecl(True, False, ArrayType(PrimitiveType("int"), 256), [Attribute("cache")]),
        MethodDecl(False, PrimitiveType("void"), "initCache", [], BlockStatement(
            var_decls=[],
            statements=[ForStatement("i", IntLiteral(0), "to", BinaryOp(Identifier("MAX_SIZE"), "-", IntLiteral(1)), BlockStatement([], [
                AssignmentStatement(PostfixLHS(PostfixExpression(Identifier("cache"), [ArrayAccess(Identifier("i"))])), BinaryOp(Identifier("i"), "*", Identifier("i")))
            ]))]
        ))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_028():
    """Test complex method overloading in class hierarchy"""
    source = """
    class Animal {
        string makeSound() {
            return "generic";
        }
    }
    class Cat extends Animal {
        string makeSound() {
            return this.makeSound() ^ " meow";
        }
    }"""
    program = Program([
        ClassDecl("Animal", None, [
            MethodDecl(False, PrimitiveType("string"), "makeSound", [], BlockStatement([], [
                ReturnStatement(StringLiteral("generic"))
            ]))
        ]),
        ClassDecl("Cat", "Animal", [
            MethodDecl(False, PrimitiveType("string"), "makeSound", [], BlockStatement([], [
                ReturnStatement(BinaryOp(
                    PostfixExpression(ThisExpression(), [MethodCall("makeSound", [])]),
                    "^",
                    StringLiteral(" meow")
                ))
            ]))
        ])
    ])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_029():
    """Test break and continue statements in nested loops"""
    source = """class TestClass {
        void processMatrix(int[5] mat) {
            for i := 0 to 4 do {
                for j := 0 to 4 do {
                    if mat[i] == 0 then {
                        continue;
                    }
                    if mat[j] < 0 then {
                        break;
                    }
                }
            }
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        MethodDecl(False, PrimitiveType("void"), "processMatrix", [Parameter(ArrayType(PrimitiveType("int"), 5), "mat")], BlockStatement([], [
            ForStatement("i", IntLiteral(0), "to", IntLiteral(4), BlockStatement([], [
                ForStatement("j", IntLiteral(0), "to", IntLiteral(4), BlockStatement([], [
                    IfStatement(BinaryOp(PostfixExpression(Identifier("mat"), [ArrayAccess(Identifier("i"))]), "==", IntLiteral(0)), BlockStatement([], [
                        ContinueStatement()
                    ])),
                    IfStatement(BinaryOp(PostfixExpression(Identifier("mat"), [ArrayAccess(Identifier("j"))]), "<", IntLiteral(0)), BlockStatement([], [
                        BreakStatement()
                    ]))
                ]))
            ]))
        ]))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

def test_030():
    """Test complex boolean expressions with short-circuit operators"""
    source = """class TestClass {
        boolean evaluate(int x; int y) {
            return (x > 0 && y) || (x && y < 0) && !(x == 0 || y);
        }
    }"""
    program = Program([ClassDecl("TestClass", None, [
        MethodDecl(False, PrimitiveType("boolean"), "evaluate", [Parameter(PrimitiveType("int"), name) for name in ["x", "y"]], BlockStatement([], [
            ReturnStatement(BinaryOp(
                BinaryOp(
                    ParenthesizedExpression(BinaryOp(
                        Identifier("x"), ">", BinaryOp(IntLiteral(0), "&&", Identifier("y"))
                    )),
                    "||",
                    ParenthesizedExpression(BinaryOp(
                        BinaryOp(Identifier("x"), "&&", Identifier("y")), "<", IntLiteral(0)
                    ))
                ),
                "&&",
                UnaryOp("!", ParenthesizedExpression(BinaryOp(
                    Identifier("x"), "==", BinaryOp(IntLiteral(0), "||", Identifier("y"))
                )))
            ))
        ]))
    ])])
    expected = str(program)
    assert str(ASTGenerator(source).generate()) == expected

# def test_031():
#     """Test multiple array dimensions with complex indexing"""
#     source = """class TestClass {
#         int[2][3][4] cube;
#         int getValue(int i; int j; int k) {
#             return cube[i][j][k];
#         }
#         void setValue(int i; int j; int k; int value) {
#             cube[i][j][k] := value;
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ArrayType(ArrayType(ArrayType(PrimitiveType(int)[2])[3])[4]), [Attribute(cube)]), MethodDecl(PrimitiveType(int) getValue([Parameter(PrimitiveType(int) i), Parameter(PrimitiveType(int) j), Parameter(PrimitiveType(int) k)]), BlockStatement(stmts=[ReturnStatement(return PostfixExpression(Identifier(cube)[Identifier(i)][Identifier(j)][Identifier(k)]))])), MethodDecl(PrimitiveType(void) setValue([Parameter(PrimitiveType(int) i), Parameter(PrimitiveType(int) j), Parameter(PrimitiveType(int) k), Parameter(PrimitiveType(int) value)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(cube)[Identifier(i)][Identifier(j)][Identifier(k)])) := Identifier(value))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_032():
#     """Test complex reference type declarations and operations"""
#     source = """class TestClass {
#         void swapAndModify(int & x; int & y) {
#             int temp := x;
#             x := y + 1;
#             y := temp - 1;
#         }
#         int & getMax(int & a; int & b; int & c) {
#             if a >= b && a >= c then {
#                 return a;
#             } else if b >= a && b >= c then {
#                 return b;
#             } else {
#                 return c;
#             }
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) swapAndModify([Parameter(ReferenceType(PrimitiveType(int) &) x), Parameter(ReferenceType(PrimitiveType(int) &) y)]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(temp = Identifier(x))])], stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(y), +, IntLiteral(1))), AssignmentStatement(IdLHS(y) := BinaryOp(Identifier(temp), -, IntLiteral(1)))])), MethodDecl(ReferenceType(PrimitiveType(int) &) getMax([Parameter(ReferenceType(PrimitiveType(int) &) a), Parameter(ReferenceType(PrimitiveType(int) &) b), Parameter(ReferenceType(PrimitiveType(int) &) c)]), BlockStatement(stmts=[IfStatement(if BinaryOp(BinaryOp(Identifier(a), >=, Identifier(b)), &&, BinaryOp(Identifier(a), >=, Identifier(c))) then BlockStatement(stmts=[ReturnStatement(return Identifier(a))]), else IfStatement(if BinaryOp(BinaryOp(Identifier(b), >=, Identifier(a)), &&, BinaryOp(Identifier(b), >=, Identifier(c))) then BlockStatement(stmts=[ReturnStatement(return Identifier(b))]), else BlockStatement(stmts=[ReturnStatement(return Identifier(c))])))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_033():
#     """Test method chaining with different return types"""
#     source = """class Shape {
#         Shape setColor(string color) {
#             return this;
#         }
#         Shape move(float x; float y) {
#             return this;
#         }
#         Shape & getReference() {
#             return this;
#         }
#     }"""
#     expected = "Program([ClassDecl(Shape, [MethodDecl(ClassType(Shape) setColor([Parameter(PrimitiveType(string) color)]), BlockStatement(stmts=[ReturnStatement(return ThisExpression(this))])), MethodDecl(ClassType(Shape) move([Parameter(PrimitiveType(float) x), Parameter(PrimitiveType(float) y)]), BlockStatement(stmts=[ReturnStatement(return ThisExpression(this))])), MethodDecl(ReferenceType(ClassType(Shape) &) getReference([]), BlockStatement(stmts=[ReturnStatement(return ThisExpression(this))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_034():
#     """Test complex class hierarchy with nested types"""
#     source = """class Container {
#         class Node {
#             Node next;
#             int value;
#             Node(int v) {
#                 value := v;
#                 next := nil;
#             }
#         }
#         Node head;
#         void add(int value) {
#             head := new Node(value);
#         }
#     }"""
#     expected = "Program([ClassDecl(Container, [ClassDecl(Node, [AttributeDecl(ClassType(Node), [Attribute(next)]), AttributeDecl(PrimitiveType(int), [Attribute(value)]), ConstructorDecl(Node([Parameter(PrimitiveType(int) v)]), BlockStatement(stmts=[AssignmentStatement(IdLHS(value) := Identifier(v)), AssignmentStatement(IdLHS(next) := NilLiteral(nil))]))]), AttributeDecl(ClassType(Node), [Attribute(head)]), MethodDecl(PrimitiveType(void) add([Parameter(PrimitiveType(int) value)]), BlockStatement(stmts=[AssignmentStatement(IdLHS(head) := ObjectCreation(new Node(Identifier(value))))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_035():
#     """Test static and instance initialization with array operations"""
#     source = """class Matrix {
#         static int SIZE := 3;
#         int[3][3] data;
#         Matrix() {
#             for i := 0 to SIZE - 1 do {
#                 for j := 0 to SIZE - 1 do {
#                     data[i][j] := 0;
#                 }
#             }
#         }
#         static Matrix identity() {
#             Matrix m := new Matrix();
#             for i := 0 to SIZE - 1 do {
#                 m.data[i][i] := 1;
#             }
#             return m;
#         }
#     }"""
#     expected = "Program([ClassDecl(Matrix, [AttributeDecl(static PrimitiveType(int), [Attribute(SIZE = IntLiteral(3))]), AttributeDecl(ArrayType(ArrayType(PrimitiveType(int)[3])[3]), [Attribute(data)]), ConstructorDecl(Matrix([]), BlockStatement(stmts=[ForStatement(for i := IntLiteral(0) to BinaryOp(Identifier(SIZE), -, IntLiteral(1)) do BlockStatement(stmts=[ForStatement(for j := IntLiteral(0) to BinaryOp(Identifier(SIZE), -, IntLiteral(1)) do BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(data)[Identifier(i)][Identifier(j)])) := IntLiteral(0))]))]))])), MethodDecl(static ClassType(Matrix) identity([]), BlockStatement(vars=[VariableDecl(ClassType(Matrix), [Variable(m = ObjectCreation(new Matrix()))])], stmts=[ForStatement(for i := IntLiteral(0) to BinaryOp(Identifier(SIZE), -, IntLiteral(1)) do BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(m).data[Identifier(i)][Identifier(i)])) := IntLiteral(1))])), ReturnStatement(return Identifier(m))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_036():
#     """Test float literals in different formats"""
#     source = """class TestClass {
#         float[5] numbers := {1.0, .5e2, 1.23e-4, 5E+10, 123.456};
#         float getSum() {
#             float sum := 0.0;
#             for i := 0 to 4 do {
#                 sum := sum + numbers[i];
#             }
#             return sum;
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ArrayType(PrimitiveType(float)[5]), [Attribute(numbers = ArrayLiteral({FloatLiteral(1.0), FloatLiteral(50.0), FloatLiteral(0.000123), FloatLiteral(5e10), FloatLiteral(123.456)}))]), MethodDecl(PrimitiveType(float) getSum([]), BlockStatement(vars=[VariableDecl(PrimitiveType(float), [Variable(sum = FloatLiteral(0.0))])], stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(4) do BlockStatement(stmts=[AssignmentStatement(IdLHS(sum) := BinaryOp(Identifier(sum), +, PostfixExpression(Identifier(numbers)[Identifier(i)])))])), ReturnStatement(return Identifier(sum))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_037():
#     """Test complex string manipulation and concatenation"""
#     source = """class StringUtils {
#         static string trim(string str) {
#             return str;
#         }
#         static string repeat(string str; int times) {
#             string result := "";
#             for i := 1 to times do {
#                 result := result ^ str;
#             }
#             return result;
#         }
#     }"""
#     expected = "Program([ClassDecl(StringUtils, [MethodDecl(static PrimitiveType(string) trim([Parameter(PrimitiveType(string) str)]), BlockStatement(stmts=[ReturnStatement(return Identifier(str))])), MethodDecl(static PrimitiveType(string) repeat([Parameter(PrimitiveType(string) str), Parameter(PrimitiveType(int) times)]), BlockStatement(vars=[VariableDecl(PrimitiveType(string), [Variable(result = StringLiteral(\"\"))])], stmts=[ForStatement(for i := IntLiteral(1) to Identifier(times) do BlockStatement(stmts=[AssignmentStatement(IdLHS(result) := BinaryOp(Identifier(result), ^, Identifier(str)))])), ReturnStatement(return Identifier(result))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_038():
#     """Test multiple inheritance levels and super class method calls"""
#     source = """class Animal {
#         string name;
#         Animal(string name) {
#             this.name := name;
#         }
#         string speak() {
#             return "Animal speaks";
#         }
#     }
#     class Dog extends Animal {
#         int age;
#         Dog(string name; int age) {
#             Animal(name);
#             this.age := age;
#         }
#         string speak() {
#             return "Dog barks";
#         }
#     }"""
#     expected = "Program([ClassDecl(Animal, [AttributeDecl(PrimitiveType(string), [Attribute(name)]), ConstructorDecl(Animal([Parameter(PrimitiveType(string) name)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).name)) := Identifier(name))])), MethodDecl(PrimitiveType(string) speak([]), BlockStatement(stmts=[ReturnStatement(return StringLiteral(\"Animal speaks\"))]))]), ClassDecl(Dog, extends Animal, [AttributeDecl(PrimitiveType(int), [Attribute(age)]), ConstructorDecl(Dog([Parameter(PrimitiveType(string) name), Parameter(PrimitiveType(int) age)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(Animal)(Identifier(name)))), AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).age)) := Identifier(age))])), MethodDecl(PrimitiveType(string) speak([]), BlockStatement(stmts=[ReturnStatement(return StringLiteral(\"Dog barks\"))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_039():
#     """Test complex array initialization and nested array operations"""
#     source = """class ArrayUtils {
#         static int[3] merge(int[3] a; int[3] b) {
#             int[3] result;
#             for i := 0 to 2 do {
#                 result[i] := a[i] + b[i];
#             }
#             return result;
#         }
#         static void sort(int[5] & arr) {
#             for i := 0 to 3 do {
#                 for j := i + 1 to 4 do {
#                     if arr[i] > arr[j] then {
#                         int temp := arr[i];
#                         arr[i] := arr[j];
#                         arr[j] := temp;
#                     }
#                 }
#             }
#         }
#     }"""
#     expected = "Program([ClassDecl(ArrayUtils, [MethodDecl(static ArrayType(PrimitiveType(int)[3]) merge([Parameter(ArrayType(PrimitiveType(int)[3]) a), Parameter(ArrayType(PrimitiveType(int)[3]) b)]), BlockStatement(vars=[VariableDecl(ArrayType(PrimitiveType(int)[3]), [Variable(result)])], stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(2) do BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(result)[Identifier(i)])) := BinaryOp(PostfixExpression(Identifier(a)[Identifier(i)]), +, PostfixExpression(Identifier(b)[Identifier(i)])))])), ReturnStatement(return Identifier(result))])), MethodDecl(static PrimitiveType(void) sort([Parameter(ReferenceType(ArrayType(PrimitiveType(int)[5]) &) arr)]), BlockStatement(stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(3) do BlockStatement(stmts=[ForStatement(for j := BinaryOp(Identifier(i), +, IntLiteral(1)) to IntLiteral(4) do BlockStatement(stmts=[IfStatement(if BinaryOp(PostfixExpression(Identifier(arr)[Identifier(i)]), >, PostfixExpression(Identifier(arr)[Identifier(j)])) then BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(temp = PostfixExpression(Identifier(arr)[Identifier(i)]))])], stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[Identifier(i)])) := PostfixExpression(Identifier(arr)[Identifier(j)])), AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[Identifier(j)])) := Identifier(temp))]))]))]))]))])])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_040():
#     """Test multiple variable declarations with different types and initializations"""
#     source = """class TestClass {
#         static final float PI := 3.14159;
#         final boolean DEBUG := true;
#         void test() {
#             final int x := 1, y := 2, z := 3;
#             float a, b := 1.0, c := 2.0;
#             boolean flag1 := true, flag2;
#             string[2] messages := {"Hello", "World"};
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(static final PrimitiveType(float), [Attribute(PI = FloatLiteral(3.14159))]), AttributeDecl(final PrimitiveType(boolean), [Attribute(DEBUG = BoolLiteral(true))]), MethodDecl(PrimitiveType(void) test([]), BlockStatement(vars=[VariableDecl(final PrimitiveType(int), [Variable(x = IntLiteral(1)), Variable(y = IntLiteral(2)), Variable(z = IntLiteral(3))]), VariableDecl(PrimitiveType(float), [Variable(a), Variable(b = FloatLiteral(1.0)), Variable(c = FloatLiteral(2.0))]), VariableDecl(PrimitiveType(boolean), [Variable(flag1 = BoolLiteral(true)), Variable(flag2)]), VariableDecl(ArrayType(PrimitiveType(string)[2]), [Variable(messages = ArrayLiteral({StringLiteral(\"Hello\"), StringLiteral(\"World\")}))])], stmts=[]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_041():
#     """Test nested blocks and variable shadowing"""
#     source = """class TestClass {
#         void test() {
#             int x := 1;
#             {
#                 float x := 2.0;
#                 {
#                     string x := "3";
#                 }
#             }
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) test([]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(x = IntLiteral(1))])], stmts=[BlockStatement(vars=[VariableDecl(PrimitiveType(float), [Variable(x = FloatLiteral(2.0))])], stmts=[BlockStatement(vars=[VariableDecl(PrimitiveType(string), [Variable(x = StringLiteral(\"3\"))])], stmts=[])])]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_042():
#     """Test all logical operators and complex conditions"""
#     source = """class TestClass {
#         boolean test(boolean a; boolean b; boolean c) {
#             return !a && (b || !c) && !(a && b) || (a || b) && !c;
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(boolean) test([Parameter(PrimitiveType(boolean) a), Parameter(PrimitiveType(boolean) b), Parameter(PrimitiveType(boolean) c)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(BinaryOp(BinaryOp(UnaryOp(!, Identifier(a)), &&, BinaryOp(Identifier(b), ||, UnaryOp(!, Identifier(c)))), &&, UnaryOp(!, BinaryOp(Identifier(a), &&, Identifier(b)))), ||, BinaryOp(BinaryOp(Identifier(a), ||, Identifier(b)), &&, UnaryOp(!, Identifier(c)))))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_043():
#     """Test method overloading with different parameter types"""
#     source = """class Calculator {
#         int add(int a; int b) {
#             return a + b;
#         }
#         float add(float a; float b) {
#             return a + b;
#         }
#         string add(string a; string b) {
#             return a ^ b;
#         }
#     }"""
#     expected = "Program([ClassDecl(Calculator, [MethodDecl(PrimitiveType(int) add([Parameter(PrimitiveType(int) a), Parameter(PrimitiveType(int) b)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(Identifier(a), +, Identifier(b)))])), MethodDecl(PrimitiveType(float) add([Parameter(PrimitiveType(float) a), Parameter(PrimitiveType(float) b)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(Identifier(a), +, Identifier(b)))])), MethodDecl(PrimitiveType(string) add([Parameter(PrimitiveType(string) a), Parameter(PrimitiveType(string) b)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(Identifier(a), ^, Identifier(b)))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_044():
#     """Test complex class with all member types and modifiers"""
#     source = """class ComplexClass {
#         static final int CONSTANT := 100;
#         static float defaultValue := 0.0;
#         final string name;
#         boolean[10] flags;
        
#         ComplexClass() {
#             name := "default";
#         }
        
#         ComplexClass(ComplexClass other) {
#             name := other.name;
#             flags := other.flags;
#         }
        
#         static void initialize() {
#             defaultValue := 1.0;
#         }
        
#         void setFlag(int index; boolean value) {
#             flags[index] := value;
#         }
        
#         ~ComplexClass() {
#             flags[0] := false;
#         }
#     }"""
#     expected = "Program([ClassDecl(ComplexClass, [AttributeDecl(static final PrimitiveType(int), [Attribute(CONSTANT = IntLiteral(100))]), AttributeDecl(static PrimitiveType(float), [Attribute(defaultValue = FloatLiteral(0.0))]), AttributeDecl(final PrimitiveType(string), [Attribute(name)]), AttributeDecl(ArrayType(PrimitiveType(boolean)[10]), [Attribute(flags)]), ConstructorDecl(ComplexClass([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(name) := StringLiteral(\"default\"))])), ConstructorDecl(ComplexClass([Parameter(ClassType(ComplexClass) other)]), BlockStatement(stmts=[AssignmentStatement(IdLHS(name) := PostfixExpression(Identifier(other).name)), AssignmentStatement(IdLHS(flags) := PostfixExpression(Identifier(other).flags))])), MethodDecl(static PrimitiveType(void) initialize([]), BlockStatement(stmts=[AssignmentStatement(IdLHS(defaultValue) := FloatLiteral(1.0))])), MethodDecl(PrimitiveType(void) setFlag([Parameter(PrimitiveType(int) index), Parameter(PrimitiveType(boolean) value)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(flags)[Identifier(index)])) := Identifier(value))])), DestructorDecl(~ComplexClass(), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(flags)[IntLiteral(0)])) := BoolLiteral(false))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_045():
#     """Test all integer operators and precedence"""
#     source = """class MathUtils {
#         int calculate(int a; int b; int c) {
#             return (-a + b * c) \\ 2 % 3 - 4 * (5 + 6);
#         }
#     }"""
#     expected = "Program([ClassDecl(MathUtils, [MethodDecl(PrimitiveType(int) calculate([Parameter(PrimitiveType(int) a), Parameter(PrimitiveType(int) b), Parameter(PrimitiveType(int) c)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(BinaryOp(BinaryOp(BinaryOp(UnaryOp(-, Identifier(a)), +, BinaryOp(Identifier(b), *, Identifier(c))), \\, IntLiteral(2)), %, IntLiteral(3)), -, BinaryOp(IntLiteral(4), *, BinaryOp(IntLiteral(5), +, IntLiteral(6)))))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_046():
#     """Test nested array types with reference parameters"""
#     source = """class ArrayProcessor {
#         void processMatrix(int[2][3] & matrix) {
#             for i := 0 to 1 do {
#                 for j := 0 to 2 do {
#                     matrix[i][j] := matrix[i][j] * 2;
#                 }
#             }
#         }
#     }"""
#     expected = "Program([ClassDecl(ArrayProcessor, [MethodDecl(PrimitiveType(void) processMatrix([Parameter(ReferenceType(ArrayType(ArrayType(PrimitiveType(int)[2])[3]) &) matrix)]), BlockStatement(stmts=[ForStatement(for i := IntLiteral(0) to IntLiteral(1) do BlockStatement(stmts=[ForStatement(for j := IntLiteral(0) to IntLiteral(2) do BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(matrix)[Identifier(i)][Identifier(j)])) := BinaryOp(PostfixExpression(Identifier(matrix)[Identifier(i)][Identifier(j)]), *, IntLiteral(2)))]))]))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_047():
#     """Test complex object initialization and method chaining"""
#     source = """class ChainDemo {
#         ChainDemo setX(int x) {
#             return this;
#         }
#         ChainDemo setY(int y) {
#             return this;
#         }
#         static void demo() {
#             ChainDemo obj := new ChainDemo().setX(10).setY(20);
#         }
#     }"""
#     expected = "Program([ClassDecl(ChainDemo, [MethodDecl(ClassType(ChainDemo) setX([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[ReturnStatement(return ThisExpression(this))])), MethodDecl(ClassType(ChainDemo) setY([Parameter(PrimitiveType(int) y)]), BlockStatement(stmts=[ReturnStatement(return ThisExpression(this))])), MethodDecl(static PrimitiveType(void) demo([]), BlockStatement(vars=[VariableDecl(ClassType(ChainDemo), [Variable(obj = PostfixExpression(PostfixExpression(ObjectCreation(new ChainDemo()).setX(IntLiteral(10))).setY(IntLiteral(20))))])], stmts=[]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_048():
#     """Test complex class hierarchy with multiple inheritance levels"""
#     source = """class Shape {
#         string color;
#     }
#     class TwoDShape extends Shape {
#         float area() {
#             return 0.0;
#         }
#     }
#     class Circle extends TwoDShape {
#         static final float PI := 3.14;
#         float radius;
#         float area() {
#             return PI * radius * radius;
#         }
#     }"""
#     expected = "Program([ClassDecl(Shape, [AttributeDecl(PrimitiveType(string), [Attribute(color)])]), ClassDecl(TwoDShape, extends Shape, [MethodDecl(PrimitiveType(float) area([]), BlockStatement(stmts=[ReturnStatement(return FloatLiteral(0.0))]))]), ClassDecl(Circle, extends TwoDShape, [AttributeDecl(static final PrimitiveType(float), [Attribute(PI = FloatLiteral(3.14))]), AttributeDecl(PrimitiveType(float), [Attribute(radius)]), MethodDecl(PrimitiveType(float) area([]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(BinaryOp(Identifier(PI), *, Identifier(radius)), *, Identifier(radius)))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_049():
#     """Test all string operations and escape sequences"""
#     source = """class StringTest {
#         string testEscapes() {
#             string s1 := "Hello\\n";
#             string s2 := "World\\t";
#             string s3 := "Quote: \\"";
#             string s4 := "Backslash: \\\\";
#             return s1 ^ s2 ^ s3 ^ s4;
#         }
#     }"""
#     expected = "Program([ClassDecl(StringTest, [MethodDecl(PrimitiveType(string) testEscapes([]), BlockStatement(vars=[VariableDecl(PrimitiveType(string), [Variable(s1 = StringLiteral(\"Hello\\n\"))]), VariableDecl(PrimitiveType(string), [Variable(s2 = StringLiteral(\"World\\t\"))]), VariableDecl(PrimitiveType(string), [Variable(s3 = StringLiteral(\"Quote: \\\"\"))]), VariableDecl(PrimitiveType(string), [Variable(s4 = StringLiteral(\"Backslash: \\\\\"))])], stmts=[ReturnStatement(return BinaryOp(BinaryOp(BinaryOp(Identifier(s1), ^, Identifier(s2)), ^, Identifier(s3)), ^, Identifier(s4)))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_050():
#     """Test all assignment forms and compound expressions"""
#     source = """class AssignmentTest {
#         void test(Shape s) {
#             int x;
#             int[3] arr;
#             x := 1 + 2 * 3;
#             arr[0] := x + 1;
#             s.value := arr[0] * 2;
#             this.field := s.value;
#         }
#     }"""
#     expected = "Program([ClassDecl(AssignmentTest, [MethodDecl(PrimitiveType(void) test([Parameter(ClassType(Shape) s)]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(x)]), VariableDecl(ArrayType(PrimitiveType(int)[3]), [Variable(arr)])], stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3)))), AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[IntLiteral(0)])) := BinaryOp(Identifier(x), +, IntLiteral(1))), AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(s).value)) := BinaryOp(PostfixExpression(Identifier(arr)[IntLiteral(0)]), *, IntLiteral(2))), AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).field)) := PostfixExpression(Identifier(s).value))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_051():
#     """Test basic if-then statement without else"""
#     source = """class TestClass {
#         void test(int x) {
#             if x > 0 then {
#                 x := x + 1;
#             }
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) test([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(x), +, IntLiteral(1)))]))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_052():
#     """Test if-then-else with complex conditions"""
#     source = """class TestClass {
#         void test(int x; int y) {
#             if (x > 0) then {
#                 x := x + 1;
#             } else {
#                 y := y - 1;
#             }
#         }
#     }"""
#     program = Program([ClassDecl("TestClass", None, [
#         MethodDecl(False, PrimitiveType("void"), "test", [Parameter(PrimitiveType("int"), "x"), Parameter(PrimitiveType("int"), "y")], BlockStatement(
#             var_decls=[],
#             statements=[
#                 IfStatement(ParenthesizedExpression(BinaryOp(Identifier("x"), ">", IntLiteral(0))), BlockStatement(
#                     var_decls=[],
#                     statements=[AssignmentStatement(IdLHS("x"), BinaryOp(Identifier("x"), "+", IntLiteral(1)))]
#                 ), BlockStatement(
#                     var_decls=[],
#                     statements=[AssignmentStatement(IdLHS("y"), BinaryOp(Identifier("y"), "-", IntLiteral(1)))]
#                 ))
#             ]
#         ))
#     ])])
#     expected = str(program)
#     assert str(ASTGenerator(source).generate()) == expected

# def test_053():
#     """Test nested if-then-else with else matching nearest if"""
#     source = """class TestClass {
#         void test(int x) {
#             if x > 0 then
#                 if x < 10 then {
#                     x := 1;
#                 } else {
#                     x := 2;
#                 }
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) test([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then IfStatement(if BinaryOp(Identifier(x), <, IntLiteral(10)) then BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := IntLiteral(1))]), else BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := IntLiteral(2))])))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_054():
#     """Test cascading if-then-else statements"""
#     source = """class TestClass {
#         int test(int x) {
#             if x < 0 then {
#                 return -1;
#             } else if x == 0 then {
#                 return 0;
#             } else if x > 10 then {
#                 return 2;
#             } else {
#                 return 1;
#             }
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(int) test([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), <, IntLiteral(0)) then BlockStatement(stmts=[ReturnStatement(return UnaryOp(-, IntLiteral(1)))]), else IfStatement(if BinaryOp(Identifier(x), ==, IntLiteral(0)) then BlockStatement(stmts=[ReturnStatement(return IntLiteral(0))]), else IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(10)) then BlockStatement(stmts=[ReturnStatement(return IntLiteral(2))]), else BlockStatement(stmts=[ReturnStatement(return IntLiteral(1))]))))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_055():
#     """Test if-then-else with complex nested structure"""
#     source = """class TestClass {
#         void test(int x; int y) {
#             if x > 0 then {
#                 if y > 0 then {
#                     x := x + y;
#                 } else {
#                     x := x - y;
#                 }
#             } else {
#                 if y > 0 then {
#                     x := y - x;
#                 } else {
#                     x := -x - y;
#                 }
#             }
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) test([Parameter(PrimitiveType(int) x), Parameter(PrimitiveType(int) y)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(y), >, IntLiteral(0)) then BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(x), +, Identifier(y)))]), else BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(x), -, Identifier(y)))]))]), else BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(y), >, IntLiteral(0)) then BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(y), -, Identifier(x)))]), else BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(UnaryOp(-, Identifier(x)), -, Identifier(y)))]))]))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_056():
#     """Test dangling else ambiguity resolution"""
#     source = """class TestClass {
#         void test(int x; int y; int z) {
#             if x > 0 then
#                 if y > 0 then
#                     if z > 0 then {
#                         x := 1;
#                     } else {
#                         x := 2;
#                     }
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) test([Parameter(PrimitiveType(int) x), Parameter(PrimitiveType(int) y), Parameter(PrimitiveType(int) z)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then IfStatement(if BinaryOp(Identifier(y), >, IntLiteral(0)) then IfStatement(if BinaryOp(Identifier(z), >, IntLiteral(0)) then BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := IntLiteral(1))]), else BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := IntLiteral(2))]))))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_057():
#     """Test mixed matched and unmatched if statements"""
#     source = """class TestClass {
#         void test(int x; int y) {
#             if x > 0 then
#                 if y > 0 then {
#                     x := 1;
#                 } else {
#                     x := 2;
#                 }
#             else {
#                 x := 3;
#             }
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) test([Parameter(PrimitiveType(int) x), Parameter(PrimitiveType(int) y)]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then IfStatement(if BinaryOp(Identifier(y), >, IntLiteral(0)) then BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := IntLiteral(1))]), else BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := IntLiteral(2))])), else BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := IntLiteral(3))]))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_058():
#     """Test if-then with block statements and complex expressions"""
#     source = """class TestClass {
#         void test(int x; int y; int z) {
#             if !(x > y + z) then {
#                 {
#                     x := x + 1;
#                 }
#                 {
#                     y := y - 1;
#                 }
#             }
#         }
#     }"""
#     program = Program([ClassDecl("TestClass", None, [
#         MethodDecl(False, PrimitiveType("void"), "test", [Parameter(PrimitiveType("int"), "x"), Parameter(PrimitiveType("int"), "y"), Parameter(PrimitiveType("int"), "z")], BlockStatement(
#             var_decls=[],
#             statements=[IfStatement(UnaryOp("!", ParenthesizedExpression(BinaryOp(Identifier("x"), ">", BinaryOp(Identifier("y"), "+", Identifier("z"))))), BlockStatement(
#                 var_decls=[],
#                 statements=[
#                     BlockStatement(
#                         var_decls=[],
#                         statements=[AssignmentStatement(IdLHS("x"), BinaryOp(Identifier("x"), "+", IntLiteral(1)))]
#                     ),
#                     BlockStatement(
#                         var_decls=[],
#                         statements=[AssignmentStatement(IdLHS("y"), BinaryOp(Identifier("y"), "-", IntLiteral(1)))]
#                     )
#                 ]
#             ))]
#         ))
#     ])])
#     expected = str(program)
#     assert str(ASTGenerator(source).generate()) == expected

# def test_059():
#     """Test if-then with method calls and complex conditions"""
#     source = """class TestClass {
#         boolean isValid(int x) {
#             return x > 0;
#         }
#         void test(int x) {
#             if this.isValid(x + 1) && this.isValid(x - 1) then {
#                 x := x + 1;
#             }
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(boolean) isValid([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[ReturnStatement(return BinaryOp(Identifier(x), >, IntLiteral(0)))])), MethodDecl(PrimitiveType(void) test([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[IfStatement(if BinaryOp(PostfixExpression(ThisExpression(this).isValid(BinaryOp(Identifier(x), +, IntLiteral(1)))), &&, PostfixExpression(ThisExpression(this).isValid(BinaryOp(Identifier(x), -, IntLiteral(1))))) then BlockStatement(stmts=[AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(x), +, IntLiteral(1)))]))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_060():
#     """Test if-then-else with array access and member access"""
#     source = """class TestClass {
#         int[5] arr;
#         Shape shape;
#         void test(int i) {
#             if arr[i] == shape.value then {
#                 arr[i] := shape.getValue();
#             } else {
#                 shape.setValue(arr[i]);
#             }
#         }
#     }"""
#     program = Program([ClassDecl("TestClass", None, [
#         AttributeDecl(False, False, ArrayType(PrimitiveType("int"), 5), [Attribute("arr")]),
#         AttributeDecl(False, False, ClassType("Shape"), [Attribute("shape")]),
#         MethodDecl(False, PrimitiveType("void"), "test", [Parameter(PrimitiveType("int"), "i")], BlockStatement(
#             var_decls=[],
#             statements=[IfStatement(BinaryOp(PostfixExpression(Identifier("arr"), [ArrayAccess(Identifier("i"))]), "==", PostfixExpression(Identifier("shape"), [MemberAccess("value")])), BlockStatement(
#                 var_decls=[],
#                 statements=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier("arr"), [ArrayAccess(Identifier("i"))])), PostfixExpression(Identifier("shape"), [MethodCall("getValue", [])]))],
#             ), BlockStatement(
#                 var_decls=[],
#                 statements=[MethodInvocationStatement(PostfixExpression(Identifier("shape"), [MethodCall("setValue", [PostfixExpression(Identifier("arr"), [ArrayAccess(Identifier("i"))])])]))]
#             ))]
#         ))
#     ])])
#     expected = str(program)
#     assert str(ASTGenerator(source).generate()) == expected

# def test_061():
#     """Test complex postfix expressions with method calls and array access"""
#     source = """class TestClass {
#         Shape[3] shapes;
#         void test() {
#             shapes[0].setColor("red").move(1, 2).scale(2.0);
#             shapes[1].getPoints()[0].x := 10;
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ArrayType(ClassType(Shape)[3]), [Attribute(shapes)]), MethodDecl(PrimitiveType(void) test([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(PostfixExpression(PostfixExpression(PostfixExpression(Identifier(shapes)[IntLiteral(0)]).setColor(StringLiteral(\"red\"))).move(IntLiteral(1), IntLiteral(2))).scale(FloatLiteral(2.0)))), AssignmentStatement(PostfixLHS(PostfixExpression(PostfixExpression(PostfixExpression(Identifier(shapes)[IntLiteral(1)]).getPoints())[IntLiteral(0)].x)) := IntLiteral(10))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_062():
#     """Test nested postfix expressions with parenthesized subexpressions"""
#     source = """class TestClass {
#         Shape[3] shapes;
#         void test() {
#             (shapes[0].getNext()).setValue((1 + 2) * 3);
#             (shapes[1].getPrev().getCurrent()).x := 5;
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ArrayType(ClassType(Shape)[3]), [Attribute(shapes)]), MethodDecl(PrimitiveType(void) test([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(ParenthesizedExpression(PostfixExpression(Identifier(shapes)[IntLiteral(0)].getNext())).setValue(BinaryOp(ParenthesizedExpression(BinaryOp(IntLiteral(1), +, IntLiteral(2))), *, IntLiteral(3))))), AssignmentStatement(PostfixLHS(PostfixExpression(ParenthesizedExpression(PostfixExpression(PostfixExpression(Identifier(shapes)[IntLiteral(1)].getPrev()).getCurrent())).x)) := IntLiteral(5))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_063():
#     """Test method calls with complex argument expressions"""
#     source = """class TestClass {
#         void processShape(Shape s) {
#             s.setValues(
#                 this.getValue() + 1,
#                 s.getWidth() * 2,
#                 s.getNext().getHeight()
#             );
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) processShape([Parameter(ClassType(Shape) s)]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(s).setValues(BinaryOp(PostfixExpression(ThisExpression(this).getValue()), +, IntLiteral(1)), BinaryOp(PostfixExpression(Identifier(s).getWidth()), *, IntLiteral(2)), PostfixExpression(PostfixExpression(Identifier(s).getNext()).getHeight()))))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_064():
#     """Test array access with complex index expressions"""
#     source = """class TestClass {
#         int[10][10] matrix;
#         int getValue(int i; int j) {
#             return matrix[i + 1][matrix[i][j] + 2];
#         }
#         void setValue(int i; int j; int val) {
#             matrix[matrix[i][j]][matrix[j][i]] := val;
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ArrayType(ArrayType(PrimitiveType(int)[10])[10]), [Attribute(matrix)]), MethodDecl(PrimitiveType(int) getValue([Parameter(PrimitiveType(int) i), Parameter(PrimitiveType(int) j)]), BlockStatement(stmts=[ReturnStatement(return PostfixExpression(Identifier(matrix)[BinaryOp(Identifier(i), +, IntLiteral(1))][BinaryOp(PostfixExpression(Identifier(matrix)[Identifier(i)][Identifier(j)]), +, IntLiteral(2))]))])), MethodDecl(PrimitiveType(void) setValue([Parameter(PrimitiveType(int) i), Parameter(PrimitiveType(int) j), Parameter(PrimitiveType(int) val)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(matrix)[PostfixExpression(Identifier(matrix)[Identifier(i)][Identifier(j)])][PostfixExpression(Identifier(matrix)[Identifier(j)][Identifier(i)])])) := Identifier(val))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_065():
#     """Test member access with this expression and chaining"""
#     source = """class TestClass {
#         Shape current;
#         Shape next;
#         void test() {
#             this.current.next := this.next;
#             this.next.current := this.current;
#             this.current.next.current.next := this.next.current;
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ClassType(Shape), [Attribute(current)]), AttributeDecl(ClassType(Shape), [Attribute(next)]), MethodDecl(PrimitiveType(void) test([]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).current.next)) := PostfixExpression(ThisExpression(this).next)), AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).next.current)) := PostfixExpression(ThisExpression(this).current)), AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).current.next.current.next)) := PostfixExpression(ThisExpression(this).next.current))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_066():
#     """Test complex PostfixLHS assignments"""
#     source = """class TestClass {
#         Shape[5] shapes;
#         int[5][5] matrix;
#         void test() {
#             shapes[0].getNext().value := 1;
#             matrix[shapes[1].getIndex()][shapes[2].getIndex()] := 2;
#             (shapes[3].getCurrent()).value := (shapes[4].getValue());
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ArrayType(ClassType(Shape)[5]), [Attribute(shapes)]), AttributeDecl(ArrayType(ArrayType(PrimitiveType(int)[5])[5]), [Attribute(matrix)]), MethodDecl(PrimitiveType(void) test([]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(PostfixExpression(Identifier(shapes)[IntLiteral(0)].getNext()).value)) := IntLiteral(1)), AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(matrix)[PostfixExpression(Identifier(shapes)[IntLiteral(1)].getIndex())][PostfixExpression(Identifier(shapes)[IntLiteral(2)].getIndex())])) := IntLiteral(2)), AssignmentStatement(PostfixLHS(PostfixExpression(ParenthesizedExpression(PostfixExpression(Identifier(shapes)[IntLiteral(3)].getCurrent())).value)) := PostfixExpression(Identifier(shapes)[IntLiteral(4)].getValue()))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_067():
#     """Test postfix expressions with multiple nested method calls"""
#     source = """class TestClass {
#         Shape root;
#         void test() {
#             root.getLeft().getRight().getValue();
#             root.findNode("key").getData().process();
#             root.getParent().getLeft().getRight().setValue(10);
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ClassType(Shape), [Attribute(root)]), MethodDecl(PrimitiveType(void) test([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(PostfixExpression(PostfixExpression(Identifier(root).getLeft()).getRight()).getValue())), MethodInvocationStatement(PostfixExpression(PostfixExpression(PostfixExpression(Identifier(root).findNode(StringLiteral(\"key\"))).getData()).process())), MethodInvocationStatement(PostfixExpression(PostfixExpression(PostfixExpression(PostfixExpression(Identifier(root).getParent()).getLeft()).getRight()).setValue(IntLiteral(10))))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_068():
#     """Test mixed array and method access in PostfixExpression"""
#     source = """class TestClass {
#         Shape[][] grid;
#         void test() {
#             grid[0][0].move(1, 1).draw();
#             grid[1][1].getNeighbors()[0].update();
#             grid[this.getRow()][this.getCol()].process();
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ArrayType(ArrayType(ClassType(Shape))), [Attribute(grid)]), MethodDecl(PrimitiveType(void) test([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(PostfixExpression(PostfixExpression(Identifier(grid)[IntLiteral(0)][IntLiteral(0)].move(IntLiteral(1), IntLiteral(1))).draw())), MethodInvocationStatement(PostfixExpression(PostfixExpression(PostfixExpression(Identifier(grid)[IntLiteral(1)][IntLiteral(1)].getNeighbors())[IntLiteral(0)].update())), MethodInvocationStatement(PostfixExpression(PostfixExpression(Identifier(grid)[PostfixExpression(ThisExpression(this).getRow())][PostfixExpression(ThisExpression(this).getCol())].process()))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_069():
#     """Test parenthesized expressions with complex method chains"""
#     source = """class TestClass {
#         Shape shape;
#         void test() {
#             (shape.getNext()).setX((shape.getX() + 1) * 2);
#             ((shape.getParent()).getChild()).setValue(
#                 (shape.getValue() + (shape.getNext()).getValue()) / 2
#             );
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ClassType(Shape), [Attribute(shape)]), MethodDecl(PrimitiveType(void) test([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(ParenthesizedExpression(PostfixExpression(Identifier(shape).getNext())).setX(BinaryOp(ParenthesizedExpression(BinaryOp(PostfixExpression(Identifier(shape).getX()), +, IntLiteral(1))), *, IntLiteral(2))))), MethodInvocationStatement(PostfixExpression(ParenthesizedExpression(PostfixExpression(ParenthesizedExpression(PostfixExpression(Identifier(shape).getParent())).getChild())).setValue(BinaryOp(BinaryOp(PostfixExpression(Identifier(shape).getValue()), +, PostfixExpression(ParenthesizedExpression(PostfixExpression(Identifier(shape).getNext())).getValue())), /, IntLiteral(2)))))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected

# def test_070():
#     """Test complex expressions mixing all postfix operators"""
#     source = """class TestClass {
#         Shape[5] shapes;
#         Node root;
#         void test() {
#             shapes[root.getIndex()].getData()[0].process();
#             (root.getLeft().getData() + root.getRight().getData())[0] := 
#                 shapes[0].getValues()[root.getHeight()];
#             root.getChildren()[shapes[0].getIndex()].setNext(
#                 shapes[root.getValue()].getCurrent()
#             );
#         }
#     }"""
#     expected = "Program([ClassDecl(TestClass, [AttributeDecl(ArrayType(ClassType(Shape)[5]), [Attribute(shapes)]), AttributeDecl(ClassType(Node), [Attribute(root)]), MethodDecl(PrimitiveType(void) test([]), BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(PostfixExpression(PostfixExpression(Identifier(shapes)[PostfixExpression(Identifier(root).getIndex())].getData())[IntLiteral(0)].process())), AssignmentStatement(PostfixLHS(PostfixExpression(ParenthesizedExpression(BinaryOp(PostfixExpression(PostfixExpression(Identifier(root).getLeft()).getData()), +, PostfixExpression(PostfixExpression(Identifier(root).getRight()).getData())))[IntLiteral(0)])) := PostfixExpression(PostfixExpression(Identifier(shapes)[IntLiteral(0)].getValues())[PostfixExpression(Identifier(root).getHeight())])), MethodInvocationStatement(PostfixExpression(PostfixExpression(Identifier(root).getChildren())[PostfixExpression(Identifier(shapes)[IntLiteral(0)].getIndex())].setNext(PostfixExpression(Identifier(shapes)[PostfixExpression(Identifier(root).getValue())].getCurrent()))))]))])])"
#     assert str(ASTGenerator(source).generate()) == expected
