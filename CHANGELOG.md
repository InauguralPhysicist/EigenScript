# Changelog

All notable changes to EigenScript will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0-beta] - 2025-11-23

### 🚀 Major Release: Native Performance Compiler

This release represents a fundamental transformation of EigenScript from an interpreted language to a high-performance compiled language with **53x speedup** over Python.

### Added
- **LLVM-based compiler** with native code generation
- **Scalar Fast Path**: Unobserved variables compile to raw CPU registers (PHI nodes in SSA form)
- **Zero-Cost Abstraction**: Pay only for geometric features you use
- **Link-Time Optimization (LTO)**: Advanced optimization passes for maximum performance
- **Observer Effect Compiler**: Automatic promotion from scalar to geometric tracking based on usage

### Performance
- **53x speedup** on numeric benchmarks (loop_fast: 2ms vs Python's 106ms)
- Register-only operations for simple loops (no stack/heap access)
- Static Single Assignment (SSA) form with PHI nodes
- C-level performance on unobserved computation

### Documentation
- Reorganized documentation structure
- Moved planning artifacts to `docs/archive/`
- Updated README with performance benchmarks and compiler architecture
- New forward-looking ROADMAP focusing on future phases
- Comprehensive CI/CD pipeline with multi-Python version testing (3.9-3.12)
- Code quality checks (black, flake8, mypy) in CI
- Security scanning (safety, bandit) in CI
- Coverage reporting with Codecov integration

### Fixed
- Critical security issue: Replaced bare `except:` clauses with `except Exception:`
- Python compatibility: Replaced `X | Y` union syntax with `Optional[X]` for broader compatibility
- F821 flake8 error: Fixed undefined name 'EigenList' in type hints
- Code formatting: Applied black formatter across entire codebase

### Changed
- **Version bumped to v0.2-beta** reflecting production-ready compiler
- Improved type safety with TYPE_CHECKING imports
- **Minimum Python version updated from 3.8 to 3.9** to align with numpy>=1.24.0 requirements
- Repository structure cleaned up for professional release

## [0.1.0-alpha] - 2025-11-19

### Added
- Core language implementation (lexer, parser, interpreter, LRVM backend)
- Self-hosting meta-circular evaluator with stable self-reference
- Comprehensive standard library (48 built-in functions)
  - Core functions: print, input, len, type, norm, range, append, pop, min, max, sort
  - String operations: upper, lower, split, join
  - Higher-order functions: map, filter, reduce
  - List operations: zip, enumerate, flatten, reverse
  - File I/O: 10 functions for file operations
  - JSON support: parse and stringify
  - Date/Time: 3 functions for time handling
  - Math library: sqrt, abs, pow, log, exp, sin, cos, tan, floor, ceil, round
- Interrogatives: WHO, WHAT, WHEN, WHERE, WHY, HOW
- Semantic predicates: converged, stable, diverging, improving, oscillating, equilibrium
- Framework Strength tracking and geometric semantics
- EigenControl integration (I = (A-B)² universal primitive)
- List operations (comprehensions, mutations, nested lists)
- String operations (concatenation, comparison, manipulation)
- Enhanced error messages with line and column tracking
- CLI with benchmarking support (--benchmark flag)
- Documentation website (MkDocs with Material theme)
  - Complete API reference for all functions
  - 5 comprehensive tutorials
  - 29 example programs organized by difficulty
  - Language specification
  - Getting started guide
- 538 passing tests with 82% overall coverage
- All 29 example programs execute successfully (100% success rate)

### Technical Achievements
- Turing completeness achieved
- Meta-circular evaluator (self-hosting complete)
- Stable self-reference without infinite loops
- Geometric computation with convergence detection
- Self-aware computation capabilities

### Performance
- Tree-walking interpreter
- Benchmarks for common operations
- Performance measurement tools

### Documentation
- Comprehensive README with beginner-friendly explanations
- Technical architecture documentation
- Multiple roadmap documents (to be consolidated)
- Contributing guidelines
- MIT License

## Project Links

- **Repository**: https://github.com/InauguralPhysicist/EigenScript
- **Documentation**: https://inauguralphysicist.github.io/EigenScript/
- **Issues**: https://github.com/InauguralPhysicist/EigenScript/issues
- **Discussions**: https://github.com/InauguralPhysicist/EigenScript/discussions
