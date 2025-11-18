"""
Unit tests for the EigenScript lexer.

Tests tokenization of EigenScript source code.
"""

import pytest
from eigenscript.lexer import Tokenizer, Token, TokenType


class TestTokenizer:
    """Test suite for the Tokenizer class."""

    def test_tokenizer_initialization(self):
        """Tokenizer should initialize with source code."""
        source = "x is 5"
        tokenizer = Tokenizer(source)
        assert tokenizer.source == source
        assert tokenizer.position == 0
        assert tokenizer.line == 1
        assert tokenizer.column == 1

    def test_empty_source(self):
        """Empty source should produce only EOF token."""
        tokenizer = Tokenizer("")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_of_operator_tokenization(self):
        """OF operator should be recognized as lightlike token."""
        tokenizer = Tokenizer("x of y")
        tokens = tokenizer.tokenize()

        assert len(tokens) == 4  # IDENTIFIER, OF, IDENTIFIER, EOF
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "x"
        assert tokens[1].type == TokenType.OF
        assert tokens[2].type == TokenType.IDENTIFIER
        assert tokens[2].value == "y"
        assert tokens[3].type == TokenType.EOF

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_is_operator_tokenization(self):
        """IS operator should be recognized."""
        tokenizer = Tokenizer("x is 5")
        tokens = tokenizer.tokenize()

        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[1].type == TokenType.IS
        assert tokens[2].type == TokenType.NUMBER
        assert tokens[2].value == 5

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_number_literals(self):
        """Number literals should be tokenized correctly."""
        test_cases = [
            ("42", 42),
            ("3.14", 3.14),
            ("-17", -17),
            ("0.001", 0.001),
        ]

        for source, expected_value in test_cases:
            tokenizer = Tokenizer(source)
            tokens = tokenizer.tokenize()
            assert tokens[0].type == TokenType.NUMBER
            assert tokens[0].value == expected_value

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_string_literals(self):
        """String literals should be tokenized correctly."""
        test_cases = [
            ('"hello"', "hello"),
            ("'world'", "world"),
            ('"EigenScript"', "EigenScript"),
        ]

        for source, expected_value in test_cases:
            tokenizer = Tokenizer(source)
            tokens = tokenizer.tokenize()
            assert tokens[0].type == TokenType.STRING
            assert tokens[0].value == expected_value

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_keywords(self):
        """Keywords should be recognized."""
        keywords = ["of", "is", "if", "else", "loop", "while", "define", "as", "return"]

        for keyword in keywords:
            tokenizer = Tokenizer(keyword)
            tokens = tokenizer.tokenize()
            assert tokens[0].type == TokenType[keyword.upper()]

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_identifiers_vs_keywords(self):
        """Identifiers should be distinguished from keywords."""
        tokenizer = Tokenizer("offset")  # Contains 'of' but is identifier
        tokens = tokenizer.tokenize()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "offset"

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_vector_literals(self):
        """Vector literals should be tokenized."""
        tokenizer = Tokenizer("(1, 2, 3)")
        tokens = tokenizer.tokenize()
        # Should recognize as vector or as LPAREN, numbers, commas, RPAREN
        # Implementation detail TBD

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_comments(self):
        """Comments should be ignored."""
        tokenizer = Tokenizer("x is 5  # This is a comment")
        tokens = tokenizer.tokenize()

        # Should only have: IDENTIFIER, IS, NUMBER, EOF
        # Comment should be skipped
        assert len([t for t in tokens if t.type != TokenType.EOF]) == 3

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_indentation_tracking(self):
        """Indentation should produce INDENT/DEDENT tokens."""
        source = """if x:
    y is 5
    z is 10
done"""
        tokenizer = Tokenizer(source)
        tokens = tokenizer.tokenize()

        # Should have INDENT and DEDENT tokens
        indent_tokens = [t for t in tokens if t.type == TokenType.INDENT]
        dedent_tokens = [t for t in tokens if t.type == TokenType.DEDENT]

        assert len(indent_tokens) > 0
        assert len(dedent_tokens) > 0

    @pytest.mark.skip(reason="Lexer implementation pending")
    def test_nested_of_expressions(self):
        """Nested OF expressions should tokenize correctly."""
        tokenizer = Tokenizer("owner of (engine of car)")
        tokens = tokenizer.tokenize()

        # Should have proper nesting with parentheses
        of_tokens = [t for t in tokens if t.type == TokenType.OF]
        assert len(of_tokens) == 2


class TestToken:
    """Test suite for the Token class."""

    def test_token_creation(self):
        """Token should be created with type and value."""
        token = Token(TokenType.NUMBER, value=42, line=1, column=5)
        assert token.type == TokenType.NUMBER
        assert token.value == 42
        assert token.line == 1
        assert token.column == 5

    def test_token_repr(self):
        """Token should have readable string representation."""
        token = Token(TokenType.IDENTIFIER, value="x", line=1, column=1)
        repr_str = repr(token)
        assert "IDENTIFIER" in repr_str
        assert "x" in repr_str
