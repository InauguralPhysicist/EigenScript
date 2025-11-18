"""
Tokenizer for EigenScript.

Converts source code text into a stream of tokens.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Any


class TokenType(Enum):
    """Token types for EigenScript."""

    # Keywords
    OF = "OF"
    IS = "IS"
    IF = "IF"
    ELSE = "ELSE"
    LOOP = "LOOP"
    WHILE = "WHILE"
    DEFINE = "DEFINE"
    AS = "AS"
    RETURN = "RETURN"
    BREAK = "BREAK"
    NULL = "NULL"

    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    VECTOR = "VECTOR"
    IDENTIFIER = "IDENTIFIER"

    # Operators and Punctuation
    COLON = "COLON"
    COMMA = "COMMA"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"

    # Whitespace (significant in Python-style indentation)
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"

    # Special
    EOF = "EOF"


@dataclass
class Token:
    """
    Represents a single token in the source code.

    Attributes:
        type: The type of token (from TokenType enum)
        value: The actual value of the token (if applicable)
        line: Line number where token appears
        column: Column number where token starts
    """

    type: TokenType
    value: Any = None
    line: int = 0
    column: int = 0

    def __repr__(self) -> str:
        if self.value is not None:
            return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"
        return f"Token({self.type.name}, {self.line}:{self.column})"


class Tokenizer:
    """
    Tokenizes EigenScript source code.

    This lexer converts raw source text into a stream of tokens
    that can be parsed into an Abstract Syntax Tree (AST).

    Example:
        >>> tokenizer = Tokenizer("x is 5")
        >>> tokens = tokenizer.tokenize()
        >>> print(tokens)
        [Token(IDENTIFIER, 'x'), Token(IS), Token(NUMBER, 5), Token(EOF)]
    """

    # Keywords mapping
    KEYWORDS = {
        "of": TokenType.OF,
        "is": TokenType.IS,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "loop": TokenType.LOOP,
        "while": TokenType.WHILE,
        "define": TokenType.DEFINE,
        "as": TokenType.AS,
        "return": TokenType.RETURN,
        "break": TokenType.BREAK,
        "null": TokenType.NULL,
    }

    def __init__(self, source: str):
        """
        Initialize the tokenizer with source code.

        Args:
            source: EigenScript source code as string
        """
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

        # For tracking indentation (Python-style)
        self.indent_stack = [0]

    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.

        Returns:
            List of tokens including EOF token at the end

        Raises:
            SyntaxError: If invalid syntax is encountered
        """
        # TODO: Implement tokenization logic
        # For now, return empty list with EOF
        self.tokens.append(Token(TokenType.EOF, line=self.line, column=self.column))
        return self.tokens

    def current_char(self) -> Optional[str]:
        """Get current character without advancing."""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at character ahead without advancing."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def advance(self) -> Optional[str]:
        """Advance position and return current character."""
        if self.position >= len(self.source):
            return None

        char = self.source[self.position]
        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def skip_whitespace(self):
        """Skip whitespace except newlines (which are significant)."""
        while self.current_char() and self.current_char() in " \t\r":
            self.advance()

    def skip_comment(self):
        """Skip single-line comments starting with #."""
        if self.current_char() == "#":
            while self.current_char() and self.current_char() != "\n":
                self.advance()

    def read_number(self) -> Token:
        """
        Read a number literal (integer or float).

        Returns:
            Token with NUMBER type and numeric value
        """
        # TODO: Implement number reading
        # Should handle: 42, 3.14, -17, etc.
        pass

    def read_string(self) -> Token:
        """
        Read a string literal.

        Returns:
            Token with STRING type and string value
        """
        # TODO: Implement string reading
        # Should handle: "hello", 'world', escape sequences
        pass

    def read_identifier(self) -> Token:
        """
        Read an identifier or keyword.

        Returns:
            Token with IDENTIFIER or keyword type
        """
        # TODO: Implement identifier reading
        # Should recognize keywords vs identifiers
        pass

    def read_vector(self) -> Token:
        """
        Read a vector literal like (1, 2, 3).

        Returns:
            Token with VECTOR type and list value
        """
        # TODO: Implement vector reading
        # Should handle: (1, 2, 3), (1.0, -2.5, 3.14)
        pass

    def handle_indentation(self):
        """
        Handle indentation-based block structure.

        Emits INDENT and DEDENT tokens similar to Python.
        """
        # TODO: Implement indentation handling
        # Track indent levels and emit INDENT/DEDENT tokens
        pass
