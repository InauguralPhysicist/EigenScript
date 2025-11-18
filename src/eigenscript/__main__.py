"""
Main entry point for EigenScript interpreter.

Run as: python -m eigenscript [file.eigs]
"""

import sys
import argparse
from pathlib import Path


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

        print(f"EigenScript interpreter (Phase 1 - Minimal Core)")
        print(f"File: {args.file}")
        print("\nNote: Full interpreter not yet implemented.")
        print("This is a placeholder for the future implementation.")
        return 0
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
