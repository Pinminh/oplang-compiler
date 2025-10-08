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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ne_cls_decl_list.
    def visitNe_cls_decl_list(self, ctx:OPLangParser.Ne_cls_decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#cls_decl.
    def visitCls_decl(self, ctx:OPLangParser.Cls_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#cls_extension.
    def visitCls_extension(self, ctx:OPLangParser.Cls_extensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#mem_decl_list.
    def visitMem_decl_list(self, ctx:OPLangParser.Mem_decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#mem_decl.
    def visitMem_decl(self, ctx:OPLangParser.Mem_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#attr_decl.
    def visitAttr_decl(self, ctx:OPLangParser.Attr_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#attr_modifier.
    def visitAttr_modifier(self, ctx:OPLangParser.Attr_modifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ne_cm_asgn_id_list.
    def visitNe_cm_asgn_id_list(self, ctx:OPLangParser.Ne_cm_asgn_id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#asgn_id.
    def visitAsgn_id(self, ctx:OPLangParser.Asgn_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#asgn_expr.
    def visitAsgn_expr(self, ctx:OPLangParser.Asgn_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#method_decl.
    def visitMethod_decl(self, ctx:OPLangParser.Method_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#method_modifier.
    def visitMethod_modifier(self, ctx:OPLangParser.Method_modifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#sm_param_decl_list.
    def visitSm_param_decl_list(self, ctx:OPLangParser.Sm_param_decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ne_sm_param_decl_list.
    def visitNe_sm_param_decl_list(self, ctx:OPLangParser.Ne_sm_param_decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#param_decl.
    def visitParam_decl(self, ctx:OPLangParser.Param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ne_cm_id_list.
    def visitNe_cm_id_list(self, ctx:OPLangParser.Ne_cm_id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#constructor_decl.
    def visitConstructor_decl(self, ctx:OPLangParser.Constructor_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#default_constructor_decl.
    def visitDefault_constructor_decl(self, ctx:OPLangParser.Default_constructor_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#copy_constructor_decl.
    def visitCopy_constructor_decl(self, ctx:OPLangParser.Copy_constructor_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#user_constructor_decl.
    def visitUser_constructor_decl(self, ctx:OPLangParser.User_constructor_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#destructor_decl.
    def visitDestructor_decl(self, ctx:OPLangParser.Destructor_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#dtype.
    def visitDtype(self, ctx:OPLangParser.DtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ptype.
    def visitPtype(self, ctx:OPLangParser.PtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#atype.
    def visitAtype(self, ctx:OPLangParser.AtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ctype.
    def visitCtype(self, ctx:OPLangParser.CtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#rtype.
    def visitRtype(self, ctx:OPLangParser.RtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#expr.
    def visitExpr(self, ctx:OPLangParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#gtexpr.
    def visitGtexpr(self, ctx:OPLangParser.GtexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#eqexpr.
    def visitEqexpr(self, ctx:OPLangParser.EqexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#lgexpr.
    def visitLgexpr(self, ctx:OPLangParser.LgexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#addexpr.
    def visitAddexpr(self, ctx:OPLangParser.AddexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#mulexpr.
    def visitMulexpr(self, ctx:OPLangParser.MulexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#conexpr.
    def visitConexpr(self, ctx:OPLangParser.ConexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#notexpr.
    def visitNotexpr(self, ctx:OPLangParser.NotexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#uniexpr.
    def visitUniexpr(self, ctx:OPLangParser.UniexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#idxexpr.
    def visitIdxexpr(self, ctx:OPLangParser.IdxexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#newexpr.
    def visitNewexpr(self, ctx:OPLangParser.NewexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#parexpr.
    def visitParexpr(self, ctx:OPLangParser.ParexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#callargs.
    def visitCallargs(self, ctx:OPLangParser.CallargsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#cm_expr_list.
    def visitCm_expr_list(self, ctx:OPLangParser.Cm_expr_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ne_cm_expr_list.
    def visitNe_cm_expr_list(self, ctx:OPLangParser.Ne_cm_expr_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#lit.
    def visitLit(self, ctx:OPLangParser.LitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#plit.
    def visitPlit(self, ctx:OPLangParser.PlitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#alit.
    def visitAlit(self, ctx:OPLangParser.AlitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ne_cm_plit_list.
    def visitNe_cm_plit_list(self, ctx:OPLangParser.Ne_cm_plit_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#stmt.
    def visitStmt(self, ctx:OPLangParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#other_stmt.
    def visitOther_stmt(self, ctx:OPLangParser.Other_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#block_stmt.
    def visitBlock_stmt(self, ctx:OPLangParser.Block_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#vardecl_list.
    def visitVardecl_list(self, ctx:OPLangParser.Vardecl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#vardecl.
    def visitVardecl(self, ctx:OPLangParser.VardeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#var_modifier.
    def visitVar_modifier(self, ctx:OPLangParser.Var_modifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#stmt_list.
    def visitStmt_list(self, ctx:OPLangParser.Stmt_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#asgn_stmt.
    def visitAsgn_stmt(self, ctx:OPLangParser.Asgn_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#asgnlhs.
    def visitAsgnlhs(self, ctx:OPLangParser.AsgnlhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#match_stmt.
    def visitMatch_stmt(self, ctx:OPLangParser.Match_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#open_stmt.
    def visitOpen_stmt(self, ctx:OPLangParser.Open_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#for_stmt.
    def visitFor_stmt(self, ctx:OPLangParser.For_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#break_stmt.
    def visitBreak_stmt(self, ctx:OPLangParser.Break_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#cont_stmt.
    def visitCont_stmt(self, ctx:OPLangParser.Cont_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#ret_stmt.
    def visitRet_stmt(self, ctx:OPLangParser.Ret_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OPLangParser#invk_stmt.
    def visitInvk_stmt(self, ctx:OPLangParser.Invk_stmtContext):
        return self.visitChildren(ctx)
