"""
Main entry point for EigenScript interpreter.

Run as: python -m eigenscript [file.eigs]
"""

import sys
import argparse
from pathlib import Path

from eigenscript.lexer import Tokenizer
from eigenscript.parser import Parser
from eigenscript.evaluator import Interpreter


def main():
    """Main entry point for the EigenScript interpreter."""
    parser = argparse.ArgumentParser(
        description="EigenScript: A geometric programming language"
    )
    parser.add_argument(
        "file", nargs="?", help="EigenScript source file (.eigs) to execute"
    )
    parser.add_argument(
        "--version", action="version", version="EigenScript 0.1.0-alpha"
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Start interactive REPL"
    )
    parser.add_argument(
        "--show-fs",
        action="store_true",
        help="Show Framework Strength metrics after execution",
    )

    args = parser.parse_args()

    if args.interactive:
        print("EigenScript REPL (coming soon)")
        print("Interactive mode not yet implemented.")
        return 1

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1

        try:
            # Read source code
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            # Tokenize
            tokenizer = Tokenizer(source)
            tokens = tokenizer.tokenize()

            # Parse
            parser_obj = Parser(tokens)
            ast = parser_obj.parse()

            # Interpret
            interpreter = Interpreter()
            result = interpreter.evaluate(ast)

            # Show metrics if requested
            if args.show_fs:
                fs = interpreter.get_framework_strength()
                signature, classification = interpreter.get_spacetime_signature()
                converged = interpreter.has_converged()
                
                print(f"\n=== Framework Strength Metrics ===")
                print(f"Framework Strength: {fs:.4f}")
                print(f"Converged: {converged}")
                print(f"Spacetime Signature: {signature:.4f} ({classification})")

            return 0

        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
