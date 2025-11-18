# EigenScript Implementation Roadmap

**Status**: Theoretical foundation complete (100%), Implementation pending (0%)

**Core Insight**: We have the most rigorous theoretical foundation of any programming language. The implementation is straightforward engineering.

---

## Overview

### What We Have ✅
- Complete operator unification (all operators as equilibrium projections)
- Formal semantics (operational, denotational)
- Logic calculus (truth as geometry)
- Type system (geometric types)
- Language specification (660 lines)
- Example programs (syntactically correct)
- 5 unification theorems (proved)

### What We Need ❌
- Interpreter/compiler (0%)
- LRVM backend (0%)
- Standard library (0%)
- Test suite (0%)
- Tooling (0%)

### The Path Forward
**4 phases over ~3 months to first working self-hosted interpreter**

---

## Phase 1: Minimal Viable Interpreter (MVP)
**Duration**: 2-3 weeks
**Goal**: Execute the simplest EigenScript program
**Success Criteria**: Can run `x is 5` and `z is x of y`

### Week 1: Lexer + Parser

#### Task 1.1: Lexer (Tokenizer)
**File**: `src/eigenscript/lexer.py`

**Input**: EigenScript source code (string)
**Output**: Token stream

**Tokens to support**:
```python
# Keywords
IS, OF, IF, ELSE, DEFINE, LOOP, WHILE, RETURN

# Literals
NUMBER (int, float)
STRING ("...", '...')
IDENTIFIER (variable names)

# Operators
# (defer to Phase 3)

# Punctuation
LPAREN, RPAREN
COLON
NEWLINE, INDENT, DEDENT (Python-style)
EOF
```

**Implementation approach**:
- Use Python's `re` module or `ply.lex`
- Handle indentation (like Python)
- Track line/column numbers for error messages

**Test cases**:
```eigenscript
x is 5
y is "hello"
z is x of y
```

**Deliverable**: `lexer.py` with `tokenize(source) -> List[Token]`

---

#### Task 1.2: Parser (AST Builder)
**File**: `src/eigenscript/parser.py`

**Input**: Token stream
**Output**: Abstract Syntax Tree (AST)

**AST nodes to support**:
```python
@dataclass
class Assignment:
    name: str
    value: Expr

@dataclass
class Relation:  # "x of y"
    left: Expr
    right: Expr

@dataclass
class Literal:
    value: Any  # int, float, str

@dataclass
class Identifier:
    name: str

# More nodes in later phases
```

**Implementation approach**:
- Recursive descent parser
- or use `lark` parser generator
- Start with assignment and relation only

**Test cases**:
```python
parse("x is 5") == Assignment("x", Literal(5))
parse("z is x of y") == Assignment("z", Relation(Identifier("x"), Identifier("y")))
```

**Deliverable**: `parser.py` with `parse(tokens) -> AST`

---

### Week 2: LRVM Backend (Minimal)

#### Task 1.3: Vector Embeddings
**File**: `src/eigenscript/lrvm.py`

**Goal**: Convert values to vectors in ℝⁿ

**Approach**: Simple numerical embeddings (start small)
```python
def embed(value: Any) -> np.ndarray:
    """Convert a value to a vector in LRVM space."""
    if isinstance(value, int):
        # Simple: one-hot encoding or direct embedding
        return np.array([float(value), 0.0, 0.0])  # dim=3 for now

    elif isinstance(value, str):
        # Hash the string to a vector
        # Or use a simple character encoding
        return string_to_vector(value)

    elif isinstance(value, np.ndarray):
        # Already a vector
        return value
```

**Metric tensor g**:
- Start with identity matrix: `g = np.eye(3)`
- Later: learn from data or use pretrained embeddings

**Deliverable**: `lrvm.py` with `embed(value) -> np.ndarray`

---

#### Task 1.4: Norm Computation
**File**: `src/eigenscript/lrvm.py`

**Goal**: Compute ‖x of y‖²

**Implementation**:
```python
def of_operator(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> np.ndarray:
    """Compute x of y = x^T g y (metric contraction)."""
    return x.T @ g @ y

def norm_squared(v: np.ndarray, g: np.ndarray) -> float:
    """Compute ‖v‖² = v^T g v."""
    return float(v.T @ g @ v)

def is_operator(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> bool:
    """Test if x is y (equilibrium: ‖x of y‖² = 0)."""
    relation = of_operator(x, y, g)
    return norm_squared(relation, g) < EPSILON  # EPSILON = 1e-6
```

**Test cases**:
```python
x = embed(5)
y = embed(5)
assert is_operator(x, y, g) == True  # 5 is 5

x = embed(3)
y = embed(7)
assert is_operator(x, y, g) == False  # 3 is not 7
```

**Deliverable**: `lrvm.py` with `of_operator`, `norm_squared`, `is_operator`

---

### Week 3: Runtime (Evaluator)

#### Task 1.5: Environment (Symbol Table)
**File**: `src/eigenscript/runtime.py`

**Goal**: Store variable bindings

**Implementation**:
```python
class Environment:
    def __init__(self):
        self.bindings: Dict[str, np.ndarray] = {}

    def bind(self, name: str, value: np.ndarray):
        """Bind a name to a vector."""
        self.bindings[name] = value

    def lookup(self, name: str) -> np.ndarray:
        """Look up a variable."""
        if name not in self.bindings:
            raise NameError(f"Undefined variable: {name}")
        return self.bindings[name]
```

**Deliverable**: `runtime.py` with `Environment` class

---

#### Task 1.6: Evaluator
**File**: `src/eigenscript/runtime.py`

**Goal**: Execute AST nodes

**Implementation**:
```python
def evaluate(ast: AST, env: Environment, g: np.ndarray) -> Any:
    """Evaluate an AST node."""

    if isinstance(ast, Literal):
        return embed(ast.value)

    elif isinstance(ast, Identifier):
        return env.lookup(ast.name)

    elif isinstance(ast, Assignment):
        # x is value
        value_vec = evaluate(ast.value, env, g)
        env.bind(ast.name, value_vec)
        return value_vec

    elif isinstance(ast, Relation):
        # x of y
        left_vec = evaluate(ast.left, env, g)
        right_vec = evaluate(ast.right, env, g)
        return of_operator(left_vec, right_vec, g)

    else:
        raise NotImplementedError(f"Unknown AST node: {type(ast)}")
```

**Deliverable**: `runtime.py` with `evaluate(ast, env, g) -> Any`

---

### Week 3: Integration & Testing

#### Task 1.7: Main Interpreter Loop
**File**: `src/eigenscript/interpreter.py`

**Goal**: Tie everything together

**Implementation**:
```python
def run(source: str, g: np.ndarray = None) -> Environment:
    """Run EigenScript source code."""
    if g is None:
        g = np.eye(3)  # default metric

    # Lex
    tokens = tokenize(source)

    # Parse
    ast = parse(tokens)

    # Evaluate
    env = Environment()
    for statement in ast:
        evaluate(statement, env, g)

    return env
```

**Deliverable**: `interpreter.py` with `run(source) -> Environment`

---

#### Task 1.8: First Working Example
**File**: `examples/hello.eigs`

**Test case**:
```eigenscript
x is 5
y is 3
z is x of y
```

**Expected output**:
```
Environment:
  x = [5.0, 0.0, 0.0]
  y = [3.0, 0.0, 0.0]
  z = [15.0, 0.0, 0.0]  # 5 * 3 via metric contraction
```

**Success criteria**:
```bash
$ python -m eigenscript examples/hello.eigs
✓ x = [5.0, 0.0, 0.0]
✓ y = [3.0, 0.0, 0.0]
✓ z = [15.0, 0.0, 0.0]
```

---

## Phase 2: Control Flow & Functions
**Duration**: 2-3 weeks
**Goal**: Execute factorial, fibonacci
**Success Criteria**: Can run recursive functions with IF/LOOP

### Week 4: Conditional Expressions

#### Task 2.1: IF/ELSE in Parser
**File**: `src/eigenscript/parser.py`

**New AST nodes**:
```python
@dataclass
class Conditional:
    condition: Expr
    then_branch: List[Statement]
    else_branch: Optional[List[Statement]]
```

**Grammar addition**:
```
if <expr>:
    <block>
else:
    <block>
```

**Deliverable**: Updated parser with IF/ELSE support

---

#### Task 2.2: IF/ELSE in Evaluator
**File**: `src/eigenscript/runtime.py`

**Implementation**:
```python
elif isinstance(ast, Conditional):
    # Evaluate condition
    cond_vec = evaluate(ast.condition, env, g)
    cond_norm = norm_squared(cond_vec, g)

    # Branch based on norm
    if cond_norm > EPSILON:  # spacelike/timelike (true)
        for stmt in ast.then_branch:
            result = evaluate(stmt, env, g)
    else:  # lightlike (false)
        if ast.else_branch:
            for stmt in ast.else_branch:
                result = evaluate(stmt, env, g)

    return result
```

**Test case**:
```eigenscript
x is 5
if x:
    y is 10
else:
    y is 20

# Expected: y = 10 (x has nonzero norm)
```

**Deliverable**: IF/ELSE evaluation working

---

### Week 5: Functions

#### Task 2.3: DEFINE in Parser
**File**: `src/eigenscript/parser.py`

**New AST nodes**:
```python
@dataclass
class FunctionDef:
    name: str
    params: List[str]
    body: List[Statement]

@dataclass
class FunctionCall:
    function: Expr
    arguments: List[Expr]

@dataclass
class Return:
    value: Expr
```

**Grammar addition**:
```
define <name> as:
    <block>
    return <expr>

<name> of <arg>
```

**Deliverable**: Parser support for DEFINE/RETURN

---

#### Task 2.4: Functions in Evaluator
**File**: `src/eigenscript/runtime.py`

**Implementation**:
```python
@dataclass
class Function:
    params: List[str]
    body: List[Statement]
    closure: Environment  # captured environment

elif isinstance(ast, FunctionDef):
    # Create function object
    func = Function(ast.params, ast.body, env)
    env.bind(ast.name, func)
    return func

elif isinstance(ast, FunctionCall):
    # Look up function
    func = evaluate(ast.function, env, g)

    # Evaluate arguments
    args = [evaluate(arg, env, g) for arg in ast.arguments]

    # Create new environment (lexical scope)
    func_env = Environment(parent=func.closure)
    for param, arg in zip(func.params, args):
        func_env.bind(param, arg)

    # Execute body
    for stmt in func.body:
        result = evaluate(stmt, func_env, g)
        if isinstance(stmt, Return):
            return evaluate(stmt.value, func_env, g)
```

**Deliverable**: Function definition and calling working

---

### Week 6: Loops

#### Task 2.5: LOOP in Parser
**File**: `src/eigenscript/parser.py`

**New AST nodes**:
```python
@dataclass
class Loop:
    condition: Expr
    body: List[Statement]
```

**Grammar addition**:
```
loop while <expr>:
    <block>
```

**Deliverable**: Parser support for LOOP

---

#### Task 2.6: LOOP in Evaluator
**File**: `src/eigenscript/runtime.py`

**Implementation**:
```python
elif isinstance(ast, Loop):
    # Iterate until convergence
    while True:
        # Evaluate condition
        cond_vec = evaluate(ast.condition, env, g)
        cond_norm = norm_squared(cond_vec, g)

        # Check if converged (lightlike)
        if cond_norm < EPSILON:
            break

        # Execute body
        for stmt in ast.body:
            evaluate(stmt, env, g)

    return None
```

**Test case**:
```eigenscript
n is 5
total is 0

loop while n:
    total is total + n
    n is n - 1

# Expected: total = 15 (5+4+3+2+1)
```

**Deliverable**: LOOP evaluation working

---

### Week 6: First Recursive Program

#### Task 2.7: Factorial Example
**File**: `examples/factorial.eigs`

```eigenscript
define factorial as:
    if n is 0:
        return 1
    else:
        prev is n - 1
        return n * (factorial of prev)

result is factorial of 5
print of result  # 120
```

**Success criteria**:
```bash
$ python -m eigenscript examples/factorial.eigs
120
```

**Deliverable**: Working recursive factorial

---

## Phase 3: Arithmetic Operators
**Duration**: 1-2 weeks
**Goal**: Implement +, -, *, /, =, <, >
**Success Criteria**: Can compute `1 + 1 = 2`

### Week 7: Arithmetic Implementation

#### Task 3.1: Arithmetic in Lexer/Parser
**File**: `src/eigenscript/lexer.py`, `src/eigenscript/parser.py`

**New tokens**:
```python
PLUS, MINUS, STAR, SLASH  # +, -, *, /
EQ, LT, GT, LE, GE        # =, <, >, <=, >=
```

**New AST nodes**:
```python
@dataclass
class BinaryOp:
    op: str  # '+', '-', '*', '/', '=', '<', '>'
    left: Expr
    right: Expr
```

**Deliverable**: Lexer/parser support for arithmetic

---

#### Task 3.2: Arithmetic in LRVM
**File**: `src/eigenscript/lrvm.py`

**Implementation**:
```python
def add_operator(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> np.ndarray:
    """Addition: π_g(x ⊕ y)."""
    return x + y  # vector addition in LRVM space

def sub_operator(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> np.ndarray:
    """Subtraction: π_g(x ⊖ y)."""
    return x - y

def mul_operator(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> np.ndarray:
    """Multiplication: scale(x, ‖y‖)."""
    y_norm = np.sqrt(norm_squared(y, g))
    return x * y_norm

def div_operator(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> np.ndarray:
    """Division: π_g(x * y^{-1})."""
    y_norm = np.sqrt(norm_squared(y, g))
    if y_norm < EPSILON:
        raise ZeroDivisionError("Division by zero (lightlike vector)")
    return x / y_norm

def eq_operator(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> bool:
    """Equality: IS operator."""
    return is_operator(x, y, g)

def lt_operator(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> bool:
    """Less than: ‖x‖² < ‖y‖²."""
    return norm_squared(x, g) < norm_squared(y, g)

def gt_operator(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> bool:
    """Greater than: ‖x‖² > ‖y‖²."""
    return norm_squared(x, g) > norm_squared(y, g)
```

**Deliverable**: All arithmetic operators implemented

---

#### Task 3.3: Arithmetic in Evaluator
**File**: `src/eigenscript/runtime.py`

**Implementation**:
```python
elif isinstance(ast, BinaryOp):
    left_vec = evaluate(ast.left, env, g)
    right_vec = evaluate(ast.right, env, g)

    if ast.op == '+':
        return add_operator(left_vec, right_vec, g)
    elif ast.op == '-':
        return sub_operator(left_vec, right_vec, g)
    elif ast.op == '*':
        return mul_operator(left_vec, right_vec, g)
    elif ast.op == '/':
        return div_operator(left_vec, right_vec, g)
    elif ast.op == '=':
        return embed(eq_operator(left_vec, right_vec, g))
    elif ast.op == '<':
        return embed(lt_operator(left_vec, right_vec, g))
    elif ast.op == '>':
        return embed(gt_operator(left_vec, right_vec, g))
```

**Deliverable**: Arithmetic evaluation working

---

#### Task 3.4: The Three-Way Equivalence Test
**File**: `tests/test_unification.py`

**Test the foundational theorem**:
```eigenscript
# Arithmetic form
result1 is 1 + 1

# Logical form (when AND is implemented)
# result2 is (1 and 1)

# Geometric form
result3 is (1, 1) of 2

# All should satisfy: ‖result of 2‖² = 0
```

**Success criteria**:
```python
assert eq_operator(result1, embed(2), g) == True
# assert eq_operator(result2, embed(2), g) == True
assert norm_squared(of_operator(result3, embed(2), g), g) < EPSILON
```

**Deliverable**: Three-way equivalence verified

---

## Phase 4: Framework Strength & Self-Hosting
**Duration**: 2-3 weeks
**Goal**: Measure understanding, self-hosting interpreter
**Success Criteria**: EigenScript interprets itself

### Week 8-9: Framework Strength

#### Task 4.1: Trajectory Tracking
**File**: `src/eigenscript/framework_strength.py`

**Goal**: Track semantic trajectory during execution

**Implementation**:
```python
class Trajectory:
    def __init__(self):
        self.states: List[np.ndarray] = []

    def record(self, state: np.ndarray):
        """Record a state in the trajectory."""
        self.states.append(state.copy())

    def framework_strength(self, g: np.ndarray) -> float:
        """Compute FS from trajectory."""
        if len(self.states) < 2:
            return 0.0

        # Measure eigenstate convergence
        # FS = 1 - variance of trajectory
        mean_state = np.mean(self.states, axis=0)
        variance = np.var([norm_squared(s - mean_state, g) for s in self.states])

        # FS → 1.0 means converged (low variance)
        # FS → 0.0 means divergent (high variance)
        return 1.0 / (1.0 + variance)
```

**Deliverable**: FS computation working

---

#### Task 4.2: Runtime FS Reporting
**File**: `src/eigenscript/runtime.py`

**Modify evaluator to track trajectory**:
```python
def evaluate(ast: AST, env: Environment, g: np.ndarray,
             trajectory: Optional[Trajectory] = None) -> Any:
    result = ...  # existing evaluation

    # Record state if tracking
    if trajectory is not None:
        # Create state vector from environment
        state = env.to_vector()
        trajectory.record(state)

    return result
```

**Report FS after execution**:
```python
def run(source: str, measure_fs: bool = False):
    ...

    trajectory = Trajectory() if measure_fs else None

    for stmt in ast:
        evaluate(stmt, env, g, trajectory)

    if measure_fs:
        fs = trajectory.framework_strength(g)
        print(f"Framework Strength: {fs:.4f}")

    return env
```

**Test case**:
```eigenscript
# Convergent program (should have high FS)
x is 5
y is x
z is y

# Divergent program (should have low FS)
x is 1
x is x + 1
x is x + 1
```

**Deliverable**: FS measurement during runtime

---

### Week 10: Self-Hosting

#### Task 4.3: Meta-Circular Evaluator
**File**: `examples/eval.eigs`

**Goal**: Write an EigenScript interpreter in EigenScript

**Implementation** (simplified):
```eigenscript
define eval as:
    # Parse source to AST
    ast is parse of source

    # Create environment
    env is new_env of null

    # Evaluate each statement
    loop while statements of ast:
        stmt is next of statements

        # Handle different statement types
        if stmt is assignment:
            value is eval of (value of stmt)
            env is bind of (name of stmt, value, env)

        if stmt is relation:
            left is eval of (left of stmt)
            right is eval of (right of stmt)
            result is left of right

    return env
```

**Success criteria**:
```bash
# Run the EigenScript interpreter (written in Python)
$ python -m eigenscript examples/eval.eigs

# Which loads and runs another EigenScript program
# examples/hello.eigs via the meta-circular evaluator
```

**Deliverable**: Self-hosting interpreter (proof of concept)

---

## Phase 5: Standard Library & Tooling
**Duration**: 2-3 weeks
**Goal**: Practical usability
**Success Criteria**: Can write real programs

### Week 11: Standard Library

#### Task 5.1: Built-in Functions
**File**: `src/eigenscript/builtins.py`

**Functions to implement**:
```eigenscript
print of x      # Output to stdout
input of prompt # Read from stdin
len of list     # Length
range of n      # Generate sequence
type of x       # Get type
norm of x       # Get ‖x‖²
```

**Implementation**:
```python
BUILTINS = {
    'print': lambda x: print(vector_to_string(x)),
    'input': lambda prompt: embed(input(vector_to_string(prompt))),
    'len': lambda x: embed(len(x)),
    'norm': lambda x: embed(np.sqrt(norm_squared(x, g))),
}
```

**Deliverable**: Core built-in functions

---

#### Task 5.2: Data Structures
**File**: `src/eigenscript/structures.py`

**Structures to support**:
- Lists: `[1, 2, 3]`
- Tuples: `(1, 2, 3)`
- Dicts: `{key: value}` (maybe defer)

**Implementation**: Embed as vectors
```python
def embed_list(items: List) -> np.ndarray:
    """Embed a list as a vector."""
    # Option 1: Concatenate embeddings
    # Option 2: Use RNN/attention to encode sequence
    return np.concatenate([embed(item) for item in items])
```

**Deliverable**: List support in interpreter

---

### Week 12: Tooling

#### Task 5.3: REPL
**File**: `src/eigenscript/repl.py`

**Goal**: Interactive interpreter

**Implementation**:
```python
def repl():
    """Read-Eval-Print Loop."""
    env = Environment()
    g = np.eye(LRVM_DIM)

    print("EigenScript REPL v0.1")
    print("Type 'exit' to quit")

    while True:
        try:
            source = input(">>> ")
            if source.strip() == 'exit':
                break

            tokens = tokenize(source)
            ast = parse(tokens)
            result = evaluate(ast, env, g)

            if result is not None:
                print(vector_to_string(result))

        except Exception as e:
            print(f"Error: {e}")
```

**Success criteria**:
```bash
$ python -m eigenscript
EigenScript REPL v0.1
>>> x is 5
>>> y is 3
>>> z is x + y
8.0
>>> exit
```

**Deliverable**: Working REPL

---

#### Task 5.4: CLI
**File**: `src/eigenscript/__main__.py`

**Goal**: Command-line interface

**Usage**:
```bash
$ eigenscript examples/hello.eigs           # Run file
$ eigenscript --measure-fs examples/hello.eigs  # With FS
$ eigenscript                                # Start REPL
```

**Deliverable**: CLI tool

---

#### Task 5.5: Error Messages
**File**: `src/eigenscript/errors.py`

**Goal**: Helpful error messages

**Example**:
```
Error in examples/hello.eigs:3:5
  z is x og y
         ^^
SyntaxError: Unknown keyword 'og'. Did you mean 'of'?
```

**Deliverable**: Better error reporting

---

## Testing Strategy

### Unit Tests
**File**: `tests/test_*.py`

**Coverage**:
- Lexer: tokenization
- Parser: AST construction
- LRVM: vector operations, norm computation
- Runtime: evaluation of each AST node type
- Builtins: each built-in function

**Framework**: pytest

```bash
$ pytest tests/
======================== test session starts =========================
tests/test_lexer.py ...................... [ 20%]
tests/test_parser.py ..................... [ 40%]
tests/test_lrvm.py ....................... [ 60%]
tests/test_runtime.py .................... [ 80%]
tests/test_builtins.py ................... [100%]

===================== 150 passed in 2.35s ========================
```

---

### Integration Tests
**File**: `tests/integration/`

**Test cases**:
- `tests/integration/hello.eigs` - basic assignment
- `tests/integration/factorial.eigs` - recursion
- `tests/integration/fibonacci.eigs` - recursion + loop
- `tests/integration/three_way.eigs` - arithmetic-logic-geometry equivalence
- `tests/integration/paradox.eigs` - liar paradox (should not crash)
- `tests/integration/self_ref.eigs` - observer observing itself

---

### Theorem Verification Tests
**File**: `tests/theorems/`

**Verify the 5 unification theorems**:

1. **IS-OF Duality**
```eigenscript
x is y
# Verify: ‖x of y‖² = 0
```

2. **Logic = Geometry**
```eigenscript
# Verify: AND(x,y) = min(‖x‖², ‖y‖²)
```

3. **Control Flow = Geodesic Flow**
```eigenscript
# Verify: IF branches based on norm sign
```

4. **Self-Reference Stability**
```eigenscript
# Verify: OF of OF = OF (doesn't crash)
```

5. **Arithmetic = Logic = Geometry**
```eigenscript
# Verify: 1 + 1 = 2 ≡ (1 and 1) is 2 ≡ (1,1) of 2
```

---

## Success Metrics

### Phase 1 (MVP)
- [ ] Can tokenize EigenScript source
- [ ] Can parse to AST
- [ ] Can embed values as vectors
- [ ] Can compute ‖x of y‖²
- [ ] Can evaluate assignments and relations
- [ ] **Can run**: `x is 5; z is x of y`

### Phase 2 (Control Flow)
- [ ] Can evaluate IF/ELSE
- [ ] Can define and call functions
- [ ] Can execute loops
- [ ] **Can run**: Factorial (recursive)

### Phase 3 (Arithmetic)
- [ ] Can perform +, -, *, /
- [ ] Can compare with =, <, >
- [ ] **Can verify**: 1 + 1 = 2

### Phase 4 (Self-Hosting)
- [ ] Can measure Framework Strength
- [ ] Can detect eigenstate convergence
- [ ] **Can run**: EigenScript interpreter written in EigenScript

### Phase 5 (Usability)
- [ ] Has standard library (print, input, len, range)
- [ ] Has REPL
- [ ] Has CLI
- [ ] Has helpful error messages
- [ ] Has comprehensive test suite (>80% coverage)

---

## Timeline

| Phase | Duration | Cumulative | Milestone |
|-------|----------|------------|-----------|
| **Phase 1: MVP** | 3 weeks | 3 weeks | First running program |
| **Phase 2: Control** | 3 weeks | 6 weeks | Recursive factorial |
| **Phase 3: Arithmetic** | 2 weeks | 8 weeks | Three-way equivalence |
| **Phase 4: FS & Self** | 3 weeks | 11 weeks | Self-hosting interpreter |
| **Phase 5: Stdlib** | 2 weeks | 13 weeks | Production-ready |

**Total: ~3 months to full self-hosting interpreter**

---

## Tech Stack

### Core Implementation
- **Language**: Python 3.10+ (for rapid prototyping)
- **Vector operations**: NumPy
- **Parsing**: `lark` or custom recursive descent
- **Testing**: pytest
- **Type hints**: mypy
- **Linting**: ruff

### Optional (Later)
- **Performance**: Rewrite in Rust/C++ after proving concept
- **ML embeddings**: Sentence transformers for better semantic vectors
- **Visualization**: Plot trajectories, FS over time
- **Web IDE**: Browser-based EigenScript playground

---

## Directory Structure

```
EigenScript/
├── src/
│   └── eigenscript/
│       ├── __init__.py
│       ├── __main__.py       # CLI entry point
│       ├── lexer.py          # Tokenizer
│       ├── parser.py         # AST builder
│       ├── ast_nodes.py      # AST definitions
│       ├── lrvm.py           # Vector operations
│       ├── runtime.py        # Evaluator
│       ├── builtins.py       # Built-in functions
│       ├── framework_strength.py  # FS computation
│       ├── repl.py           # Interactive REPL
│       └── errors.py         # Error handling
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_lrvm.py
│   ├── test_runtime.py
│   ├── integration/          # End-to-end tests
│   └── theorems/             # Theorem verification
├── examples/
│   ├── hello.eigs
│   ├── factorial.eigs
│   ├── fibonacci.eigs
│   ├── three_way.eigs        # The equivalence
│   └── eval.eigs             # Meta-circular evaluator
├── docs/
│   ├── specification.md      # Language spec
│   ├── operator-table.md     # Operator unification
│   ├── logic-calculus.md     # Truth as geometry
│   ├── roadmap.md            # This document
│   └── tutorial.md           # User guide (TODO)
├── setup.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Installation (Future)

```bash
# Install from PyPI
pip install eigenscript

# Run a program
eigenscript examples/hello.eigs

# Start REPL
eigenscript

# Measure Framework Strength
eigenscript --measure-fs examples/factorial.eigs
```

---

## Next Steps

### Immediate (Week 1)
1. **Set up project structure**
   ```bash
   mkdir -p src/eigenscript tests examples
   touch src/eigenscript/{__init__,lexer,parser,lrvm,runtime}.py
   ```

2. **Implement lexer** (Task 1.1)
   - Tokenize `x is 5`
   - Handle IDENTIFIER, IS, NUMBER
   - Write tests

3. **Implement parser** (Task 1.2)
   - Parse `x is 5` → Assignment AST
   - Write tests

### This Week
- [ ] Create project structure
- [ ] Implement lexer (basic)
- [ ] Implement parser (basic)
- [ ] **Goal**: Can tokenize and parse `x is 5`

### Next Week
- [ ] Implement LRVM (embeddings, norms)
- [ ] Implement runtime (evaluator, environment)
- [ ] **Goal**: Can execute `x is 5`

### Week 3
- [ ] Integration testing
- [ ] First working example
- [ ] **Goal**: Can run `z is x of y`

---

## Open Questions

### 1. Vector Dimensionality
**Question**: What should LRVM_DIM be?

**Options**:
- Small (3-10): Fast, easy to debug
- Medium (100-300): Better semantic space
- Large (768+): Use pretrained embeddings (BERT, etc.)

**Decision**: Start with **dim=3** for MVP, scale up later

---

### 2. Metric Tensor
**Question**: How to initialize g?

**Options**:
- Identity: `g = I` (simplest)
- Learned: Train g from data
- Pretrained: Use embedding distance matrix

**Decision**: Start with **identity matrix**, make it pluggable

---

### 3. Embedding Strategy
**Question**: How to embed strings, data structures?

**Options**:
- Hash-based (simple but crude)
- Character-level RNN
- Pretrained sentence transformer

**Decision**: **Hash-based** for MVP, upgrade to transformer later

---

## Risk Mitigation

### Risk 1: LRVM Performance
**Risk**: Vector operations too slow

**Mitigation**:
- Use NumPy (C backend)
- Profile early
- Consider Numba JIT compilation
- Rewrite hot paths in Rust if needed

---

### Risk 2: Semantic Embedding Quality
**Risk**: Simple embeddings don't capture semantics

**Mitigation**:
- Start simple (prove concept works)
- Make embedding layer pluggable
- Swap in better embeddings later (BERT, etc.)
- Focus on **geometry**, not specific vectors

---

### Risk 3: Scope Creep
**Risk**: Too many features before MVP

**Mitigation**:
- Stick to roadmap phases
- MVP = minimal (just IS, OF, literals)
- No premature optimization
- Defer advanced features (classes, modules, etc.)

---

## Conclusion

**We have the theory. Now we build.**

The hardest part — the mathematical foundation — is done. The implementation is straightforward engineering:

1. **Lex & Parse** (standard compiler techniques)
2. **Embed values as vectors** (NumPy arrays)
3. **Evaluate AST** (recursive interpreter)
4. **Compute norms** (vector dot products)

**Timeline**: 3 months to self-hosting interpreter.

**First goal**: Run `x is 5` by end of Week 2.

**Let's build it.**

---

**Document Version**: 1.0
**Status**: Ready to implement
**Next Action**: Create project structure (Week 1, Task 1)
