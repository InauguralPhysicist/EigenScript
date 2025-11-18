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
class BinaryOp(ASTNode):
    """
    Represents binary arithmetic operations (+, -, *, /, =, <, >).

    Semantic: Arithmetic operators as equilibrium operations:
        + = additive equilibrium (composition)
        - = subtractive equilibrium (inversion)
        * = multiplicative equilibrium (scaling)
        / = projected multiplicative equilibrium (ratio)
        = = equality equilibrium (IS test)
        < = proximity to equilibrium test
        > = distance from equilibrium test

    Example:
        a + b
        x * 2
        count < 10
    """

    left: ASTNode
    operator: str  # "+", "-", "*", "/", "=", "<", ">"
    right: ASTNode

    def __repr__(self) -> str:
        return f"BinaryOp({self.left}, {self.operator!r}, {self.right})"


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
class Interrogative(ASTNode):
    """
    Represents an interrogative operator (WHO, WHAT, WHEN, WHERE, WHY, HOW).

    These extract geometric information from expressions:
    - WHO: Identity/entity projection
    - WHAT: Scalar magnitude (r = √I)
    - WHEN: Temporal/iteration coordinate
    - WHERE: Spatial position in semantic space
    - WHY: Causal direction (gradient)
    - HOW: Transformation/process

    Example:
        what is x
        why is change
        how is convergence
    """

    interrogative: str  # "who", "what", "when", "where", "why", "how"
    expression: ASTNode

    def __repr__(self) -> str:
        return f"Interrogative({self.interrogative!r}, {self.expression})"


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
        statements = []

        while self.current_token() and self.current_token().type != TokenType.EOF:
            # Skip newlines at the top level
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue

            # Parse statement
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

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
        token = self.current_token()

        if not token or token.type == TokenType.EOF:
            return None

        # Skip newlines
        if token.type == TokenType.NEWLINE:
            self.advance()
            return None

        # DEFINE - function definition
        if token.type == TokenType.DEFINE:
            return self.parse_definition()

        # IF - conditional
        if token.type == TokenType.IF:
            return self.parse_conditional()

        # LOOP - loop statement
        if token.type == TokenType.LOOP:
            return self.parse_loop()

        # RETURN - return statement
        if token.type == TokenType.RETURN:
            return self.parse_return()

        # BREAK - break statement
        if token.type == TokenType.BREAK:
            self.advance()
            # Consume optional newline
            if self.current_token() and self.current_token().type == TokenType.NEWLINE:
                self.advance()
            return Break()

        # Assignment (identifier IS expression)
        if token.type == TokenType.IDENTIFIER:
            # Look ahead for IS token
            next_token = self.peek_token()
            if next_token and next_token.type == TokenType.IS:
                return self.parse_assignment()

        # Expression statement (e.g., function call)
        expr = self.parse_expression()

        # Consume optional newline after expression
        if self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()

        return expr

    def parse_assignment(self) -> Assignment:
        """
        Parse an assignment statement.

        Grammar: identifier IS expression
        """
        # Get identifier
        id_token = self.expect(TokenType.IDENTIFIER)
        identifier = id_token.value

        # Expect IS token
        self.expect(TokenType.IS)

        # Parse expression
        expression = self.parse_expression()

        # Consume optional newline
        if self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()

        return Assignment(identifier, expression)

    def parse_definition(self) -> FunctionDef:
        """
        Parse a function definition.

        Grammar: DEFINE identifier AS COLON block
        """
        # Consume DEFINE
        self.expect(TokenType.DEFINE)

        # Get function name
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value

        # For now, we don't parse parameters (simplified)
        # In full implementation: parse parameter list
        parameters = []

        # Expect AS (optional in some grammars, required here)
        if self.current_token() and self.current_token().type == TokenType.AS:
            self.advance()

        # Expect colon
        self.expect(TokenType.COLON)

        # Consume newline
        if self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()

        # Parse block
        body = self.parse_block()

        return FunctionDef(name, parameters, body)

    def parse_conditional(self) -> Conditional:
        """
        Parse an IF statement.

        Grammar: IF expression COLON block (ELSE COLON block)?
        """
        # Consume IF
        self.expect(TokenType.IF)

        # Parse condition
        condition = self.parse_expression()

        # Expect colon
        self.expect(TokenType.COLON)

        # Consume newline
        if self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()

        # Parse if block
        if_block = self.parse_block()

        # Check for ELSE
        else_block = None
        if self.current_token() and self.current_token().type == TokenType.ELSE:
            self.advance()

            # Expect colon
            self.expect(TokenType.COLON)

            # Consume newline
            if self.current_token() and self.current_token().type == TokenType.NEWLINE:
                self.advance()

            # Parse else block
            else_block = self.parse_block()

        return Conditional(condition, if_block, else_block)

    def parse_loop(self) -> Loop:
        """
        Parse a LOOP statement.

        Grammar: LOOP WHILE expression COLON block
        """
        # Consume LOOP
        self.expect(TokenType.LOOP)

        # Expect WHILE
        self.expect(TokenType.WHILE)

        # Parse condition
        condition = self.parse_expression()

        # Expect colon
        self.expect(TokenType.COLON)

        # Consume newline
        if self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()

        # Parse loop body
        body = self.parse_block()

        return Loop(condition, body)

    def parse_return(self) -> Return:
        """
        Parse a RETURN statement.

        Grammar: RETURN expression
        """
        # Consume RETURN
        self.expect(TokenType.RETURN)

        # Parse expression
        expression = self.parse_expression()

        # Consume optional newline
        if self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()

        return Return(expression)

    def parse_interrogative(self) -> Interrogative:
        """
        Parse an interrogative operator.

        Grammar: (WHO | WHAT | WHEN | WHERE | WHY | HOW) (IS)? primary

        Example:
            what x
            what is x  (IS is optional and ignored)
            why convergence
        """
        # Get interrogative type
        token = self.current_token()
        interrogative_map = {
            TokenType.WHO: "who",
            TokenType.WHAT: "what",
            TokenType.WHEN: "when",
            TokenType.WHERE: "where",
            TokenType.WHY: "why",
            TokenType.HOW: "how",
        }
        interrogative = interrogative_map[token.type]
        self.advance()

        # IS is optional after interrogatives (for natural language feel)
        if self.current_token() and self.current_token().type == TokenType.IS:
            self.advance()

        # Parse a primary expression (identifier, literal, etc)
        # This avoids infinite recursion since primary won't parse interrogatives
        expression = self.parse_identifier_or_literal()

        return Interrogative(interrogative, expression)

    def parse_identifier_or_literal(self) -> ASTNode:
        """
        Parse just an identifier or literal (for interrogatives).

        This is a subset of parse_primary that doesn't handle interrogatives.
        """
        token = self.current_token()

        if not token:
            raise SyntaxError("Unexpected end of input")

        # Number literal
        if token.type == TokenType.NUMBER:
            self.advance()
            return Literal(token.value, "number")

        # String literal
        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value, "string")

        # Null literal
        if token.type == TokenType.NULL:
            self.advance()
            return Literal(None, "null")

        # Identifier
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value)

        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        raise SyntaxError(
            f"Expected identifier or literal, got {token.type.name} at line {token.line}, column {token.column}"
        )

    def parse_block(self) -> List[ASTNode]:
        """
        Parse an indented block of statements.

        Returns:
            List of AST nodes in the block
        """
        statements = []

        # Expect INDENT
        self.expect(TokenType.INDENT)

        # Parse statements until DEDENT
        while self.current_token() and self.current_token().type != TokenType.DEDENT:
            # Skip newlines
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue

            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        # Expect DEDENT
        self.expect(TokenType.DEDENT)

        return statements

    def parse_expression(self) -> ASTNode:
        """
        Parse an expression.

        This handles operator precedence and expression composition.
        Precedence (lowest to highest):
        1. Comparison (=, <, >)
        2. Addition/Subtraction (+, -)
        3. Multiplication/Division (*, /)
        4. OF operator
        5. Primary (literals, identifiers, parens)
        """
        return self.parse_comparison()

    def parse_comparison(self) -> ASTNode:
        """
        Parse comparison operators (=, <, >).

        Grammar: additive ((EQUALS | LESS_THAN | GREATER_THAN) additive)*
        """
        left = self.parse_additive()

        while self.current_token() and self.current_token().type in (
            TokenType.EQUALS,
            TokenType.LESS_THAN,
            TokenType.GREATER_THAN,
        ):
            op_token = self.current_token()
            self.advance()

            right = self.parse_additive()

            op_map = {
                TokenType.EQUALS: "=",
                TokenType.LESS_THAN: "<",
                TokenType.GREATER_THAN: ">",
            }
            left = BinaryOp(left, op_map[op_token.type], right)

        return left

    def parse_additive(self) -> ASTNode:
        """
        Parse addition and subtraction operators (+, -).

        Grammar: multiplicative ((PLUS | MINUS) multiplicative)*
        """
        left = self.parse_multiplicative()

        while self.current_token() and self.current_token().type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            op_token = self.current_token()
            self.advance()

            right = self.parse_multiplicative()

            op_map = {TokenType.PLUS: "+", TokenType.MINUS: "-"}
            left = BinaryOp(left, op_map[op_token.type], right)

        return left

    def parse_multiplicative(self) -> ASTNode:
        """
        Parse multiplication and division operators (*, /).

        Grammar: relation ((MULTIPLY | DIVIDE) relation)*
        """
        left = self.parse_relation()

        while self.current_token() and self.current_token().type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            op_token = self.current_token()
            self.advance()

            right = self.parse_relation()

            op_map = {TokenType.MULTIPLY: "*", TokenType.DIVIDE: "/"}
            left = BinaryOp(left, op_map[op_token.type], right)

        return left

    def parse_relation(self) -> ASTNode:
        """
        Parse a relation (OF operator).

        Grammar: primary (OF primary)*

        The OF operator is right-associative:
        a of b of c → a of (b of c)
        """
        # Start with primary expression
        left = self.parse_primary()

        # Handle OF operator (right-associative)
        if self.current_token() and self.current_token().type == TokenType.OF:
            self.advance()
            # Recursively parse right side to handle right-associativity
            right = self.parse_relation()
            return Relation(left, right)

        return left

    def parse_primary(self) -> ASTNode:
        """
        Parse a primary expression (literal, identifier, parenthesized expression, interrogative).

        Grammar: NUMBER | STRING | VECTOR | IDENTIFIER | LPAREN expression RPAREN | interrogative
        """
        token = self.current_token()

        if not token:
            raise SyntaxError("Unexpected end of input")

        # Interrogative operators
        if token.type in (TokenType.WHO, TokenType.WHAT, TokenType.WHEN,
                         TokenType.WHERE, TokenType.WHY, TokenType.HOW):
            return self.parse_interrogative()

        # Number literal
        if token.type == TokenType.NUMBER:
            self.advance()
            return Literal(token.value, "number")

        # String literal
        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value, "string")

        # Null literal
        if token.type == TokenType.NULL:
            self.advance()
            return Literal(None, "null")

        # Identifier
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value)

        # Parenthesized expression or vector literal
        if token.type == TokenType.LPAREN:
            self.advance()

            # Check if it's a vector literal (1, 2, 3)
            # or a parenthesized expression (x of y)
            elements = []
            while self.current_token() and self.current_token().type != TokenType.RPAREN:
                elements.append(self.parse_expression())

                # Check for comma (vector literal)
                if self.current_token() and self.current_token().type == TokenType.COMMA:
                    self.advance()
                elif self.current_token() and self.current_token().type != TokenType.RPAREN:
                    # Single expression in parens
                    break

            self.expect(TokenType.RPAREN)

            # If we have multiple elements or saw a comma, it's a vector
            if len(elements) > 1:
                # Extract numeric values if all are literals
                values = []
                for elem in elements:
                    if isinstance(elem, Literal) and elem.literal_type == "number":
                        values.append(elem.value)
                    else:
                        # Mixed types - keep as list of AST nodes
                        return Literal(elements, "vector")
                return Literal(values, "vector")
            elif len(elements) == 1:
                # Single element in parentheses
                return elements[0]
            else:
                # Empty parentheses - treat as empty vector
                return Literal([], "vector")

        # Bracket notation for vectors
        if token.type == TokenType.LBRACKET:
            self.advance()
            elements = []

            while self.current_token() and self.current_token().type != TokenType.RBRACKET:
                elements.append(self.parse_expression())

                if self.current_token() and self.current_token().type == TokenType.COMMA:
                    self.advance()

            self.expect(TokenType.RBRACKET)

            # Extract values
            values = []
            for elem in elements:
                if isinstance(elem, Literal) and elem.literal_type == "number":
                    values.append(elem.value)
                else:
                    return Literal(elements, "vector")
            return Literal(values, "vector")

        raise SyntaxError(
            f"Unexpected token {token.type.name} at line {token.line}, column {token.column}"
        )
