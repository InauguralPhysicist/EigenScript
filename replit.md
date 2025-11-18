# EigenScript - Replit Project Setup

## Overview
EigenScript is a geometric programming language modeling computation as flow in semantic spacetime. This is a Python-based interpreter for executing `.eigs` files.

## Project Type
- **Language:** Python 3.11
- **Type:** CLI Tool (Command-Line Interpreter)
- **Main Entry Point:** `eigenscript` command (via `python -m eigenscript`)

## Project Structure
```
.
├── src/eigenscript/          # Main source code
│   ├── lexer/                # Tokenization
│   ├── parser/               # AST building
│   ├── evaluator/            # Interpretation engine
│   ├── runtime/              # Runtime systems (eigencontrol, framework strength)
│   ├── semantic/             # LRVM backend, metric tensor, operations
│   └── __main__.py           # CLI entry point
├── tests/                    # Test suite (149 tests, 59% coverage)
├── examples/                 # Sample .eigs programs
├── docs/                     # Documentation
├── pyproject.toml            # Project configuration
└── requirements.txt          # Dependencies
```

## Setup Complete
- ✅ Python 3.11 installed
- ✅ All dependencies installed (numpy, pytest, pytest-cov, black, flake8, mypy, typing-extensions)
- ✅ Package installed in editable mode (`pip install -e .`)
- ✅ All 149 tests passing
- ✅ Workflow configured: "Run Tests" (pytest -v)

## How to Use

### Run the Test Suite
The workflow "Run Tests" automatically runs the test suite. You can also run manually:
```bash
pytest -v
```

### Run the EigenScript Interpreter
```bash
eigenscript examples/hello_world.eigs
```

Or using Python module syntax:
```bash
python -m eigenscript examples/hello_world.eigs
```

### Check Version
```bash
eigenscript --version
```

### Interactive REPL
```bash
eigenscript -i
```

The REPL supports multi-line input for function definitions, conditionals, and loops:
- Lines ending with `:` enter continuation mode (prompt changes to `...`)
- Press Enter on a blank line to complete a multi-line block
- Non-indented lines also complete blocks (dedent detection)

## Development Commands

### Run Tests with Coverage
```bash
pytest -v --cov=eigenscript --cov-report=html
```

### Code Formatting
```bash
black src/
```

### Linting
```bash
flake8 src/
```

### Type Checking
```bash
mypy src/eigenscript/
```

## Current Status
- **Phase:** Phase 4 - List Comprehensions Complete! 🎉
- **Test Coverage:** 62% overall, 267+ passing tests 
- **Turing Complete:** ✅ Yes
- **Core Features Complete:** 
  - ✅ Lexer, Parser, LRVM, Interpreter
  - ✅ Interrogatives (who, what, when, where, why, how)
  - ✅ Semantic Predicates (converged, stable, diverging, oscillating, fs, signature)
  - ✅ Standard Library (print, input, len, type, norm, range)
  - ✅ Interactive REPL with multi-line support
  - ✅ Meta-circular evaluator (proof-of-concept)
  - ✅ Improved error messages
  - ✅ **Full list/array support:**
    - List literals `[1, 2, 3]`
    - List indexing `my_list[0]`
    - List slicing `my_list[1:4]`
    - `range of n` function
    - `len of list` and `type of list` support
    - Manual iteration with index
    - **Advanced list operations (Phase 3):**
      - `append of [list, value]` - add element to end
      - `pop of list` - remove and return last element
      - `min of list` - find minimum value
      - `max of list` - find maximum value
      - `sort of list` - return sorted copy (non-mutating)
  - ✅ **Complete if-then-else:**
    - Equality comparison `if x = 5:`
    - Less than `if x < 10:`
    - Greater than `if x > 20:`
    - Nested conditionals
    - Works with lists and loops
  - ✅ **Logical operators with short-circuit evaluation:**
    - NOT: `not (x = 5)` - logical negation
    - AND: `(x > 5) and (y < 10)` - logical conjunction (short-circuits on false)
    - OR: `(x = 0) or (y = 0)` - logical disjunction (short-circuits on true)
  - ✅ **Extended comparisons:**
    - `<=` less than or equal
    - `>=` greater than or equal
    - `!=` not equal
  - ✅ **Modulo operator:**
    - `%` modulo/remainder: `10 % 3` returns `1`
    - Even/odd checks: `n % 2 = 0`
  - ✅ **String Power (Phase 2):**
    - String concatenation: `"Hello" + " World"`
    - String indexing: `text[0]` get single character
    - String slicing: `text[0:5]`, `text[2:]`, `text[:3]`
    - Built-in functions: `upper of text`, `lower of text`, `split of text`, `join of list`
  - ✅ **Higher-Order Functions (Phase 4A):**
    - `map of [function, list]` - transform each element
    - `filter of [predicate, list]` - select matching elements
    - `reduce of [function, list, initial]` - fold/accumulate to single value
    - Functions maintain geometric semantics (transformation, constraint satisfaction, sequential composition)
    - examples/higher_order_functions.eigs with comprehensive demonstrations
  - ✅ **List Comprehensions (Phase 4B):**
    - Syntax: `[expression for variable in list]` - transform elements
    - With filter: `[expression for variable in list if condition]` - filter and transform
    - Concise alternative to map/filter chains
    - Proper lexical scoping (loop variable doesn't leak)
    - Maintains geometric semantics in LRVM space
    - 19 comprehensive unit tests
    - examples/list_comprehensions.eigs with real-world examples
    - docs/list_comprehensions.md with complete documentation

## Recent Bug Fixes (November 2025)
**Type System & Runtime Safety Improvements:**
- ✅ Fixed critical type system issues by introducing `Value = Union[LRVMVector, EigenList]` type alias
- ✅ Reduced LSP type errors from 84 to 21 (75% reduction)
- ✅ Added runtime type checks preventing AttributeError crashes when lists used with arithmetic operators
- ✅ Fixed unbound variable issue in logical operators (and/or) with short-circuit evaluation
- ✅ Implemented proper list equality/inequality comparison support (`=` and `!=` operators)
- ✅ Updated all builtin function signatures to properly handle both vectors and lists
- ✅ Clear TypeError messages for invalid operations (e.g., `[1,2] + [3,4]` now shows helpful error)
- ✅ All 248 tests continue passing after fixes

## Recent Additions (Phases 1, 2, 3 & 4 Complete)
1. **Phase 4: Higher-Order Functions (NEW!)** - Functional programming powerhouses:
   - `map of [f, list]` - Transform each element uniformly
   - `filter of [p, list]` - Select elements matching predicate
   - `reduce of [f, list, init]` - Fold/accumulate to single value
   - Maintains geometric semantics throughout
   - Examples: doubling, filtering evens/positives, sum/product/max reduction
   - Chaining operations: filter → map → reduce
   - See `docs/higher_order_functions.md` for full documentation
   - See `examples/higher_order_functions.eigs` for comprehensive examples
2. **Phase 3: Advanced List Operations** - Complete list manipulation:
   - `append of [list, value]` mutates list in place
   - `pop of list` removes and returns last element
   - `min of list` and `max of list` for finding extremes
   - `sort of list` returns new sorted list (non-mutating)
   - Fixed negative number decoding in LRVM space
   - Nested list support (lists can contain other lists)
   - 24 comprehensive unit tests, examples/lists.eigs updated
2. **Phase 2: String Power** - Complete string manipulation:
   - String concatenation with `+` operator
   - String indexing `text[0]` for character access
   - String slicing `text[0:5]`, `text[2:]`, `text[:3]`
   - String built-ins: `upper`, `lower`, `split`, `join`
   - Metadata system to preserve string values in LRVM space
   - 18 comprehensive unit tests, examples/strings.eigs
3. **Phase 1: Core Operators** - Complete C/C++/Python operator parity:
   - Logical operators: AND, OR with **short-circuit evaluation**
   - Extended comparisons: <=, >=, !=
   - Modulo operator: %
   - Correct operator precedence
   - 30 comprehensive unit tests (205 total, 60% coverage)
4. **CLI Integration** - Fully connected interpreter to command-line interface
5. **Standard Library** - Built-in functions (print, input, len, type, norm, range, upper, lower, split, join, append, pop, min, max, sort, map, filter, reduce)
6. **Interactive REPL** - Full multi-line support for function definitions, conditionals, loops
7. **Introspection** - Framework Strength (fs) and spacetime signature accessible from code
8. **Meta-Circular Evaluator** - examples/eval.eigs demonstrates self-interpretation
9. **Better Error Messages** - Helpful hints for common syntax and runtime errors
10. **Full List/Array Support** - Complete implementation with:
    - List literals `[1, 2, 3]` 
    - List indexing `my_list[i]`
    - List slicing `my_list[1:4]`
    - range() function creating sequences
    - len() and type() aware of lists
    - append, pop, min, max, sort operations
    - Nested list support
    - 38 comprehensive unit tests (14 basic + 24 advanced)

## Next Steps (Future Enhancements)
- List comprehensions (EigenScript-style)
- Additional string functions (replace, find, strip, startswith, endswith)
- Complete meta-circular evaluator with AST representation
- Performance optimizations

## Notes
- This is a CLI tool, not a web application
- No frontend or backend servers needed
- Main development activity is running tests and executing .eigs files
- The interpreter is in alpha development - language spec may change
