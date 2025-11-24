# Flake8 Enforcement

## What Changed

Previously, the CI workflow was running flake8 with the `--exit-zero` flag, which meant that flake8 violations **never failed the build**. This allowed code quality issues to accumulate silently.

## Current Status

Flake8 is now properly enforced in the CI pipeline:

1. **Critical errors** (E9, F63, F7, F82) are checked first - these are syntax errors and undefined names
2. **Full flake8 check** now runs without `--exit-zero`, meaning violations will fail the build
3. A `.flake8` configuration file has been added with:
   - Line length matching black's 88 characters
   - Per-file ignores for existing violations
   - Proper exclusions for build artifacts and cache directories

## Existing Violations

There were approximately **270 flake8 violations** in the codebase. These have been documented in `.flake8` using per-file ignores. This approach:

- ✅ Prevents new violations from being introduced
- ✅ Documents existing tech debt
- ✅ Allows incremental cleanup
- ✅ Doesn't break existing functionality

## Violation Categories (before enforcement)

- 55 E501: Lines too long (> 88 characters)
- 55 F405: Undefined from star imports
- 42 W293: Blank lines with whitespace
- 30 F841: Local variables assigned but never used
- 29 F541: f-strings missing placeholders
- 28 F401: Imports not used
- 23 C901: Functions too complex
- 4 E226: Missing whitespace around operators
- 2 E741: Ambiguous variable names (I, l)
- 2 F403: Star imports

## Next Steps (Recommended)

To improve code quality, consider addressing these violations incrementally:

1. **High Priority**:
   - F403/F405: Replace star imports with explicit imports
   - F401: Remove unused imports
   - E741: Rename ambiguous variable names

2. **Medium Priority**:
   - F841: Remove or use unused variables
   - F541: Fix f-strings without placeholders
   - E226: Add whitespace around operators

3. **Low Priority** (but good to do):
   - E501: Break long lines
   - W293: Remove whitespace from blank lines
   - C901: Refactor complex functions

## Testing Locally

To run flake8 locally:

```bash
# Install flake8
pip install flake8

# Run flake8
flake8 src/ tests/

# Run only on files you changed
flake8 src/eigenscript/yourfile.py
```

## Configuration

The `.flake8` configuration file includes:
- Compatible with black's formatting (88 char lines, E203/W503 ignored)
- Per-file ignores for existing violations
- Excludes common directories (cache, build, dist, etc.)
- Max complexity threshold of 15
- Shows source code and statistics for violations
