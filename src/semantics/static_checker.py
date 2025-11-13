"""
Static Semantic Checker for OPLang Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the OPLang object-oriented programming language. It performs type checking,
scope management, inheritance validation, and detects all semantic errors as 
specified in the OPLang language specification.
"""

from copy import deepcopy
from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ClassDecl, AttributeDecl, Attribute, MethodDecl,
    ConstructorDecl, DestructorDecl, Parameter, VariableDecl, Variable,
    AssignmentStatement, IfStatement, ForStatement, BreakStatement,
    ContinueStatement, ReturnStatement, MethodInvocationStatement,
    BlockStatement, PrimitiveType, ArrayType, ClassType, ReferenceType,
    IdLHS, PostfixLHS, BinaryOp, UnaryOp, PostfixExpression, PostfixOp,
    MethodCall, MemberAccess, ArrayAccess, ObjectCreation, Identifier,
    ThisExpression, ParenthesizedExpression, IntLiteral, FloatLiteral,
    BoolLiteral, StringLiteral, ArrayLiteral, NilLiteral, Type
)
from .static_error import (
    StaticError, Redeclared, UndeclaredIdentifier, UndeclaredClass,
    UndeclaredAttribute, UndeclaredMethod, CannotAssignToConstant,
    TypeMismatchInStatement, TypeMismatchInExpression, TypeMismatchInConstant,
    MustInLoop, IllegalConstantExpression, IllegalArrayLiteral,
    IllegalMemberAccess, NoEntryPoint
)


class Symb:
    def __repr__(self):
        return "Symb"

class ClassSymb(Symb):
    def __init__(self, name, superclass, members):
        self.name = name
        self.superclass = superclass
        self.members = members
    
    def __repr__(self):
        members = "; ".join(str(m) for m in self.members)
        return f"ClassSymb({self.name} extends {self.superclass}, members: {members})"

class AttributeSymb(Symb):
    def __init__(self, is_final, is_static, type, name, is_super=False):
        self.is_final = is_final
        self.is_static = is_static
        self.type = type.set_final_if(is_final)
        self.name = name
        self.is_super = is_super

    def __repr__(self):
        final = "final " if self.is_final else ""
        static = "static " if self.is_static else ""
        return f"AttributeSymb({final}{static}{self.type} {self.name})"

class ParameterSymb(Symb):
    def __init__(self, type, name):
        self.type = type
        self.name = name
    
    def __repr__(self):
        return f"ParameterSymb({self.type} {self.name})"


class MethodSymb(Symb):
    def __init__(self, is_static, return_type, name, param_types, is_super=False):
        self.is_static = is_static
        self.return_type = return_type
        self.name = name
        self.param_types = param_types
        self.is_super = is_super
    
    def __repr__(self):
        static = "static " if self.is_static else ""
        params = ", ".join(self.param_types)
        return f"MethodSymb({static}{self.return_type} {self.name}({params}))"


class ConstructorSymb(Symb):
    def __init__(self, name, param_types, is_super=False):
        self.name = name
        self.param_types = param_types
        self.is_super = is_super
    
    def __repr__(self):
        params = ", ".join(self.param_types)
        return f"ConstructorSymb({self.name}({params}))"


class DestructorSymb(Symb):
    def __init__(self, name, is_super=False):
        self.name = name
        self.is_super = is_super
    
    def __repr__(self):
        return f"DestructorSymb(~{self.name}())"


class VariableSymb(Symb):
    def __init__(self, is_final, type, name):
        self.is_final = is_final
        self.type = type.set_final_if(is_final)
        self.name = name
    
    def __repr__(self):
        final = "final " if self.is_final else ""
        return f"VariableSymb({final}{self.type} {self.name})"


class ForSignal(Symb):
    def __init__(self):
        self.name = "!LOOP"
    
    def __repr__(self):
        return "ForSignal()"

class T:
    def __init__(self, is_final=False):
        self.is_final = is_final
        self.type_name = "general"
    
    def set_final_if(self, condition: bool):
        self.is_final = condition
        return self
    
    def __repr__(self):
        final = "final " if self.is_final else ""
        return f"{final}{self.type_name}"

class Tint(T):
    def __init__(self, is_final=False):
        super().__init__(is_final)
        self.type_name = "int"

class Tfloat(T):
    def __init__(self, is_final=False):
        super().__init__(is_final)
        self.type_name = "float"

class Tboolean(T):
    def __init__(self, is_final=False):
        super().__init__(is_final)
        self.type_name = "boolean"

class Tstring(T):
    def __init__(self, is_final=False):
        super().__init__(is_final)
        self.type_name = "string"

class Tvoid(T):
    def __init__(self):
        super().__init__(is_final=False)
        self.type_name = "void"

class Tclass(T):
    def __init__(self, name, superclass=None, symb=None):
        super().__init__(is_final=False)
        self.name = self.type_name = name
        self.superclass = superclass
        self.symb = symb

class Treference(T):
    def __init__(self, referenced_type: T):
        super().__init__(is_final=False)
        self.referenced_type = referenced_type
        self.type_name = f"{referenced_type}&"

class Tarray(T):
    def __init__(self, element_type: Optional[T], size: int):
        super().__init__(is_final=False)
        self.element_type = element_type
        self.size = size
        self.type_name = f"{element_type}[{size}]"

class Tnil(T):
    def __init__(self):
        super().__init__(is_final=False)
        self.type_name = "nil"


class Postfix:
    pass

class ArrayPostfix(Postfix):
    pass

class MemberPostfix(Postfix):
    def __init__(self, name: str):
        self.name = name

class MethodPostfix(Postfix):
    def __init__(self, name: str, arg_types: List[T]):
        self.name = name
        self.arg_types = arg_types


def env_contains(node: Union[ASTNode, str], env: List[List[Any]]):
    if not isinstance(node, str):
        node = node.name
    for scope in env:
        for entity in scope:
            entity = entity if isinstance(entity, str) else entity.name
            if entity == node:
                return True
    return False

def scope_contains(node: Union[ASTNode, str], scope: List[Any]):
    if not isinstance(node, str):
        node = node.name
    
    for entity in scope:
        entity = entity if isinstance(entity, str) else entity.name
        if entity == node:
            return True
    return False


def get_class_symb(class_name: str, class_scope: List[Any]):
    found_class = next((symb for symb in class_scope if symb.name == class_name), None)
    return found_class

def get_class_attribute(class_symb: ClassSymb, attr_name: str):
    found_attr = next((m for m in class_symb.members if m.name == attr_name), None)
    return found_attr

def get_symb_from_scope(name: str, scope: List[Any]):
    found_symb = next((s for s in scope if s.name == name), None)
    return found_symb

def get_symb_by_id(name: str, env: List[List[Any]]):
    found_symb = next((symb for scope in env for symb in scope if symb.name == name), None)
    return found_symb

def get_for_signal(env: List[List[Any]]):
    search_env = env[:-2]
    found_signal = next((symb for scope in search_env for symb in scope if symb.name == "!LOOP"), None)
    return found_signal

def can_coerce_type(from_type: T, to_type: T):
    # Class coercion
    if type(from_type) is Tclass and type(to_type) is Tclass:
        if from_type.name == to_type.name:
            return True
        if from_type.superclass == to_type.name:
            return True
        return False

    # Numeric coercion
    if type(from_type) is Tint and type(to_type) is Tfloat:
        return True
    
    # Array equality (not coercion)
    if type(from_type) is Tarray and type(from_type) is Tarray:
        if type(from_type.element_type) is type(to_type.element_type) and from_type.size == to_type.size:
            return True
    
    # Fall through case
    def is_non_coercible(target_type):
        return type(target_type) in [Tvoid, Tnil, Tarray, Treference]
    
    if is_non_coercible(from_type) or is_non_coercible(to_type):
        return False
    
    return type(from_type) is type(to_type)


def can_coerce_args(arg_types, param_types):
    if len(arg_types) != len(param_types):
        return False
    return all(can_coerce_type(arg, param) for arg, param in zip(arg_types, param_types))


class StaticChecker(ASTVisitor):
    """
    Stateless static semantic checker for OPLang using visitor pattern.
    
    Checks for all 10 error types specified in OPLang semantic constraints:
    1. Redeclared - Variables, constants, attributes, classes, methods, parameters
    2. Undeclared - Identifiers, classes, attributes, methods  
    3. CannotAssignToConstant - Assignment to final variables/attributes
    4. TypeMismatchInStatement - Type incompatibilities in statements
    5. TypeMismatchInExpression - Type incompatibilities in expressions
    6. TypeMismatchInConstant - Type incompatibilities in constant declarations
    7. MustInLoop - Break/continue outside loop contexts
    8. IllegalConstantExpression - Invalid expressions in constant initialization
    9. IllegalArrayLiteral - Inconsistent types in array literals
    10. IllegalMemberAccess - Improper access to static/instance members

    Also checks for valid entry point: static void main() with no parameters.
    """
    
    processing_class = None     # Current class being processed     (ClassSymb)
    processing_method = None    # Current method being processed    (MethodSymb)
    
    # Entry point
    
    def check_program(self, node: "Program", env=[[]]):
        self.visit_program(node, env)
    
    
    # Program and class declarations
    
    def visit_program(self, node: "Program", env=[[]]):
        return reduce(
            lambda global_env, class_decl: self.visit(class_decl, global_env),
            node.class_decls,
            env,
        )


    def visit_class_decl(self, node: "ClassDecl", env: List[List[Any]]):
        if env_contains(node.name, env):
            raise Redeclared("Class", node.name)
        
        superclass_symb = get_class_symb(node.superclass, env[-1]) if node.superclass else None
        if node.superclass and not superclass_symb:
            raise UndeclaredClass(node.superclass)
        
        # Resolve superclass members
        def copy_and_label_super_member(member):
            member = deepcopy(member)
            member.is_super = True
            return member
        class_scope = deepcopy(superclass_symb.members) if superclass_symb else []
        class_scope = list(map(copy_and_label_super_member, class_scope))
        
        self.processing_class = ClassSymb(node.name, node.superclass, class_scope)
        
        def process_class_member(class_env, member):
            class_env = self.visit(member, class_env)
            self.processing_class.members = class_env[0]
            return class_env
        
        class_env = reduce(process_class_member, node.members, [class_scope] + env)
        
        return [env[0] + [self.processing_class], *env[1:]]


    # Attribute declarations
    
    def visit_attribute_decl(self, node: "AttributeDecl", env: List[List[Any]]):
        def check_attr_redeclared(class_env, attr):
            name, init_type = self.visit(attr, class_env)
            attr_type = self.visit(node.attr_type, env)
            
            overlap_attr = get_symb_from_scope(name, class_env[0])
            if overlap_attr and not overlap_attr.is_super:
                raise Redeclared("Constant" if node.is_final else "Attribute", name)
            
            # Fill in the element type if array type is returned
            if type(attr_type) is Tarray and type(init_type) is Tarray and not init_type.element_type:
                init_type.element_type = attr_type.element_type
            
            # Non-constant attribute declaration case is not specified for type checking
            # Constant attribute declaration case
            if node.is_final:
                if not init_type:
                    raise IllegalConstantExpression(NilLiteral())
                
                # Initialization is not statically evaluable
                if not init_type.is_final:
                    raise IllegalConstantExpression(attr.init_value)
                
                # Initialization doesn't match types (under coercion rules)
                if not can_coerce_type(init_type, attr_type):
                    raise TypeMismatchInConstant(node)

            attr_symb = AttributeSymb(node.is_final, node.is_static, attr_type, name)
            class_scope = [attr_symb] + class_env[0]
            return [class_scope, *class_env[1:]]

        class_env = reduce(check_attr_redeclared, node.attributes, env)
        return class_env


    def visit_attribute(self, node: "Attribute", env: List[List[Any]]):
        init_type = self.visit(node.init_value, env) if node.init_value else None
        return node.name, init_type

    # Method declarations
    
    def visit_method_decl(self, node: "MethodDecl", env: List[List[Any]]):
        overlap_method = get_symb_from_scope(node.name, env[0])
        if overlap_method and not overlap_method.is_super:
            raise Redeclared("Method", node.name)
        
        # Initialize method scope
        def check_param_redeclared(method_env, param):
            param_symb = self.visit(param, method_env)
            if scope_contains(param_symb.name, method_env[0]):
                raise Redeclared("Parameter", param_symb.name)
            return [method_env[0] + [param_symb], *method_env[1:]]
        
        method_env = reduce(check_param_redeclared, node.params, [[]] + env)
        
        method_symb = MethodSymb(
            node.is_static, self.visit(node.return_type, env), node.name, 
            [self.visit(param.param_type, env) for param in node.params],
        )
        self.processing_method = method_symb
        
        # Check the body
        self.visit(node.body, method_env)
        
        class_env = [[method_symb] + env[0], *env[1:]]
        return class_env


    def visit_constructor_decl(self, node: "ConstructorDecl", env: List[List[Any]]):
        overlap_method = get_symb_from_scope(node.name, env[0])
        if overlap_method and not overlap_method.is_super:
            raise Redeclared("Method", node.name)
        
        # Initialize constructor scope
        def check_param_redeclared(constructor_env, param):
            param_symb = self.visit(param, constructor_env)
            if scope_contains(param.name, constructor_env[0]):
                raise Redeclared("Parameter", param.name)
            return [constructor_env[0] + [param_symb], *constructor_env[1:]]

        constructor_env = reduce(check_param_redeclared, node.params, [[]] + env)
        
        # Check the body
        self.visit(node.body, constructor_env)
        
        constructor_symb = ConstructorSymb(
            node.name,
            list(map(lambda p: self.visit(p.param_type, env), node.params)),
        )
        return [[constructor_symb] + env[0], *env[1:]]


    def visit_destructor_decl(self, node: "DestructorDecl", env: List[List[Any]]):
        name = f"~{node.name}"
        overlap_method = get_symb_from_scope(name, env[0])
        if overlap_method and not overlap_method.is_super:
            raise Redeclared("Method", name)
        
        # Initialize destructor scope and check the body
        destructor_env = [[]] + env
        self.visit(node.body, destructor_env)
        
        destructor_symb = DestructorSymb(name)
        return [[destructor_symb] + env[0], *env[1:]]


    def visit_parameter(self, node: "Parameter", env: List[List[Any]]):
        param_type = self.visit(node.param_type, env)
        return ParameterSymb(param_type, node.name)

    # Type system

    def visit_primitive_type(self, node: "PrimitiveType", env: List[List[Any]]):
        prim_map = {"int": Tint(), "float": Tfloat(), "boolean": Tboolean(), "string": Tstring(), "void": Tvoid(), "nil": Tnil()}
        return prim_map[node.type_name]


    def visit_array_type(self, node: "ArrayType", env: List[List[Any]]):
        element_type = self.visit(node.element_type, env)
        return Tarray(element_type, node.size)


    def visit_class_type(self, node: "ClassType", env: List[List[Any]]):
        target_class = get_class_symb(node.class_name, env[-1])
        if not target_class:
            raise UndeclaredClass(node.class_name)
        return Tclass(target_class.name, target_class.superclass)


    def visit_reference_type(self, node: "ReferenceType", env: List[List[Any]]):
        referenced_type = self.visit(node.referenced_type, env)
        return Treference(referenced_type)

    # Statements

    def visit_block_statement(self, node: "BlockStatement", env: List[List[Any]]):
        block_env = reduce(
            lambda block_env, var_decl: self.visit(var_decl, block_env),
            node.var_decls,
            env,
        )
        for stmt in node.statements:
            stmt_env = [[]] + block_env if type(stmt) is BlockStatement else block_env
            self.visit(stmt, stmt_env)


    def visit_variable_decl(self, node: "VariableDecl", env: List[List[Any]]):
        def check_var_redeclared(var_list, var):
            name, init_type = self.visit(var, env)
            var_type = self.visit(node.var_type, env)
            
            var_symb = VariableSymb(node.is_final, var_type, name)
            if scope_contains(var_symb.name, var_list):
                raise Redeclared("Constant", var_symb.name) if node.is_final else Redeclared("Variable", var_symb.name)
            
            # Fill in the element type if array type is returned
            if type(var_type) is Tarray and type(init_type) is Tarray and not init_type.element_type:
                init_type.element_type = var_type.element_type
            
            # Non-constant variable declaration case is not specified for type checking
            if not node.is_final:
                if init_type and type(init_type) is not Tnil and not can_coerce_type(init_type, var_type):
                    raise TypeMismatchInStatement(node)
            
            # Constant variable declaration case
            if node.is_final:
                if not init_type:
                    raise IllegalConstantExpression(NilLiteral())
                
                # Initialization is not statically evaluable
                if not init_type.is_final:
                    raise IllegalConstantExpression(var.init_value)
                
                # Initialization doesn't match types (under coercion rules)
                if not can_coerce_type(init_type, var_type):
                    raise TypeMismatchInConstant(node)
            
            return var_list + [var_symb]

        block_scope = reduce(check_var_redeclared, node.variables, env[0])
        return [block_scope, *env[1:]]


    def visit_variable(self, node: "Variable", env: List[List[Any]]):
        init_type = self.visit(node.init_value, env) if node.init_value else None
        return node.name, init_type


    def visit_assignment_statement(self, node: "AssignmentStatement", env: List[List[Any]]):
        lhs_type = self.visit(node.lhs, env)
        rhs_type = self.visit(node.rhs, env)
        
        # Constant assignment
        if lhs_type.is_final:
            raise CannotAssignToConstant(node)
        
        if not can_coerce_type(rhs_type, lhs_type):
            raise TypeMismatchInStatement(node)


    def visit_if_statement(self, node: "IfStatement", env: List[List[Any]]):
        condition_type = self.visit(node.condition, env)
        if type(condition_type) is not Tboolean:
            raise TypeMismatchInStatement(node)
        
        then_env = [[]] + env
        self.visit(node.then_stmt, then_env)
        
        if node.else_stmt:
            else_env = [[]] + env
            self.visit(node.else_stmt, else_env)


    def visit_for_statement(self, node: "ForStatement", env: List[List[Any]]):
        idx_symb = get_symb_by_id(node.variable, env)
        if idx_symb and type(idx_symb) in [AttributeSymb, ParameterSymb, VariableSymb] and type(idx_symb.type) is not Tint:
            raise TypeMismatchInStatement(node)
        
        if not idx_symb or type(idx_symb) not in [AttributeSymb, ParameterSymb, VariableSymb]:
            idx_symb = VariableSymb(False, Tint(), node.variable)
        
        start_type = self.visit(node.start_expr, env)
        end_type = self.visit(node.end_expr, env)
        if type(start_type) is not Tint or type(end_type) is not Tint:
            raise TypeMismatchInStatement(node)
        
        for_signal = ForSignal()
        self.visit(node.body, [[for_signal, idx_symb]] + env)


    def visit_break_statement(self, node: "BreakStatement", env: List[List[Any]]):
        for_signal = get_for_signal(env)
        if not for_signal:
            raise MustInLoop(node)


    def visit_continue_statement(self, node: "ContinueStatement", env: List[List[Any]]):
        for_signal = get_for_signal(env)
        if not for_signal:
            raise MustInLoop(node)


    def visit_return_statement(self, node: "ReturnStatement", env: List[List[Any]]):
        return_type = self.processing_method.return_type
        if type(return_type) in [Tnil, Tvoid]:
            raise TypeMismatchInStatement(node)
        
        value_type = self.visit(node.value, env)
        if type(value_type) is not type(return_type):
            raise TypeMismatchInStatement(node)


    def visit_method_invocation_statement(self, node: "MethodInvocationStatement", env: List[List[Any]]):
        return_type = self.visit(node.method_call, env)
        if type(return_type) not in [Tnil, Tvoid]:
            raise TypeMismatchInStatement(node)

    # Left-hand side (LHS)

    def visit_id_lhs(self, node: "IdLHS", env: List[List[Any]]):
        found_symb = get_symb_by_id(node.name, env)
        if not found_symb:
            raise UndeclaredIdentifier(node.name)
        if type(found_symb) not in [AttributeSymb, VariableSymb, ParameterSymb]:
            return Tvoid()
        return found_symb.type


    def visit_postfix_lhs(self, node: "PostfixLHS", env: List[List[Any]]):
        postfix_type = self.visit(node.postfix_expr, env)
        return postfix_type

    # Expressions

    def visit_binary_op(self, node: "BinaryOp", env: List[List[Any]]):
        left_type = self.visit(node.left, env)
        right_type = self.visit(node.right, env)
        
        # Arithmetic operations
        if node.operator in ["+", "-", "*", "/"]:
            if not type(left_type) in [Tint, Tfloat] or not type(right_type) in [Tint, Tfloat]:
                raise TypeMismatchInExpression(node)
            if type(left_type) is Tfloat or type(right_type) is Tfloat:
                return Tfloat().set_final_if(left_type.is_final and right_type.is_final)
            if node.operator == "/":
                return Tfloat().set_final_if(left_type.is_final and right_type.is_final)
            return Tint().set_final_if(left_type.is_final and right_type.is_final)

        if node.operator in ["\\", "%"]:
            if type(left_type) is not Tint or type(right_type) is not Tint:
                raise TypeMismatchInExpression(node)
            return Tint().set_final_if(left_type.is_final and right_type.is_final)
        
        # Boolean operations
        if node.operator in ["&&", "||"]:
            if type(left_type) is not Tboolean or type(right_type) is not Tboolean:
                raise TypeMismatchInExpression(node)
            return Tboolean().set_final_if(left_type.is_final and right_type.is_final)
        
        # Relational operators
        if node.operator in ["==", "!="]:
            if type(left_type) not in [Tint, Tboolean] or type(right_type) not in [Tint, Tboolean]:
                raise TypeMismatchInExpression(node)
            if type(left_type) is not type(right_type):
                raise TypeMismatchInExpression(node)
            return Tboolean().set_final_if(left_type.is_final and right_type.is_final)
        
        if node.operator in [">", "<", ">=", "<="]:
            if type(left_type) not in [Tint, Tfloat] or type(right_type) not in [Tint, Tfloat]:
                raise TypeMismatchInExpression(node)
            return Tboolean().set_final_if(left_type.is_final and right_type.is_final)
        
        # String operators
        if node.operator in ["^"]:
            if type(left_type) is not Tstring or type(right_type) is not Tstring:
                raise TypeMismatchInExpression(node)
            return Tstring().set_final_if(left_type.is_final and right_type.is_final)

        raise TypeMismatchInExpression(node)


    def visit_unary_op(self, node: "UnaryOp", env: List[List[Any]]):
        operand_type = self.visit(node.operand, env)

        # Arithmetic operators
        if node.operator in ["+", "-"]:
            if type(operand_type) not in [Tint, Tfloat]:
                raise TypeMismatchInExpression(node)
            return operand_type.set_final_if(operand_type.is_final)

        # Boolean operators
        if node.operator in ["!"]:
            if type(operand_type) is not Tboolean:
                raise TypeMismatchInExpression(node)
            return operand_type.set_final_if(operand_type.is_final)
        
        raise TypeMismatchInExpression(node)


    def visit_postfix_expression(self, node: "PostfixExpression", env: List[List[Any]]):
        primary_type = self.visit(node.primary, env)
        
        def evaluate_postfix_expressions(current_type, postfix_op):
            postfix_type = self.visit(postfix_op, env)
            
            # Method call
            if type(postfix_type) is MethodPostfix:
                
                # Static method call
                if type(current_type) is ClassSymb:
                    method_symb = get_class_attribute(current_type, postfix_type.name)
                    if not method_symb or type(method_symb) is not MethodSymb:
                        raise UndeclaredMethod(postfix_type.name)
                    
                    if type(method_symb.return_type) in [Tnil, Tvoid]:
                        raise TypeMismatchInExpression(node)
                    
                    if not can_coerce_args(postfix_type.arg_types, method_symb.param_types):
                        raise TypeMismatchInExpression(node)
                    
                    if not method_symb.is_static:
                        raise IllegalMemberAccess(node)
                    
                    return method_symb.return_type.set_final_if(False)
                
                # Instance method call
                if type(current_type) is Tclass:
                    class_symb = current_type.symb if current_type.symb else get_class_symb(current_type.name, env[-1])
                    if not class_symb:
                        raise UndeclaredClass(current_type.name)
                    
                    method_symb = get_class_attribute(class_symb, postfix_type.name)
                    if not method_symb or type(method_symb) is not MethodSymb:
                        raise UndeclaredMethod(postfix_type.name)
                    
                    if type(method_symb.return_type) in [Tnil, Tvoid]:
                        raise TypeMismatchInExpression(node)
                    
                    if not can_coerce_args(postfix_type.arg_types, method_symb.param_types):
                        raise TypeMismatchInExpression(node)
                    
                    if method_symb.is_static:
                        raise IllegalMemberAccess(node)
                    
                    return method_symb.return_type.set_final_if(False)

                raise TypeMismatchInExpression(node)
            
            # Member access
            if type(postfix_type) is MemberPostfix:
                
                # Static member access
                if type(current_type) is ClassSymb:
                    attr_symb = get_class_attribute(current_type, postfix_type.name)
                    if not attr_symb or type(attr_symb) is not AttributeSymb:
                        raise UndeclaredAttribute(postfix_type.name)
                    
                    if not attr_symb.is_static:
                        raise IllegalMemberAccess(node)
                    
                    return attr_symb.type.set_final_if(False)
                
                # Instance member access
                if type(current_type) is Tclass:
                    class_symb = current_type.symb if current_type.symb else get_class_symb(current_type.name, env[-1])
                    if not class_symb:
                        raise UndeclaredClass(current_type.name)
                    
                    attr_symb = get_class_attribute(class_symb, postfix_type.name)
                    if not attr_symb or type(attr_symb) is not AttributeSymb:
                        raise UndeclaredAttribute(postfix_type.name)
                    
                    if attr_symb.is_static:
                        raise IllegalMemberAccess(node)
                    
                    return attr_symb.type.set_final_if(False)
                
                raise TypeMismatchInExpression(node)
            
            # Array access
            if type(postfix_type) is ArrayPostfix:
                if type(current_type) is not Tarray:
                    raise TypeMismatchInExpression(node)
                return current_type.element_type.set_final_if(False)
            
            raise TypeMismatchInExpression(node)
            
        output_type = reduce(evaluate_postfix_expressions, node.postfix_ops, primary_type)
        return output_type.set_final_if(False)


    def visit_method_call(self, node: "MethodCall", env: List[List[Any]]):
        arg_types = list(map(lambda arg: self.visit(arg, env), node.args))
        return MethodPostfix(node.method_name, arg_types)


    def visit_member_access(self, node: "MemberAccess", env: List[List[Any]]):
        return MemberPostfix(node.member_name)


    def visit_array_access(self, node: "ArrayAccess", env: List[List[Any]]):
        index_type = self.visit(node.index, env)
        if type(index_type) is not Tint:
            raise TypeMismatchInExpression(node)
        return ArrayPostfix()


    def visit_object_creation(self, node: "ObjectCreation", env: List[List[Any]]):
        class_symb = get_class_symb(node.class_name, env[-1])
        if not class_symb:
            raise UndeclaredClass(node.class_name)
        return Tclass(class_symb.name, class_symb.superclass)


    def visit_identifier(self, node: "Identifier", env: List[List[Any]]):
        cls = self.processing_class
        found_symb = cls if cls.name == node.name else get_symb_by_id(node.name, env)
        if not found_symb:
            raise UndeclaredIdentifier(node.name)
        
        if type(found_symb) in [AttributeSymb, ParameterSymb, VariableSymb]:
            return found_symb.type
        return found_symb


    def visit_this_expression(self, node: "ThisExpression", env: List[List[Any]]):
        cls = self.processing_class
        return Tclass(cls.name, cls.superclass, cls)


    def visit_parenthesized_expression(self, node: "ParenthesizedExpression", env: List[List[Any]]):
        return self.visit(node.expr, env)

    # Literals

    def visit_int_literal(self, node: "IntLiteral", env: List[List[Any]]):
        return Tint(is_final=True)


    def visit_float_literal(self, node: "FloatLiteral", env: List[List[Any]]):
        return Tfloat(is_final=True)


    def visit_bool_literal(self, node: "BoolLiteral", env: List[List[Any]]):
        return Tboolean(is_final=True)


    def visit_string_literal(self, node: "StringLiteral", env: List[List[Any]]):
        return Tstring(is_final=True)


    def visit_array_literal(self, node: "ArrayLiteral", env: List[List[Any]]):
        def check_same_type_literal(types, element):
            element_type = self.visit(element, env)
            if type(element_type) in [Tvoid, Tnil, Tarray]:
                    raise IllegalArrayLiteral(node)
            
            if types:
                recent_type = types[-1]
                if type(element_type) is not type(recent_type):
                    raise IllegalArrayLiteral(node)
            
            return types + [element_type]
        
        type_list = reduce(check_same_type_literal, node.value, [])
        element_type = type_list[0] if type_list else None
        
        array_type = Tarray(element_type, len(type_list))
        array_type.is_final = all(t.is_final for t in type_list)
        return array_type


    def visit_nil_literal(self, node: "NilLiteral", env: List[List[Any]]):
        return Tnil()
    
    def visit_static_method_invocation(
        self, node: "StaticMethodInvocation", o: Any = None
    ):
        for arg in node.args:
            self.visit(arg, o)

    def visit_static_member_access(self, node: "StaticMemberAccess", o: Any = None):
        pass

    def visit_method_invocation(self, node: "MethodInvocation", o: Any = None):
        self.visit(node.postfix_expr, o)


class BaseVisitor(ASTVisitor):
    """Base visitor that provides default implementations for all visit methods.
    Subclasses can override only the methods they need to customize."""

    def visit_program(self, node: "Program", o: Any = None):
        for class_decl in node.class_decls:
            self.visit(class_decl, o)

    def visit_class_decl(self, node: "ClassDecl", o: Any = None):
        for member in node.members:
            self.visit(member, o)

    def visit_attribute_decl(self, node: "AttributeDecl", o: Any = None):
        self.visit(node.attr_type, o)
        for attr in node.attributes:
            self.visit(attr, o)

    def visit_attribute(self, node: "Attribute", o: Any = None):
        if node.init_value:
            self.visit(node.init_value, o)

    def visit_method_decl(self, node: "MethodDecl", o: Any = None):
        self.visit(node.return_type, o)
        for param in node.params:
            self.visit(param, o)
        self.visit(node.body, o)

    def visit_constructor_decl(self, node: "ConstructorDecl", o: Any = None):
        for param in node.params:
            self.visit(param, o)
        self.visit(node.body, o)

    def visit_destructor_decl(self, node: "DestructorDecl", o: Any = None):
        self.visit(node.body, o)

    def visit_parameter(self, node: "Parameter", o: Any = None):
        self.visit(node.param_type, o)

    def visit_primitive_type(self, node: "PrimitiveType", o: Any = None):
        pass

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        self.visit(node.element_type, o)

    def visit_class_type(self, node: "ClassType", o: Any = None):
        pass

    def visit_reference_type(self, node: "ReferenceType", o: Any = None):
        self.visit(node.referenced_type, o)

    def visit_block_statement(self, node: "BlockStatement", o: Any = None):
        for var_decl in node.var_decls:
            self.visit(var_decl, o)
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_variable_decl(self, node: "VariableDecl", o: Any = None):
        self.visit(node.var_type, o)
        for var in node.variables:
            self.visit(var, o)

    def visit_variable(self, node: "Variable", o: Any = None):
        if node.init_value:
            self.visit(node.init_value, o)

    def visit_assignment_statement(self, node: "AssignmentStatement", o: Any = None):
        self.visit(node.lhs, o)
        self.visit(node.rhs, o)

    def visit_if_statement(self, node: "IfStatement", o: Any = None):
        self.visit(node.condition, o)
        self.visit(node.then_stmt, o)
        if node.else_stmt:
            self.visit(node.else_stmt, o)

    def visit_for_statement(self, node: "ForStatement", o: Any = None):
        self.visit(node.start_expr, o)
        self.visit(node.end_expr, o)
        self.visit(node.body, o)

    def visit_break_statement(self, node: "BreakStatement", o: Any = None):
        pass

    def visit_continue_statement(self, node: "ContinueStatement", o: Any = None):
        pass

    def visit_return_statement(self, node: "ReturnStatement", o: Any = None):
        self.visit(node.value, o)

    def visit_method_invocation_statement(
        self, node: "MethodInvocationStatement", o: Any = None
    ):
        self.visit(node.method_invocation, o)

    def visit_id_lhs(self, node: "IdLHS", o: Any = None):
        pass

    def visit_postfix_lhs(self, node: "PostfixLHS", o: Any = None):
        self.visit(node.postfix_expr, o)

    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        self.visit(node.left, o)
        self.visit(node.right, o)

    def visit_unary_op(self, node: "UnaryOp", o: Any = None):
        self.visit(node.operand, o)

    def visit_postfix_expression(self, node: "PostfixExpression", o: Any = None):
        self.visit(node.primary, o)
        for op in node.postfix_ops:
            self.visit(op, o)

    def visit_method_call(self, node: "MethodCall", o: Any = None):
        for arg in node.args:
            self.visit(arg, o)

    def visit_member_access(self, node: "MemberAccess", o: Any = None):
        pass

    def visit_array_access(self, node: "ArrayAccess", o: Any = None):
        self.visit(node.index, o)

    def visit_object_creation(self, node: "ObjectCreation", o: Any = None):
        for arg in node.args:
            self.visit(arg, o)

    def visit_static_method_invocation(
        self, node: "StaticMethodInvocation", o: Any = None
    ):
        for arg in node.args:
            self.visit(arg, o)

    def visit_static_member_access(self, node: "StaticMemberAccess", o: Any = None):
        pass

    def visit_method_invocation(self, node: "MethodInvocation", o: Any = None):
        self.visit(node.postfix_expr, o)

    def visit_identifier(self, node: "Identifier", o: Any = None):
        pass

    def visit_this_expression(self, node: "ThisExpression", o: Any = None):
        pass

    def visit_parenthesized_expression(
        self, node: "ParenthesizedExpression", o: Any = None
    ):
        self.visit(node.expr, o)

    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        pass

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        pass

    def visit_bool_literal(self, node: "BoolLiteral", o: Any = None):
        pass

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        pass

    def visit_array_literal(self, node: "ArrayLiteral", o: Any = None):
        for elem in node.value:
            self.visit(elem, o)

    def visit_nil_literal(self, node: "NilLiteral", o: Any = None):
        pass