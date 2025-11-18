"""
Unit tests for the EigenScript parser.

Tests AST construction from token streams.
"""

import pytest
from eigenscript.lexer import Token, TokenType
from eigenscript.parser import Parser, Assignment, Relation, Literal, Identifier


class TestParser:
    """Test suite for the Parser class."""

    def test_parser_initialization(self):
        """Parser should initialize with token list."""
        tokens = [Token(TokenType.EOF)]
        parser = Parser(tokens)
        assert parser.tokens == tokens
        assert parser.position == 0

    def test_empty_program(self):
        """Empty token stream should produce empty program."""
        tokens = [Token(TokenType.EOF)]
        parser = Parser(tokens)
        program = parser.parse()
        assert len(program.statements) == 0

    @pytest.mark.skip(reason="Parser implementation pending")
    def test_parse_assignment(self):
        """Should parse assignment statement."""
        # x is 5
        tokens = [
            Token(TokenType.IDENTIFIER, value="x"),
            Token(TokenType.IS),
            Token(TokenType.NUMBER, value=5),
            Token(TokenType.EOF),
        ]

        parser = Parser(tokens)
        program = parser.parse()

        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, Assignment)
        assert stmt.identifier == "x"
        assert isinstance(stmt.expression, Literal)
        assert stmt.expression.value == 5

    @pytest.mark.skip(reason="Parser implementation pending")
    def test_parse_relation(self):
        """Should parse OF relation."""
        # engine of car
        tokens = [
            Token(TokenType.IDENTIFIER, value="engine"),
            Token(TokenType.OF),
            Token(TokenType.IDENTIFIER, value="car"),
            Token(TokenType.EOF),
        ]

        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert isinstance(stmt, Relation)
        assert isinstance(stmt.left, Identifier)
        assert stmt.left.name == "engine"
        assert isinstance(stmt.right, Identifier)
        assert stmt.right.name == "car"

    @pytest.mark.skip(reason="Parser implementation pending")
    def test_parse_nested_relation(self):
        """Should parse nested OF expressions."""
        # owner of (engine of car)
        tokens = [
            Token(TokenType.IDENTIFIER, value="owner"),
            Token(TokenType.OF),
            Token(TokenType.LPAREN),
            Token(TokenType.IDENTIFIER, value="engine"),
            Token(TokenType.OF),
            Token(TokenType.IDENTIFIER, value="car"),
            Token(TokenType.RPAREN),
            Token(TokenType.EOF),
        ]

        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert isinstance(stmt, Relation)
        # Left should be "owner"
        assert isinstance(stmt.left, Identifier)
        # Right should be another Relation
        assert isinstance(stmt.right, Relation)

    @pytest.mark.skip(reason="Parser implementation pending")
    def test_parse_conditional(self):
        """Should parse IF statement."""
        # if x:
        #     y is 5
        # Not testing full indentation handling yet
        pass

    @pytest.mark.skip(reason="Parser implementation pending")
    def test_parse_loop(self):
        """Should parse LOOP statement."""
        pass

    @pytest.mark.skip(reason="Parser implementation pending")
    def test_parse_function_def(self):
        """Should parse function definition."""
        pass


class TestASTNodes:
    """Test suite for AST node classes."""

    def test_literal_node(self):
        """Literal node should store value and type."""
        lit = Literal(value=42, literal_type="number")
        assert lit.value == 42
        assert lit.literal_type == "number"

    def test_identifier_node(self):
        """Identifier node should store name."""
        ident = Identifier(name="x")
        assert ident.name == "x"

    def test_assignment_node(self):
        """Assignment node should store identifier and expression."""
        expr = Literal(value=5, literal_type="number")
        assign = Assignment(identifier="x", expression=expr)
        assert assign.identifier == "x"
        assert assign.expression == expr

    def test_relation_node(self):
        """Relation node should store left and right."""
        left = Identifier(name="engine")
        right = Identifier(name="car")
        rel = Relation(left=left, right=right)
        assert rel.left == left
        assert rel.right == right
