"""
Abstract Syntax Tree (AST) builder for EigenScript.

Defines AST node classes and the parser that builds them from tokens.
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from eigenscript.lexer import Token, TokenType


# ============================================================================
# AST Node Classes
# ============================================================================


class ASTNode:
    """Base class for all AST nodes."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


@dataclass
class Literal(ASTNode):
    """
    Represents a literal value (number, string, vector, null).

    Example:
        42, "hello", (1, 2, 3), null
    """

    value: Any
    literal_type: str  # "number", "string", "vector", "null"

    def __repr__(self) -> str:
        return f"Literal({self.value!r}, {self.literal_type})"


@dataclass
class Identifier(ASTNode):
    """
    Represents a variable identifier.

    Example:
        x, my_variable, position
    """

    name: str

    def __repr__(self) -> str:
        return f"Identifier({self.name!r})"


@dataclass
class Relation(ASTNode):
    """
    Represents the OF operator (relational operation).

    Semantic: x of y → x^T g y (metric contraction)

    Example:
        engine of car
        parent of child
    """

    left: ASTNode
    right: ASTNode

    def __repr__(self) -> str:
        return f"Relation({self.left}, {self.right})"


@dataclass
class Assignment(ASTNode):
    """
    Represents the IS operator (identity/binding).

    Semantic: x is y → v_x ← v_y (projection in LRVM space)

    Example:
        position is (3, 4, 0)
        name is "Alice"
    """

    identifier: str
    expression: ASTNode

    def __repr__(self) -> str:
        return f"Assignment({self.identifier!r}, {self.expression})"


@dataclass
class Conditional(ASTNode):
    """
    Represents an IF statement (geometric conditional).

    Semantic: Branch based on norm signature of condition

    Example:
        if temperature of greater_than of 80:
            print of "Hot!"
        else:
            print of "Pleasant"
    """

    condition: ASTNode
    if_block: List[ASTNode]
    else_block: Optional[List[ASTNode]] = None

    def __repr__(self) -> str:
        return f"Conditional({self.condition}, if={len(self.if_block)}, else={len(self.else_block) if self.else_block else 0})"


@dataclass
class Loop(ASTNode):
    """
    Represents a LOOP statement (geodesic iteration).

    Semantic: Iterate until convergence in LRVM space

    Example:
        loop while count of less_than of 10:
            print of count
            count is count of add of 1
    """

    condition: ASTNode
    body: List[ASTNode]

    def __repr__(self) -> str:
        return f"Loop({self.condition}, body={len(self.body)})"


@dataclass
class FunctionDef(ASTNode):
    """
    Represents a function definition (timelike transformation).

    Semantic: Creates timelike transformation in LRVM

    Example:
        define factorial as:
            if n is 0:
                return 1
            else:
                return n of multiply of (factorial of (n of subtract of 1))
    """

    name: str
    parameters: List[str]
    body: List[ASTNode]

    def __repr__(self) -> str:
        return f"FunctionDef({self.name!r}, params={self.parameters}, body={len(self.body)})"


@dataclass
class Return(ASTNode):
    """
    Represents a RETURN statement (flow termination).

    Semantic: Project onto observer frame

    Example:
        return result
    """

    expression: ASTNode

    def __repr__(self) -> str:
        return f"Return({self.expression})"


@dataclass
class Break(ASTNode):
    """
    Represents a BREAK statement (loop termination).

    Example:
        break
    """

    def __repr__(self) -> str:
        return "Break()"


@dataclass
class Program(ASTNode):
    """
    Represents a complete EigenScript program.

    Contains a list of top-level statements.
    """

    statements: List[ASTNode]

    def __repr__(self) -> str:
        return f"Program({len(self.statements)} statements)"


# ============================================================================
# Parser
# ============================================================================


class Parser:
    """
    Recursive descent parser for EigenScript.

    Converts a token stream into an Abstract Syntax Tree (AST).

    Example:
        >>> from eigenscript.lexer import Tokenizer
        >>> tokenizer = Tokenizer("x is 5")
        >>> tokens = tokenizer.tokenize()
        >>> parser = Parser(tokens)
        >>> ast = parser.parse()
    """

    def __init__(self, tokens: List[Token]):
        """
        Initialize parser with token stream.

        Args:
            tokens: List of tokens from the lexer
        """
        self.tokens = tokens
        self.position = 0

    def parse(self) -> Program:
        """
        Parse the token stream into an AST.

        Returns:
            Program node containing all statements

        Raises:
            SyntaxError: If invalid syntax is encountered
        """
        # TODO: Implement parsing logic
        statements = []
        # For now, return empty program
        return Program(statements)

    def current_token(self) -> Optional[Token]:
        """Get current token without advancing."""
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek at token ahead without advancing."""
        pos = self.position + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]

    def advance(self) -> Token:
        """Advance to next token and return current."""
        token = self.current_token()
        if token:
            self.position += 1
        return token

    def expect(self, token_type: TokenType) -> Token:
        """
        Expect a specific token type and advance.

        Args:
            token_type: Expected token type

        Returns:
            The matched token

        Raises:
            SyntaxError: If current token doesn't match expected type
        """
        token = self.current_token()
        if not token or token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type.name}, got {token.type.name if token else 'EOF'}"
            )
        return self.advance()

    def parse_statement(self) -> Optional[ASTNode]:
        """
        Parse a single statement.

        Returns:
            AST node representing the statement
        """
        # TODO: Implement statement parsing
        # Dispatch to appropriate parse method based on token
        pass

    def parse_assignment(self) -> Assignment:
        """
        Parse an assignment statement.

        Grammar: identifier IS expression
        """
        # TODO: Implement assignment parsing
        pass

    def parse_definition(self) -> FunctionDef:
        """
        Parse a function definition.

        Grammar: DEFINE identifier AS COLON block
        """
        # TODO: Implement function definition parsing
        pass

    def parse_conditional(self) -> Conditional:
        """
        Parse an IF statement.

        Grammar: IF expression COLON block (ELSE COLON block)?
        """
        # TODO: Implement conditional parsing
        pass

    def parse_loop(self) -> Loop:
        """
        Parse a LOOP statement.

        Grammar: LOOP WHILE expression COLON block
        """
        # TODO: Implement loop parsing
        pass

    def parse_return(self) -> Return:
        """
        Parse a RETURN statement.

        Grammar: RETURN expression
        """
        # TODO: Implement return parsing
        pass

    def parse_expression(self) -> ASTNode:
        """
        Parse an expression.

        This handles operator precedence and expression composition.
        """
        # TODO: Implement expression parsing
        # Handle OF operator, function calls, etc.
        pass

    def parse_relation(self) -> ASTNode:
        """
        Parse a relation (OF operator).

        Grammar: expression OF expression
        """
        # TODO: Implement relation parsing
        pass

    def parse_primary(self) -> ASTNode:
        """
        Parse a primary expression (literal, identifier, parenthesized expression).

        Grammar: NUMBER | STRING | VECTOR | IDENTIFIER | LPAREN expression RPAREN
        """
        # TODO: Implement primary expression parsing
        pass
