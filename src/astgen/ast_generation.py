"""
AST Generation module for OPLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.OPLangVisitor import OPLangVisitor
from build.OPLangParser import OPLangParser
from src.utils.nodes import *


class ASTGeneration(OPLangVisitor):
    # Visit a parse tree produced by OPLangParser#program.
    def visitProgram(self, ctx:OPLangParser.ProgramContext):
        # program: ne_cls_decl_list EOF;
        cls_decl_list = self.visit(ctx.ne_cls_decl_list())
        return Program(cls_decl_list)


    # Visit a parse tree produced by OPLangParser#ne_cls_decl_list.
    def visitNe_cls_decl_list(self, ctx:OPLangParser.Ne_cls_decl_listContext):
        # ne_cls_decl_list: cls_decl ne_cls_decl_list | cls_decl ;
        cls_decl_list = [self.visit(ctx.cls_decl())]
        if ctx.ne_cls_decl_list():
            return cls_decl_list + self.visit(ctx.ne_cls_decl_list())
        return cls_decl_list


    # Visit a parse tree produced by OPLangParser#cls_decl.
    def visitCls_decl(self, ctx:OPLangParser.Cls_declContext):
        # cls_decl: CLASS ID cls_extension LB mem_decl_list RB ;
        cls_name = str(ctx.ID())
        sup_name = self.visit(ctx.cls_extension())
        mem_decl_list = self.visit(ctx.mem_decl_list())
        return ClassDecl(cls_name, sup_name, mem_decl_list)


    # Visit a parse tree produced by OPLangParser#cls_extension.
    def visitCls_extension(self, ctx:OPLangParser.Cls_extensionContext):
        # cls_extension: EXTENDS ID |  ;
        return str(ctx.ID()) if ctx.ID() else None


    # Visit a parse tree produced by OPLangParser#mem_decl_list.
    def visitMem_decl_list(self, ctx:OPLangParser.Mem_decl_listContext):
        # mem_decl_list: mem_decl mem_decl_list |  ;
        if not ctx.mem_decl():
            return []
        mem_decl_list = [self.visit(ctx.mem_decl())]
        return mem_decl_list + self.visit(ctx.mem_decl_list())


    # Visit a parse tree produced by OPLangParser#mem_decl.
    def visitMem_decl(self, ctx:OPLangParser.Mem_declContext):
        # mem_decl: attr_decl | method_decl | constructor_decl | destructor_decl ;
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#attr_decl.
    def visitAttr_decl(self, ctx:OPLangParser.Attr_declContext):
        # attr_decl: attr_modifier dtype ne_cm_asgn_id_list SEMI ;
        is_static, is_final = self.visit(ctx.attr_modifier())
        attr_type = self.visit(ctx.dtype())
        attr_list = self.visitNe_cm_asgn_id_list(ctx.ne_cm_asgn_id_list(), Attribute)
        return AttributeDecl(is_static, is_final, attr_type, attr_list)


    # Visit a parse tree produced by OPLangParser#attr_modifier.
    def visitAttr_modifier(self, ctx:OPLangParser.Attr_modifierContext):
        # attr_modifier: FINAL | STATIC | FINAL STATIC | STATIC FINAL |  ;
        is_static = bool(ctx.STATIC())
        is_final = bool(ctx.FINAL())
        return is_static, is_final


    # Visit a parse tree produced by OPLangParser#ne_cm_asgn_id_list.
    def visitNe_cm_asgn_id_list(self, ctx:OPLangParser.Ne_cm_asgn_id_listContext, structure):
        # ne_cm_asgn_id_list: asgn_id COMMA ne_cm_asgn_id_list | asgn_id ;
        attr_list = [self.visitAsgn_id(ctx.asgn_id(), structure)]
        if ctx.ne_cm_asgn_id_list():
            return attr_list + self.visitNe_cm_asgn_id_list(ctx.ne_cm_asgn_id_list(), structure)
        return attr_list


    # Visit a parse tree produced by OPLangParser#asgn_id.
    def visitAsgn_id(self, ctx:OPLangParser.Asgn_idContext, structure):
        # asgn_id: ID asgn_expr ;
        name = str(ctx.ID())
        init_value = self.visit(ctx.asgn_expr())
        return structure(name, init_value)


    # Visit a parse tree produced by OPLangParser#asgn_expr.
    def visitAsgn_expr(self, ctx:OPLangParser.Asgn_exprContext):
        # asgn_expr: ASSIGN expr |  ;
        if not ctx.expr():
            return None
        return self.visit(ctx.expr())


    # Visit a parse tree produced by OPLangParser#method_decl.
    def visitMethod_decl(self, ctx:OPLangParser.Method_declContext):
        # method_decl: method_modifier dtype ID LP sm_param_decl_list RP block_stmt ;
        is_static = self.visit(ctx.method_modifier())
        return_type = self.visit(ctx.dtype())
        name = str(ctx.ID())
        param_list = self.visit(ctx.sm_param_decl_list())
        body = self.visit(ctx.block_stmt())
        return MethodDecl(is_static, return_type, name, param_list, body)


    # Visit a parse tree produced by OPLangParser#method_modifier.
    def visitMethod_modifier(self, ctx:OPLangParser.Method_modifierContext):
        # method_modifier: STATIC |  ;
        return bool(ctx.STATIC())


    # Visit a parse tree produced by OPLangParser#sm_param_decl_list.
    def visitSm_param_decl_list(self, ctx:OPLangParser.Sm_param_decl_listContext):
        # sm_param_decl_list: ne_sm_param_decl_list |  ;
        if not ctx.ne_sm_param_decl_list():
            return []
        return self.visit(ctx.ne_sm_param_decl_list())


    # Visit a parse tree produced by OPLangParser#ne_sm_param_decl_list.
    def visitNe_sm_param_decl_list(self, ctx:OPLangParser.Ne_sm_param_decl_listContext):
        # ne_sm_param_decl_list: param_decl SEMI sm_param_decl_list | param_decl ;
        param_list = self.visit(ctx.param_decl())
        if ctx.sm_param_decl_list():
            return param_list + self.visit(ctx.sm_param_decl_list())
        return param_list


    # Visit a parse tree produced by OPLangParser#param_decl.
    def visitParam_decl(self, ctx:OPLangParser.Param_declContext):
        # param_decl: dtype ne_cm_id_list ;
        common_type = self.visit(ctx.dtype())
        id_list = self.visit(ctx.ne_cm_id_list())
        return list(map(lambda id: Parameter(common_type, id), id_list))


    # Visit a parse tree produced by OPLangParser#ne_cm_id_list.
    def visitNe_cm_id_list(self, ctx:OPLangParser.Ne_cm_id_listContext):
        # ne_cm_id_list: ID COMMA ne_cm_id_list | ID ;
        id_list = [str(ctx.ID())]
        if ctx.ne_cm_id_list():
            return id_list + self.visit(ctx.ne_cm_id_list())
        return id_list


    # Visit a parse tree produced by OPLangParser#constructor_decl.
    def visitConstructor_decl(self, ctx:OPLangParser.Constructor_declContext):
        # constructor_decl: default_constructor_decl
        #                 | copy_constructor_decl
        #                 | user_constructor_decl ;
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#default_constructor_decl.
    def visitDefault_constructor_decl(self, ctx:OPLangParser.Default_constructor_declContext):
        # default_constructor_decl: ID LP RP block_stmt ;
        cons_name = str(ctx.ID())
        param_list = []
        body = self.visit(ctx.block_stmt())
        return ConstructorDecl(cons_name, param_list, body)


    # Visit a parse tree produced by OPLangParser#copy_constructor_decl.
    def visitCopy_constructor_decl(self, ctx:OPLangParser.Copy_constructor_declContext):
        # copy_constructor_decl: ID LP ID ID RP block_stmt ;
        cons_name = str(ctx.ID(0))
        cls_name = str(ctx.ID(1))
        param_name = str(ctx.ID(2))
        param_list = [Parameter(ClassType(cls_name), param_name)]
        body = self.visit(ctx.block_stmt())
        return ConstructorDecl(cons_name, param_list, body)


    # Visit a parse tree produced by OPLangParser#user_constructor_decl.
    def visitUser_constructor_decl(self, ctx:OPLangParser.User_constructor_declContext):
        # user_constructor_decl: ID LP sm_param_decl_list RP block_stmt ;
        cons_name = str(ctx.ID())
        param_list = self.visit(ctx.sm_param_decl_list())
        body = self.visit(ctx.block_stmt())
        return ConstructorDecl(cons_name, param_list, body)


    # Visit a parse tree produced by OPLangParser#destructor_decl.
    def visitDestructor_decl(self, ctx:OPLangParser.Destructor_declContext):
        # destructor_decl: TILDE ID LP RP block_stmt ;
        dest_name = str(ctx.ID())
        body = self.visit(ctx.block_stmt())
        return DestructorDecl(dest_name, body)


    # Visit a parse tree produced by OPLangParser#dtype.
    def visitDtype(self, ctx:OPLangParser.DtypeContext):
        # dtype: ptype | atype | ctype | rtype | VOID ;
        if ctx.VOID():
            return PrimitiveType(str(ctx.VOID()))
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ptype.
    def visitPtype(self, ctx:OPLangParser.PtypeContext):
        # ptype: INT | FLOAT | BOOLEAN | STRING ;
        type_name = str(ctx.INT())
        type_name = str(ctx.FLOAT()) if ctx.FLOAT() else type_name
        type_name = str(ctx.BOOLEAN()) if ctx.BOOLEAN() else type_name
        type_name = str(ctx.STRING()) if ctx.STRING() else type_name
        return PrimitiveType(type_name)


    # Visit a parse tree produced by OPLangParser#atype.
    def visitAtype(self, ctx:OPLangParser.AtypeContext):
        # atype: (ptype | ctype) LSB INTLIT RSB ;
        ele_type = self.visit(ctx.getChild(0))
        size = int(str(ctx.INTLIT()))
        return ArrayType(ele_type, size)


    # Visit a parse tree produced by OPLangParser#ctype.
    def visitCtype(self, ctx:OPLangParser.CtypeContext):
        # ctype: ID ;
        cls_name = str(ctx.ID())
        return ClassType(cls_name)


    # Visit a parse tree produced by OPLangParser#rtype.
    def visitRtype(self, ctx:OPLangParser.RtypeContext):
        # rtype: (ptype | atype | ctype) AMPERSAND ;
        base_type = self.visit(ctx.getChild(0))
        return ReferenceType(base_type)


    # Visit a parse tree produced by OPLangParser#expr.
    def visitExpr(self, ctx:OPLangParser.ExprContext):
        # expr    : gtexpr (LT | GT | LTE | GTE) gtexpr | gtexpr ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.gtexpr(0))
        lhs, rhs = self.visit(ctx.gtexpr(0)), self.visit(ctx.gtexpr(1))
        op = str(ctx.getChild(1))
        return BinaryOp(lhs, op, rhs)


    # Visit a parse tree produced by OPLangParser#gtexpr.
    def visitGtexpr(self, ctx:OPLangParser.GtexprContext):
        # gtexpr  : eqexpr (EQ | NEQ) eqexpr | eqexpr ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.eqexpr(0))
        lhs, rhs = self.visit(ctx.eqexpr(0)), self.visit(ctx.eqexpr(1))
        op = str(ctx.getChild(1))
        return BinaryOp(lhs, op, rhs)


    # Visit a parse tree produced by OPLangParser#eqexpr.
    def visitEqexpr(self, ctx:OPLangParser.EqexprContext):
        # eqexpr  : eqexpr (AND | OR) lgexpr | lgexpr ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.lgexpr())
        lhs, rhs = self.visit(ctx.eqexpr()), self.visit(ctx.lgexpr())
        op = str(ctx.getChild(1))
        return BinaryOp(lhs, op, rhs)


    # Visit a parse tree produced by OPLangParser#lgexpr.
    def visitLgexpr(self, ctx:OPLangParser.LgexprContext):
        # lgexpr  : lgexpr (ADD | SUB) addexpr | addexpr ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.addexpr())
        lhs, rhs = self.visit(ctx.lgexpr()), self.visit(ctx.addexpr())
        op = str(ctx.getChild(1))
        return BinaryOp(lhs, op, rhs)


    # Visit a parse tree produced by OPLangParser#addexpr.
    def visitAddexpr(self, ctx:OPLangParser.AddexprContext):
        # addexpr : addexpr (MUL | FLTDIV | INTDIV | MOD) mulexpr | mulexpr ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.mulexpr())
        lhs, rhs = self.visit(ctx.addexpr()), self.visit(ctx.mulexpr())
        op = str(ctx.getChild(1))
        return BinaryOp(lhs, op, rhs)


    # Visit a parse tree produced by OPLangParser#mulexpr.
    def visitMulexpr(self, ctx:OPLangParser.MulexprContext):
        # mulexpr : mulexpr CONCAT conexpr | conexpr ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.conexpr())
        lhs, rhs = self.visit(ctx.mulexpr()), self.visit(ctx.conexpr())
        op = str(ctx.getChild(1))
        return BinaryOp(lhs, op, rhs)


    # Visit a parse tree produced by OPLangParser#conexpr.
    def visitConexpr(self, ctx:OPLangParser.ConexprContext):
        # conexpr : NOT conexpr | notexpr ;
        if not ctx.NOT():
            return self.visit(ctx.notexpr())
        op = str(ctx.NOT())
        operand = self.visit(ctx.conexpr())
        return UnaryOp(op, operand)


    # Visit a parse tree produced by OPLangParser#notexpr.
    def visitNotexpr(self, ctx:OPLangParser.NotexprContext):
        # notexpr : (ADD | SUB) notexpr | uniexpr ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.uniexpr())
        op = str(ctx.getChild(0))
        operand = self.visit(ctx.notexpr())
        return UnaryOp(op, operand)


    # Visit a parse tree produced by OPLangParser#uniexpr.
    def visitUniexpr(self, ctx:OPLangParser.UniexprContext, postfix_ops=[]):
        # uniexpr : uniexpr LSB expr RSB | uniexpr DOT ID callargs | idxexpr ;
        if ctx.getChildCount() == 1:
            if not postfix_ops:
                return self.visit(ctx.idxexpr())
            primary = self.visit(ctx.idxexpr())
            return PostfixExpression(primary, postfix_ops)
        if ctx.expr():
            idx_expr = self.visit(ctx.expr())
            postfix_op = ArrayAccess(idx_expr)
        if ctx.ID():
            name = str(ctx.ID())
            args = self.visit(ctx.callargs())
            postfix_op = MemberAccess(name) if args is None else MethodCall(name, args)
        postfix_ops = [postfix_op] + postfix_ops
        return self.visitUniexpr(ctx.uniexpr(), postfix_ops)


    # Visit a parse tree produced by OPLangParser#idxexpr.
    def visitIdxexpr(self, ctx:OPLangParser.IdxexprContext):
        # idxexpr : NEW ID LP cm_expr_list RP | newexpr ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.newexpr())
        cls_name = str(ctx.ID())
        args = self.visit(ctx.cm_expr_list())
        return ObjectCreation(cls_name, args)


    # Visit a parse tree produced by OPLangParser#newexpr.
    def visitNewexpr(self, ctx:OPLangParser.NewexprContext):
        # newexpr : LP expr RP | parexpr ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.parexpr())
        paren_expr = self.visit(ctx.expr())
        return ParenthesizedExpression(paren_expr)


    # Visit a parse tree produced by OPLangParser#parexpr.
    def visitParexpr(self, ctx:OPLangParser.ParexprContext):
        # parexpr : lit | ID | THIS | NIL ;
        if ctx.lit():
            return self.visit(ctx.lit())
        if ctx.ID():
            return Identifier(str(ctx.ID()))
        if ctx.THIS():
            return ThisExpression()
        return NilLiteral()


    # Visit a parse tree produced by OPLangParser#callargs.
    def visitCallargs(self, ctx:OPLangParser.CallargsContext):
        # callargs: LP cm_expr_list RP |  ;
        if ctx.cm_expr_list():
            return self.visit(ctx.cm_expr_list())
        return None


    # Visit a parse tree produced by OPLangParser#cm_expr_list.
    def visitCm_expr_list(self, ctx:OPLangParser.Cm_expr_listContext):
        # cm_expr_list: ne_cm_expr_list |  ;
        if ctx.ne_cm_expr_list():
            return self.visit(ctx.ne_cm_expr_list())
        return []


    # Visit a parse tree produced by OPLangParser#ne_cm_expr_list.
    def visitNe_cm_expr_list(self, ctx:OPLangParser.Ne_cm_expr_listContext):
        # ne_cm_expr_list: expr COMMA cm_expr_list | expr ;
        expr_list = [self.visit(ctx.expr())]
        if ctx.cm_expr_list():
            return expr_list + self.visit(ctx.cm_expr_list())
        return expr_list


    # Visit a parse tree produced by OPLangParser#lit.
    def visitLit(self, ctx:OPLangParser.LitContext):
        # lit: plit | alit ;
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#plit.
    def visitPlit(self, ctx:OPLangParser.PlitContext):
        # plit: INTLIT | FLOATLIT | BOOLLIT | STRINGLIT ;
        raw = str(ctx.getChild(0))
        if ctx.INTLIT():
            return IntLiteral(int(raw))
        if ctx.FLOATLIT():
            return FloatLiteral(float(raw))
        if ctx.BOOLLIT():
            return BoolLiteral(raw == "true")
        return StringLiteral(raw[1:-1])


    # Visit a parse tree produced by OPLangParser#alit.
    def visitAlit(self, ctx:OPLangParser.AlitContext):
        # alit: LB ne_cm_plit_list RB ;
        expr_list = self.visit(ctx.ne_cm_plit_list())
        return ArrayLiteral(expr_list)


    # Visit a parse tree produced by OPLangParser#ne_cm_plit_list.
    def visitNe_cm_plit_list(self, ctx:OPLangParser.Ne_cm_plit_listContext):
        # ne_cm_plit_list: plit COMMA ne_cm_plit_list | plit ;
        plit_list = [self.visit(ctx.plit())]
        if ctx.ne_cm_plit_list():
            return plit_list + self.visit(ctx.ne_cm_plit_list())
        return plit_list


    # Visit a parse tree produced by OPLangParser#stmt.
    def visitStmt(self, ctx:OPLangParser.StmtContext):
        # stmt: match_stmt | open_stmt ;
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#other_stmt.
    def visitOther_stmt(self, ctx:OPLangParser.Other_stmtContext):
        # other_stmt: block_stmt | asgn_stmt | for_stmt
        #           | break_stmt | cont_stmt | ret_stmt | invk_stmt ;
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#block_stmt.
    def visitBlock_stmt(self, ctx:OPLangParser.Block_stmtContext):
        # block_stmt: LB vardecl_list stmt_list RB ;
        var_list = self.visit(ctx.vardecl_list())
        stmt_list = self.visit(ctx.stmt_list())
        return BlockStatement(var_list, stmt_list)


    # Visit a parse tree produced by OPLangParser#vardecl_list.
    def visitVardecl_list(self, ctx:OPLangParser.Vardecl_listContext):
        # vardecl_list: vardecl vardecl_list |  ;
        if not ctx.vardecl():
            return []
        var_list = [self.visit(ctx.vardecl())]
        return var_list + self.visit(ctx.vardecl_list())


    # Visit a parse tree produced by OPLangParser#vardecl.
    def visitVardecl(self, ctx:OPLangParser.VardeclContext):
        # vardecl: var_modifier dtype ne_cm_asgn_id_list SEMI ;
        is_final = self.visit(ctx.var_modifier())
        var_type = self.visit(ctx.dtype())
        var_list = self.visitNe_cm_asgn_id_list(ctx.ne_cm_asgn_id_list(), Variable)
        return VariableDecl(is_final, var_type, var_list)


    # Visit a parse tree produced by OPLangParser#var_modifier.
    def visitVar_modifier(self, ctx:OPLangParser.Var_modifierContext):
        # var_modifier: FINAL |  ;
        return bool(ctx.FINAL())


    # Visit a parse tree produced by OPLangParser#stmt_list.
    def visitStmt_list(self, ctx:OPLangParser.Stmt_listContext):
        # stmt_list: stmt stmt_list |  ;
        if not ctx.stmt():
            return []
        stmt_list = [self.visit(ctx.stmt())]
        return stmt_list + self.visit(ctx.stmt_list())


    # Visit a parse tree produced by OPLangParser#asgn_stmt.
    def visitAsgn_stmt(self, ctx:OPLangParser.Asgn_stmtContext):
        # asgn_stmt: asgnlhs ASSIGN expr SEMI ;
        lhs = self.visit(ctx.asgnlhs())
        rhs = self.visit(ctx.expr())
        return AssignmentStatement(lhs, rhs)


    # Visit a parse tree produced by OPLangParser#asgnlhs.
    def visitAsgnlhs(self, ctx:OPLangParser.AsgnlhsContext):
        # asgnlhs: uniexpr ;
        lhs = self.visit(ctx.uniexpr())
        if isinstance(lhs, Identifier):
            lhs = IdLHS(lhs.name)
        if isinstance(lhs, PostfixExpression):
            lhs = PostfixLHS(lhs)
        return lhs


    # Visit a parse tree produced by OPLangParser#match_stmt.
    def visitMatch_stmt(self, ctx:OPLangParser.Match_stmtContext):
        # match_stmt: IF expr THEN match_stmt ELSE match_stmt | other_stmt ;
        if ctx.other_stmt():
            return self.visit(ctx.other_stmt())
        condition = self.visit(ctx.expr())
        then_stmt = self.visit(ctx.match_stmt(0))
        else_stmt = self.visit(ctx.match_stmt(1))
        return IfStatement(condition, then_stmt, else_stmt)


    # Visit a parse tree produced by OPLangParser#open_stmt.
    def visitOpen_stmt(self, ctx:OPLangParser.Open_stmtContext):
        # open_stmt: IF expr THEN stmt | IF expr THEN match_stmt ELSE open_stmt ;
        condition = self.visit(ctx.expr())
        if not ctx.ELSE():
            then_stmt = self.visit(ctx.stmt())
            return IfStatement(condition, then_stmt)
        then_stmt = self.visit(ctx.match_stmt())
        else_stmt = self.visit(ctx.open_stmt())
        return IfStatement(condition, then_stmt, else_stmt)


    # Visit a parse tree produced by OPLangParser#for_stmt.
    def visitFor_stmt(self, ctx:OPLangParser.For_stmtContext):
        # for_stmt: FOR ID ASSIGN expr (TO | DOWNTO) expr DO stmt ;
        var_name = str(ctx.ID())
        start = self.visit(ctx.expr(0))
        dir = str(ctx.getChild(4))
        end = self.visit(ctx.expr(1))
        body = self.visit(ctx.stmt())
        return ForStatement(var_name, start, dir, end, body)

    # Visit a parse tree produced by OPLangParser#break_stmt.
    def visitBreak_stmt(self, ctx:OPLangParser.Break_stmtContext):
        # break_stmt: BREAK SEMI ;
        return BreakStatement()


    # Visit a parse tree produced by OPLangParser#cont_stmt.
    def visitCont_stmt(self, ctx:OPLangParser.Cont_stmtContext):
        # cont_stmt: CONTINUE SEMI ;
        return ContinueStatement()


    # Visit a parse tree produced by OPLangParser#ret_stmt.
    def visitRet_stmt(self, ctx:OPLangParser.Ret_stmtContext):
        # ret_stmt: RETURN expr SEMI ;
        expr = self.visit(ctx.expr())
        return ReturnStatement(expr)


    # Visit a parse tree produced by OPLangParser#invk_stmt.
    def visitInvk_stmt(self, ctx:OPLangParser.Invk_stmtContext):
        # invk_stmt: uniexpr SEMI ;
        postfix_expr = self.visit(ctx.uniexpr())
        return MethodInvocationStatement(postfix_expr)
