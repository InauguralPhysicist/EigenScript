# Known Issues

**Last Updated**: 2025-11-19  
**Project Status**: 95% Complete, Phase 5 In Progress  
**Test Suite**: 442 passing, 5 skipped  
**Code Coverage**: 78% overall

---

## Summary

EigenScript is functionally complete and stable with **self-hosting achieved**. The remaining issues are primarily related to advanced parser features, standard library expansion, and test coverage improvements. No critical bugs or blockers exist.

### Issue Statistics

- **Critical**: 0 issues
- **Major**: 2 issues (Parser limitations, Untested module)
- **Minor**: 3 issues (Nested list conversion, CLI coverage gaps, Documentation)
- **Total Issues**: 5 tracked issues
- **Skipped Tests**: 5 tests

---

## Issues by Category

### 🔴 Parser & Language Features

#### **ISSUE-001: Function Definition Syntax with Named Parameters**
- **Severity**: Major
- **Status**: Known limitation, enhancement planned
- **Impact**: 3 tests skipped
- **Description**: Function definitions using the syntax `define <name> as:` with an implicit `arg` parameter work for basic cases, but more complex parameter handling is not yet fully supported by the parser.

**Affected Tests**:
- `test_datetime.py::test_measure_execution_time`
- `test_enhanced_lists.py::test_with_map_and_zip`
- `test_json.py::test_json_with_map`

**Example Code That Fails**:
```eigenscript
define factorial as:
    if arg <= 1:
        return 1
    else:
        return arg * (factorial of (arg - 1))

result is factorial of 10
```

**Current Workaround**:
Use simpler function definitions without complex recursion or nested calls. Basic map/filter/reduce operations work fine with simple predicates.

**Root Cause**:
The parser's function definition handling (`ast_builder.py`) needs enhancement to better support:
- Implicit `arg` parameter in all contexts
- Complex recursive function calls
- Function definitions used with higher-order functions (map, filter)

**Fix Required**:
- Parser enhancement in `src/eigenscript/parser/ast_builder.py`
- Add support for explicit parameter declaration syntax
- Improve AST node handling for function definitions

**Estimated Effort**: 3-5 days

**Related Files**:
- `src/eigenscript/parser/ast_builder.py` (lines 658-723: function parsing)
- `tests/test_datetime.py` (line 132)
- `tests/test_enhanced_lists.py` (line 267)
- `tests/test_json.py` (line 298)

**References**:
- See `docs/higher_order_functions.md` for design goals
- Parser coverage: 82% (needs improvement in function definition area)

---

### 🟡 Standard Library

#### **ISSUE-002: Nested List Type Conversion in JSON**
- **Severity**: Minor
- **Status**: Edge case, future improvement
- **Impact**: 2 tests skipped
- **Description**: JSON parsing and stringification work correctly for flat lists and simple nested structures, but complex nested list type conversions have edge cases that need refinement.

**Affected Tests**:
- `test_json.py::test_stringify_nested_list`
- `test_json.py::test_roundtrip_nested_list`

**Example Code**:
```eigenscript
# This works
simple is [1, 2, 3]
json is json_stringify of simple  # OK: "[1, 2, 3]"

# This has edge cases
nested is [[1, 2], [3, 4]]
json is json_stringify of nested  # Edge case: type conversion issues
parsed is json_parse of json      # Round-trip may not preserve exact structure
```

**Current Workaround**:
- Use flat lists for JSON operations
- Manually flatten nested structures before JSON conversion
- For complex nested data, use multiple JSON operations on sub-lists

**Root Cause**:
- LRVM vector type system handles lists uniformly
- Type conversion between EigenList and Python nested lists needs refinement
- JSON encoder/decoder in `builtins.py` needs enhancement for nested structures

**Fix Required**:
- Improve type conversion in `src/eigenscript/builtins.py`
- Add recursive handling for nested EigenList structures
- Update JSON encode/decode functions (lines 1385-1437)

**Estimated Effort**: 2-3 days

**Related Files**:
- `src/eigenscript/builtins.py` (JSON functions: lines 1385-1437)
- `tests/test_json.py` (lines 197-220)

**References**:
- JSON functions have 76% coverage overall
- Nested list operations work fine in other contexts (flatten, enumerate, etc.)

---

### 🟢 Testing & Coverage

#### **ISSUE-003: EigenControl Module Has Zero Test Coverage**
- **Severity**: Major
- **Status**: Module is used but untested
- **Impact**: 88 lines, 0% coverage
- **Description**: The `eigencontrol.py` module implements the core EigenControl geometric algorithm but has no test coverage. The module IS imported and used by the interpreter for advanced predicates (`improving`) and geometric metrics, but these code paths are not exercised by current tests.

**Module Functions**:
- `EigenControl.__init__` - Initialize with opposing quantities A and B
- `invariant` property - Compute I = ||A - B||²
- `radius` property - Compute r = √I
- `surface_area` property - Compute S = 4πr²
- `volume` property - Compute V = (4/3)πr³
- `curvature` property - Compute κ = 1/r
- `has_converged()` - Check if I → 0
- `get_conditioning()` - Classify problem conditioning
- `get_framework_strength()` - Compute FS from curvature
- `EigenControlTracker` - Track geometry over trajectory

**Current Status**:
- Module is imported in `src/eigenscript/evaluator/interpreter.py` (2 locations)
- Used for `improving` predicate checking
- Used for process metrics computation
- Code paths not triggered by existing tests

**Why This Matters**:
EigenControl is the theoretical foundation of the geometric computation model. While the core interpreter works without explicitly testing this module, comprehensive testing would:
- Validate the geometric algorithm implementation
- Ensure convergence detection works correctly
- Verify curvature and radius calculations
- Test trajectory tracking for optimization

**Tests Needed**:
1. Basic invariant computation (I = ||A - B||²)
2. Radius calculation (r = √I)
3. Surface area and volume scaling
4. Curvature measurement
5. Convergence detection
6. Integration with `improving` predicate
7. Edge cases: I = 0 (perfect convergence), large I (far from solution)
8. Trajectory tracking and trend analysis

**Fix Required**:
- Create `tests/test_eigencontrol.py` with comprehensive tests
- Test all EigenControl class methods
- Test EigenControlTracker functionality
- Test integration with interpreter predicates

**Estimated Effort**: 2-3 days

**Related Files**:
- `src/eigenscript/runtime/eigencontrol.py` (88 lines, 0% coverage)
- `src/eigenscript/evaluator/interpreter.py` (imports on lines for `improving` predicate)

**References**:
- See `docs/eigenfunction_analysis.md` for theoretical background
- See `UNUSED_MODULES_CLEANUP.md` for analysis of why this module was kept

---

#### **ISSUE-004: CLI Test Coverage Gaps**
- **Severity**: Minor
- **Status**: Partial coverage, needs improvement
- **Impact**: 26 lines untested (80% coverage)
- **Description**: The CLI module (`__main__.py`) has 80% test coverage, but some error handling paths and edge cases remain untested.

**Untested Code Paths** (lines with no coverage):
- Lines 72-77: Specific error handling paths
- Lines 82-93: Edge cases in argument parsing
- Line 138: Specific REPL error case
- Lines 169-170: File reading error handling
- Lines 174-178: Additional error scenarios

**Current Coverage**:
- File execution: ✅ Tested
- REPL mode: ✅ Tested
- Basic argument parsing: ✅ Tested
- `--measure-fs` flag: ✅ Tested
- Error handling: ⚠️ Partially tested

**Tests Needed**:
1. Error handling for invalid file paths
2. Error handling for malformed code
3. Edge cases in REPL input handling
4. Argument parsing with invalid combinations
5. Signal handling (Ctrl+C) in REPL

**Fix Required**:
- Add tests for uncovered error paths
- Test edge cases in `tests/test_cli.py`
- Aim for 90%+ coverage

**Estimated Effort**: 1 day

**Related Files**:
- `src/eigenscript/__main__.py` (132 lines, 80% coverage)
- `tests/test_cli.py` (existing tests)

---

#### **ISSUE-005: Documentation Website Needed**
- **Severity**: Minor
- **Status**: Planned enhancement
- **Impact**: User experience, adoption
- **Description**: Currently, documentation exists as Markdown files in the repository. A proper documentation website (MkDocs or Sphinx) would improve discoverability and user experience.

**Current State**:
- ✅ Comprehensive Markdown documentation exists
- ✅ README.md with getting started guide
- ✅ API examples in `docs/examples.md`
- ✅ Architecture documentation in `docs/architecture.md`
- ❌ No hosted documentation website
- ❌ No searchable API reference
- ❌ No interactive tutorials

**What's Needed**:
1. **Documentation Website**:
   - MkDocs or Sphinx setup
   - GitHub Pages hosting
   - Custom theme and branding

2. **Content Organization**:
   - Getting Started guide
   - Language reference
   - Standard library API reference
   - Advanced topics (geometric semantics, self-hosting)
   - Tutorials and examples
   - Contributing guide

3. **Features**:
   - Search functionality
   - Code syntax highlighting for EigenScript
   - Interactive examples (future: in-browser REPL)
   - Version selector for documentation

**Fix Required**:
- Set up MkDocs or Sphinx
- Organize existing Markdown docs
- Configure GitHub Pages deployment
- Add navigation and search

**Estimated Effort**: 5-7 days

**Related Files**:
- `docs/*.md` (all documentation)
- `README.md`
- Future: `mkdocs.yml` or `conf.py`

---

## Issues by Severity

### Critical (0 issues)
*None* - No critical bugs or blockers. Core language is stable and production-ready.

### Major (2 issues)
1. **ISSUE-001**: Function Definition Syntax with Named Parameters (Parser)
2. **ISSUE-003**: EigenControl Module Has Zero Test Coverage (Testing)

### Minor (3 issues)
3. **ISSUE-002**: Nested List Type Conversion in JSON (Standard Library)
4. **ISSUE-004**: CLI Test Coverage Gaps (Testing)
5. **ISSUE-005**: Documentation Website Needed (Documentation)

---

## Skipped Tests Reference

All 5 skipped tests are documented and tracked with clear reasons:

| Test | Reason | Issue |
|------|--------|-------|
| `test_datetime.py::test_measure_execution_time` | Function definition syntax with 'arg' parameter | ISSUE-001 |
| `test_enhanced_lists.py::test_with_map_and_zip` | Function definition syntax with 'arg' parameter | ISSUE-001 |
| `test_json.py::test_stringify_nested_list` | Nested list type conversion edge case | ISSUE-002 |
| `test_json.py::test_roundtrip_nested_list` | Nested list type conversion edge case | ISSUE-002 |
| `test_json.py::test_json_with_map` | Function definition syntax with 'arg' parameter | ISSUE-001 |

To run only skipped tests:
```bash
pytest -v -k "test_measure_execution_time or test_with_map_and_zip or test_stringify_nested_list or test_roundtrip_nested_list or test_json_with_map"
```

---

## Non-Issues

### What's NOT Broken

The following are explicitly **not** issues:

1. **Self-Hosting**: ✅ Working perfectly (meta-circular evaluator)
2. **Turing Completeness**: ✅ Proven and tested
3. **Framework Strength**: ✅ 90% coverage, fully functional
4. **LRVM Backend**: ✅ 85% coverage, stable
5. **Interrogatives**: ✅ All working (WHO, WHAT, WHEN, WHERE, WHY, HOW)
6. **Semantic Predicates**: ✅ All working (converged, stable, diverging, etc.)
7. **Control Flow**: ✅ IF/ELSE, LOOP working perfectly
8. **Arithmetic**: ✅ All operators functional
9. **Built-in Functions**: ✅ 18 functions, 76% coverage
10. **Math Library**: ✅ 11 functions, all tested
11. **Higher-Order Functions**: ✅ map, filter, reduce working (except Issue-001 edge cases)

---

## Workarounds

While we work on fixing the known issues, here are recommended workarounds:

### For Function Definitions (ISSUE-001)
Instead of:
```eigenscript
define factorial as:
    if arg <= 1:
        return 1
    else:
        return arg * (factorial of (arg - 1))
```

Use simpler patterns or inline computation:
```eigenscript
# Use built-in functions where possible
numbers is [1, 2, 3, 4, 5]
doubled is map of [lambda x: x * 2, numbers]  # When lambda syntax is added
```

### For Nested Lists in JSON (ISSUE-002)
Instead of:
```eigenscript
nested is [[1, 2], [3, 4]]
json is json_stringify of nested
```

Flatten first:
```eigenscript
nested is [[1, 2], [3, 4]]
flat is flatten of nested
json is json_stringify of flat  # Works reliably
```

Or process each sublist:
```eigenscript
nested is [[1, 2], [3, 4]]
# Convert each sublist separately
json1 is json_stringify of nested[0]
json2 is json_stringify of nested[1]
```

---

## Resolution Timeline

Based on current project roadmap (see `WHATS_LEFT_TODO.md`):

### Week 2-3: Parser & Standard Library
- **ISSUE-001**: Function definition syntax enhancement
- **ISSUE-002**: JSON nested list improvements
- **Target**: Unskip 3 datetime/list tests

### Week 3-4: Testing & Quality
- **ISSUE-003**: EigenControl test coverage
- **ISSUE-004**: CLI coverage improvements
- **Target**: 85%+ overall coverage

### Week 4-5: Documentation
- **ISSUE-005**: Documentation website
- **Target**: Live website with full API reference

**Estimated Total Time to Resolution**: 3-5 weeks

---

## How to Help

### For New Contributors

**Easy Issues** (Good First Issues):
- ISSUE-004: Add CLI test cases (1 day, clear scope)
- ISSUE-005: Help with documentation website setup

**Medium Issues**:
- ISSUE-002: Improve JSON nested list handling (2-3 days)
- ISSUE-003: Write EigenControl tests (2-3 days)

**Advanced Issues**:
- ISSUE-001: Parser enhancement for function definitions (3-5 days)

### For Experienced Contributors

Help with:
1. Parser architecture review (ISSUE-001)
2. Type system improvements (ISSUE-002)
3. Test infrastructure and coverage tools

### For Documentation Writers

Help with:
1. Documentation website setup (ISSUE-005)
2. Tutorial content creation
3. API reference formatting
4. Example program curation

---

## Reporting New Issues

If you encounter an issue not listed here:

1. **Check this document** to ensure it's not already known
2. **Check GitHub Issues** at https://github.com/yourusername/EigenScript/issues
3. **Verify it's reproducible** with a minimal test case
4. **Report with details**:
   - EigenScript version
   - Python version
   - Operating system
   - Minimal code to reproduce
   - Expected vs. actual behavior
   - Full error message and stack trace

### Issue Template

```markdown
**Description**: Brief summary

**EigenScript Version**: (from `eigenscript --version`)
**Python Version**: (from `python --version`)
**OS**: (e.g., Ubuntu 22.04, macOS 13, Windows 11)

**Code to Reproduce**:
```eigenscript
# Your minimal example here
```

**Expected Behavior**:
What you expected to happen

**Actual Behavior**:
What actually happened

**Error Message** (if any):
```
Full error message and stack trace
```

**Additional Context**:
Any other relevant information
```

---

## Related Documents

- **[WHATS_LEFT_TODO.md](WHATS_LEFT_TODO.md)** - Roadmap and task checklist
- **[PROJECT_STATUS_SUMMARY.md](PROJECT_STATUS_SUMMARY.md)** - Overall project status
- **[COMPLETION_PLAN.md](COMPLETION_PLAN.md)** - Detailed completion strategy
- **[UNUSED_MODULES_CLEANUP.md](UNUSED_MODULES_CLEANUP.md)** - Module analysis
- **[docs/roadmap.md](docs/roadmap.md)** - Technical roadmap
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines

---

## Version History

### 2025-11-19 - v1.0
- Initial comprehensive known issues document
- 5 issues tracked across 3 categories
- All skipped tests documented
- Workarounds provided for all issues
- Resolution timeline established

---

**Status**: COMPLETE AND CURRENT  
**Next Review**: After Week 2 tasks complete  
**Maintainer**: Project Team

For questions or clarifications, please open a GitHub discussion or issue.
