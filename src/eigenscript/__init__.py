"""
EigenScript: A geometric programming language modeling computation
as flow in semantic spacetime.

This package contains the core interpreter and runtime for EigenScript.
"""

__version__ = "0.1.0-alpha"
__author__ = "EigenScript Contributors"

from eigenscript.lexer import Tokenizer, Token, TokenType
from eigenscript.parser import Parser, ASTNode
from eigenscript.evaluator import Interpreter

__all__ = [
    "Tokenizer",
    "Token",
    "TokenType",
    "Parser",
    "ASTNode",
    "Interpreter",
]
