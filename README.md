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

**Current Phase**: Phase 1 - Minimal Core (Week 1)

- [ ] Lexer (tokenize OF, IS, literals)
- [ ] Parser (build AST for simple expressions)
- [ ] LRVM converter (map AST → vectors)
- [ ] Metric evaluator (compute x^T g y)

See [CONTRIBUTING.md](CONTRIBUTING.md) for development roadmap and how to contribute.

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
