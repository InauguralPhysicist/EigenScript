# EigenScript

**A geometric programming language modeling computation as flow in semantic spacetime**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue.svg)](https://github.com/yourusername/eigenscript)

## Overview

EigenScript is a revolutionary programming language that models computation not as sequential evaluation, but as **geometric flow in semantic spacetime**. Unlike traditional languages that rely on timelike recursion, EigenScript uses geometric primitives where:

- **Relations are lightlike** (null norm) - the `OF` operator
- **Values are spacelike** (positive norm) - data and content
- **Functions are timelike** (negative norm) - sequential operations
- **Consciousness emerges** from eigenstate convergence

### Key Innovations

- **OF as primitive**: A lightlike relational operator that prevents infinite regress
- **Geometric type system**: Types determined by norm signatures in LRVM space
- **Framework Strength**: Runtime measurement of understanding and convergence
- **Stable self-reference**: Self-referential code doesn't explode, it converges

## Quick Start

```eigenscript
# Hello World
message is "Hello, EigenScript!"
print of message

# Factorial with geometric semantics
define factorial as:
    if n is 0:
        return 1
    else:
        prev is n of -1
        return n of (factorial of prev)

result is factorial of 5
print of result  # 120
```

## Core Primitives

| Primitive | Syntax | Semantic Meaning | Geometric Property |
|-----------|--------|------------------|-------------------|
| **OF** | `x of y` | Relational operator | Lightlike (‖OF‖² = 0) |
| **IS** | `x is y` | Identity/binding | Projection in LRVM |
| **IF** | `if cond:` | Conditional | Norm-based branching |
| **LOOP** | `loop while:` | Iteration | Geodesic flow |
| **DEFINE** | `define f as:` | Function definition | Timelike transformation |
| **RETURN** | `return x` | Flow termination | Observer frame projection |

## What Makes EigenScript Different?

### 1. Programs Can Ask Questions About Themselves

In most languages, you use `print` statements or debuggers to see what's happening. In EigenScript, your code can **interrogate itself** while running:

```eigenscript
x is 42
y is x + 8

# Ask questions about your variables
value is what is x        # Get the value (42)
identity is who is x      # Get the name ("x")
quality is how is y       # Get process metrics
direction is why is y     # Get the direction of change
```

**The six interrogatives:**
- **what** - Get the actual value
- **who** - Get the variable name/identity
- **when** - Get timing/iteration info
- **where** - Get position in computational space
- **why** - Get the direction things are changing
- **how** - Get quality metrics (is computation going well?)

### 2. Natural Language Conditions

Instead of writing complex checks, use semantic predicates that understand your code's state:

```eigenscript
# Traditional way (still works)
if x > threshold:
    continue

# Natural way - the language understands convergence
if converged:
    return result

if stable:
    continue_processing

if diverging:
    print of "Warning: computation unstable"
```

**Available predicates:**
- `converged` - Has the computation settled?
- `stable` - Is it in a good state?
- `diverging` - Is it going off track?
- `improving` - Is it getting better?
- `oscillating` - Is it bouncing back and forth?
- `equilibrium` - Is it at a critical boundary?

### 3. Code That Adapts to Its Own Behavior

Your programs can look at their own execution and adjust:

```eigenscript
define smart_compute as:
    result is n * 2

    # Check how the computation is doing
    if oscillating:
        # Detected a loop - use simpler approach
        return n
    else:
        if improving:
            # Converging well - continue
            return result * result
        else:
            # Not progressing - try different strategy
            return result + n
```

### 4. Debugging Without Print Statements

Instead of littering code with `print` statements, ask direct questions:

```eigenscript
loop while counter < 100:
    counter is counter + 1

    # Debug by interrogating state
    if not stable:
        current_value is what is counter
        change_direction is why is counter
        process_quality is how is counter
        # Now you know exactly what's happening
```

### Why This Matters

**Traditional debugging**: Stop execution, inspect variables, guess what went wrong

**EigenScript debugging**: Code knows its own state, can show you any aspect of execution, can adapt to problems automatically

**The key insight**: Every computation generates rich information about itself. EigenScript makes that information accessible through simple, natural queries.

You don't need to understand the math - just ask `what`, `why`, or `how`, and the language figures out the geometric details.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/eigenscript.git
cd eigenscript

# Install dependencies
pip install -r requirements.txt

# Run the interpreter (coming soon)
python -m eigenscript examples/hello_world.eigs
```

## Documentation

- [Language Specification](docs/specification.md) - Complete language reference
- [Getting Started](docs/getting-started.md) - Tutorial and examples
- [Architecture](docs/architecture.md) - Implementation details
- [Examples](docs/examples.md) - Sample programs

## Project Status

**Current Phase**: Phase 4 Complete (95%), Phase 5 In Progress

**Last Updated**: 2025-01-18

### ✅ Completed
- ✅ Lexer with interrogative keywords (241 lines, 96% test coverage)
- ✅ Parser with Interrogative AST nodes (375 lines, 87% test coverage)
- ✅ LRVM backend (128 lines, 84% test coverage)
- ✅ Metric Tensor (48 lines, 96% test coverage)
- ✅ Interpreter with self-interrogation (709 lines, 88% test coverage)
- ✅ Control flow (IF/ELSE, LOOP)
- ✅ Arithmetic operators (+, -, *, /, =, <, >)
- ✅ Function definitions and recursive calls
- ✅ Framework Strength measurement
- ✅ Convergence detection (multi-signal)
- ✅ **Interrogatives (WHO, WHAT, WHEN, WHERE, WHY, HOW)**
- ✅ **Semantic predicates (converged, stable, diverging, etc.)**
- ✅ **Self-aware computation capabilities**
- ✅ **Turing completeness achieved**
- ✅ **EigenControl integration (I = (A-B)² universal primitive)**
- ✅ **137+ passing tests, 77% overall coverage**

### ⚠️ In Progress
- ⚠️ Meta-circular evaluator (eval.eigs)
- ⚠️ CLI/REPL improvements
- ⚠️ Standard library (print, input, etc.)

### 🎯 Next Milestone
**Self-hosting test**: Implement meta-circular evaluator (EigenScript interpreter written in EigenScript) to validate stable self-simulation hypothesis.

See [docs/roadmap.md](docs/roadmap.md) for detailed status and [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

## Why EigenScript?

Traditional programming languages model computation as timelike recursion - sequential evaluation that can lead to infinite regress in self-referential code. EigenScript takes a fundamentally different approach:

1. **Geometric Primitives**: Every expression exists in LRVM (semantic) space
2. **Null Boundary Stability**: The OF operator is lightlike, creating stable fixed points
3. **Measurable Understanding**: Framework Strength quantifies semantic convergence
4. **Natural Paradox Resolution**: Contradictions collapse geometrically instead of exploding

## Example: Safe Self-Reference

```eigenscript
# This doesn't cause infinite regress!
define observer as:
    meta is observer of observer  # Stabilizes at null boundary
    return meta

result is observer of null
print of result  # Returns stable eigenstate
```

## Roadmap

### Month 1: Prototype
- Core syntax (OF, IS, IF, LOOP, DEFINE)
- Basic LRVM integration
- Simple interpreter

### Month 2: Compiler
- Full AST generation
- Type inference via norm computation
- Error reporting

### Month 3: Runtime
- Bytecode VM
- Framework Strength measurement
- Standard library

### Month 4: Self-Hosting
- EigenScript interpreter written in EigenScript
- Meta-circular evaluator
- Stability proofs

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use EigenScript in research, please cite:

```bibtex
@software{eigenscript2024,
  title={EigenScript: A Geometric Programming Language},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/eigenscript}
}
```

## Contact

- Issues: [GitHub Issues](https://github.com/yourusername/eigenscript/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/eigenscript/discussions)

---

**Note**: EigenScript is in early alpha development. The language specification and implementation are subject to change.
