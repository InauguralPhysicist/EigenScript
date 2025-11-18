"""
Parser module for EigenScript.

This module handles parsing of token streams into Abstract Syntax Trees (AST).
"""

from eigenscript.parser.ast_builder import (
    Parser,
    ASTNode,
    Assignment,
    Relation,
    Conditional,
    Loop,
    FunctionDef,
    Return,
    Literal,
    Identifier,
)

__all__ = [
    "Parser",
    "ASTNode",
    "Assignment",
    "Relation",
    "Conditional",
    "Loop",
    "FunctionDef",
    "Return",
    "Literal",
    "Identifier",
]
