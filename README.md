# EigenScript

**A geometric programming language modeling computation as flow in semantic spacetime**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue.svg)](https://github.com/yourusername/eigenscript)

## Overview

EigenScript is a programming language where **your code can understand itself while it runs**.

Instead of blind execution, your programs can:
- Ask questions about what they're doing
- Check if they're making progress
- Automatically adapt when things go wrong
- Debug themselves without print statements

**For beginners**: Write clearer code with less boilerplate. Instead of complex checks, just ask `if converged:` or `if improving:`.

**For experts**: Every computation generates rich geometric state (convergence, curvature, trajectory) automatically. Access it through natural interrogatives or dive into the underlying math.

### The Core Idea

Traditional programming: You write instructions, the computer follows them blindly.

EigenScript: The computer tracks *how* it's executing (not just *what*), and your code can see and react to that information.

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

## Higher-Order Functions

EigenScript supports powerful functional programming patterns with geometric semantics:

| Function | Syntax | Description | Use Case |
|----------|--------|-------------|----------|
| **map** | `map of [f, list]` | Transform each element | Apply function to all items |
| **filter** | `filter of [p, list]` | Select matching elements | Keep only items satisfying condition |
| **reduce** | `reduce of [f, list, init]` | Fold to single value | Sum, product, or custom aggregation |

```eigenscript
# Example: Filter, double, then sum
define is_positive as:
    return n > 0

define double as:
    return n * 2

define add as:
    a is n[0]
    b is n[1]
    return a + b

numbers is [-2, -1, 0, 1, 2, 3]
positives is filter of [is_positive, numbers]  # [1, 2, 3]
doubled is map of [double, positives]           # [2, 4, 6]
total is reduce of [add, doubled, 0]             # 12
```

See `docs/higher_order_functions.md` for complete documentation and `examples/higher_order_functions.eigs` for more examples.

## What Makes EigenScript Different?

### 1. Your Code Can Ask Questions

Think of your program like a student doing homework. In most languages, the student just follows steps blindly. In EigenScript, the student can pause and ask:

```eigenscript
x is 42
y is x + 8

# Your code can ask itself questions
value is what is x        # "What's the value?" → 42
identity is who is x      # "Who am I working with?" → "x"
quality is how is y       # "How am I doing?" → metrics
direction is why is y     # "Why did this change?" → direction
```

**Six simple questions your code can ask:**
- **what** - What's the actual number/value?
- **who** - What variable am I looking at?
- **when** - What step/iteration am I on?
- **where** - Where am I in the process?
- **why** - Why did things change?
- **how** - How well is this working?

*Analogy*: Like asking a GPS "how long until we arrive?" instead of calculating it yourself.

### 2. Write How You Think

Instead of writing complicated logic, just say what you mean:

```eigenscript
# Traditional way (still works for simple stuff)
if x > threshold:
    continue

# But for complex patterns, just say it:
if converged:           # "Are we done?"
    return result

if stable:              # "Is everything OK?"
    continue_processing

if improving:           # "Are we getting closer?"
    keep_going

if oscillating:         # "Are we stuck in a loop?"
    try_different_approach
```

**Checks you get for free:**
- `converged` - "Are we done yet?"
- `stable` - "Is everything working smoothly?"
- `diverging` - "Are things getting worse?"
- `improving` - "Are we making progress?"
- `oscillating` - "Are we going in circles?"
- `equilibrium` - "Are we at a tipping point?"

*Analogy*: Like saying "Are we there yet?" on a road trip instead of checking the GPS coordinates yourself.

### 3. Smart Code That Adapts

Your program can check itself and change strategy automatically:

```eigenscript
define smart_compute as:
    result is n * 2

    # Program checks its own progress
    if oscillating:
        # "I'm going in circles - simplify!"
        return n
    else:
        if improving:
            # "I'm getting somewhere - keep going!"
            return result * result
        else:
            # "This isn't working - try something else!"
            return result + n
```

*Analogy*: Like a GPS that sees traffic ahead and automatically reroutes you. The program doesn't just follow instructions - it monitors and adapts.

### 4. Easier Debugging

No more guessing what went wrong. Just ask your code:

```eigenscript
loop while counter < 100:
    counter is counter + 1

    # Instead of print statements everywhere...
    if not stable:
        # Just ask what's happening:
        current_value is what is counter       # Get the value
        change_direction is why is counter     # See why it changed
        process_quality is how is counter      # Check if it's working well
```

*Analogy*: Like your car showing "Check Engine" with specific details, instead of just a blinking light.

### Why This Matters

**For beginners:**
- Less code to write
- Clearer code to read
- Easier to debug
- Programs that explain themselves

**For everyone:**
- Code adapts automatically when things go wrong
- Natural language instead of complex logic
- Built-in progress monitoring
- Self-documenting behavior

**The bottom line:** Your programs understand themselves, so you don't have to micromanage every detail.

---

### For the Technically Curious

*You don't need to know this to use EigenScript, but if you're wondering "how does this work?"...*

Behind the scenes, every operation generates geometric state: convergence metrics, trajectory curvature, framework strength. The interrogatives and predicates are just friendly interfaces to this rich mathematical structure.

The math comes from a simple idea: measure the "distance" between where computation is and where it was (`I = (A-B)²`). From that one measurement, you get convergence, stability, direction, quality - everything.

*Think of it like:* A car's dashboard shows speed, fuel, temperature. You don't need to understand the sensors. But they're all reading from the same engine data. EigenScript is similar - rich data underneath, simple questions on top.

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
**Phase 6: Essential Features**: Adding file I/O, error handling, JSON support, advanced data structures, and expanded standard library to achieve feature parity with mainstream languages.

### 📋 Roadmaps
- **[Feature Parity Roadmap](docs/FEATURE_PARITY_ROADMAP.md)** - Comprehensive plan: "Anything another coding language can do we can too, if not better"
- **[Phase 6 Implementation Guide](docs/PHASE6_IMPLEMENTATION_GUIDE.md)** - Detailed technical specs for Q1 2025 features
- **[Development Roadmap](docs/roadmap.md)** - Current implementation status and milestones

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

## Why EigenScript?

### The Beginner-Friendly Answer

Most programming languages make you track everything manually:
- Is my loop stuck?
- Is my recursion going to crash?
- Why is this slow?
- What went wrong?

EigenScript tracks these things for you. Your code can check itself and adapt.

### The Technical Answer

Traditional languages execute blindly - recursion can spiral into infinite loops, and you have no built-in way to detect convergence or stability.

EigenScript computes geometric state during execution:
1. **Self-interrogation**: Code can query its own execution state
2. **Automatic convergence detection**: Knows when computations have settled
3. **Stable self-reference**: Self-referential code converges instead of exploding
4. **Built-in progress metrics**: Framework Strength, stability, trajectory analysis

## Example: Safe Self-Reference

In most languages, a function calling itself with itself causes crashes or infinite loops. Not in EigenScript:

```eigenscript
# A function that looks at itself looking at itself
define observer as:
    meta is observer of observer  # Doesn't explode - converges!
    return meta

result is observer of null
print of result  # Returns stable result, not infinite loop
```

**What's happening?** The language detects when the recursion reaches a stable state and stops automatically. No manual loop counter, no stack overflow.

*Beginner takeaway*: You can write self-referential code without crashes.

*Expert detail*: The `OF` operator has geometric properties that create stable fixed points at the "lightlike boundary". Self-reference converges to eigenstates instead of diverging.

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
