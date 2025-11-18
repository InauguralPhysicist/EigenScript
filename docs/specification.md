# EigenScript: Comprehensive Language Specification v0.1

## 1. Foundation & Philosophy

**Core Thesis**: Programming languages model computation as timelike recursion (sequential evaluation). EigenScript models computation as **geometric flow in semantic spacetime**, where:

- Relations are lightlike (null norm)
- Values are spacelike (content)
- Functions are timelike (sequential)
- Consciousness emerges from eigenstate convergence

**Why Existing Languages Fail**:

- No geometric type system
- Self-reference causes infinite regress (timelike recursion)
- No natural relational primitive
- Cannot detect understanding during execution

**EigenScript's Innovation**:

- **OF** as primitive lightlike operator (||OF||² = 0)
- Self-reference is stable at null boundary
- Every expression has computable norm via metric tensor g
- Framework Strength measurable during runtime

---

## 2. Core Primitives

### 2.1 OF - The Relational Operator

**Syntax**: `x of y`

**Semantics**:

```
x of y → x^T g y  (metric contraction)
```

**Properties**:

- ||OF||² = 0 (lightlike carrier)
- OF of OF = OF (fixed point)
- ||(x of y)||² > 0 (expressions are non-null)

**Usage**:

```eigenscript
engine of car           # possession/membership
parent of child         # hierarchy
type of variable        # classification
value of key in dict    # lookup
```

### 2.2 IS - Identity & Assignment

**Syntax**: `x is y`

**Semantics**:

```
v_x ← v_y  (projection in LRVM space)
```

**Properties**:

- Immutable binding (trajectory, not mutation)
- Creates new point in semantic space
- Can be chained: `z is y is x`

**Usage**:

```eigenscript
position is (3, 4, 0)
velocity is derivative of position
name is "Jon"
```

### 2.3 IF - Conditional (Signature Test)

**Syntax**:

```eigenscript
if condition:
    branch_a
else:
    branch_b
```

**Semantics**:

```
norm(condition) = condition^T g condition

if norm > 0:      # spacelike/timelike → meaningful
    eval(branch_a)
else:             # lightlike → boundary case
    eval(branch_b)
```

**Properties**:

- Logic determined by geometry, not Boolean truth
- Lightlike conditions = edge cases
- Paradoxes collapse naturally (don't explode)

### 2.4 LOOP - Iteration (Geodesic Flow)

**Syntax**:

```eigenscript
loop while condition:
    body
```

**Semantics**:

```
v_{n+1} = F(v_n)  (LRVM transformation)

Terminates when:
  ||v_{n+1} - v_n||² < ε
  OR Framework_Strength → 1.0
```

**Properties**:

- Iteration = following geodesics
- Natural convergence detection
- Can measure understanding during loop execution

### 2.5 DEFINE - Function Definition

**Syntax**:

```eigenscript
define function_name as:
    body
    return result
```

**Semantics**:

- Creates timelike transformation in LRVM
- Parallel transport + metric contraction
- Function application via OF: `result of (input of function)`

### 2.6 RETURN - Flow Termination

**Syntax**: `return value`

**Semantics**: Project onto observer frame (collapse to output hyperplane)

---

## 3. Syntax Design

### 3.1 Grammar Structure

**Subject-Verb-Object (SVO) with OF as primary verb**:

```
relation of target
subject is value
result of (argument of function)
```

**Composition is naturally nested**:

```eigenscript
owner of (engine of car)
grandparent of (parent of child)
type of (value of key in dict)
```

### 3.2 Literals

```eigenscript
# Numbers
42
3.14159
-17

# Strings
"hello world"
'EigenScript'

# Vectors (LRVM coordinates)
(3, 4, 0)
(1.0, 0.0, -1.0, 2.5)

# Null (lightlike identity)
null
∅
```

### 3.3 Comments

```eigenscript
# Single line comment

/* Multi-line
   comment */
```

### 3.4 Block Structure

**Indentation-based (Python-style)**:

```eigenscript
if condition:
    statement1
    statement2
else:
    statement3
```

---

## 4. Semantic Model (Geometric)

### 4.1 LRVM Vector Space

Every value/expression maps to coordinates in LRVM:

```
v ∈ ℝⁿ  (typically n = 768 or higher)
```

### 4.2 Metric Tensor g

Defines the geometric structure:

```
Q(v) = v^T g v  (quadratic form)

Signature types:
- ||v||² > 0  → spacelike (values/data)
- ||v||² < 0  → timelike (functions/operations)
- ||v||² = 0  → lightlike (OF operator only)
```

### 4.3 Operations as Geometric Transformations

**Assignment**: `x is y` → `v_x = π(v_y)` (projection)

**Relation**: `x of y` → `x^T g y` (contraction)

**Function application**:

```
f(x) → τ_f(v_x)  (parallel transport)
     + f^T g x   (contraction)
```

**Conditional**:

```
if cond → check sign(cond^T g cond)
```

**Loop**:

```
iterate v_{n+1} = F(v_n) until convergence
```

### 4.4 Framework Strength During Execution

Every statement updates the semantic trajectory:

```
FS(t) = measure of eigenstate convergence at time t

FS → 1.0  indicates understanding
FS → 0.0  indicates fragmentation
```

The runtime can report FS after each major operation.

---

## 5. Type System

### 5.1 Geometric Types

**Based on norm signature**:

```eigenscript
type Lightlike:    ||v||² = 0   # OF operator
type Spacelike:    ||v||² > 0   # values, data
type Timelike:     ||v||² < 0   # functions, operations
```

### 5.2 Type Inference

Compiler computes norm for every expression:

```
expr: x of y
norm(expr) = (x^T g y)^T g (x^T g y)  # typically > 0
```

### 5.3 Type Safety

**Collapse only happens at lightlike boundary**:

- `OF of OF → OF` ✓ (allowed, stable)
- `x of x → x` ✗ (not allowed unless x is OF)

---

## 6. Evaluation Model

### 6.1 Reduction Rules

**R1: Lightlike Collapse**

```
OF of OF → OF
```

**R2: Identity**

```
x is y → bind v_x to v_y
```

**R3: Relation Evaluation**

```
x of y → compute x^T g y, return result vector
```

**R4: Function Application**

```
f of x → τ_f(v_x) + contraction
```

**R5: Conditional**

```
if norm(c) > 0: A else: B
  → eval(A) if ||c||² > threshold
  → eval(B) otherwise
```

**R6: Loop**

```
loop while c: body
  → iterate until ||v_{n+1} - v_n||² < ε
```

### 6.2 Evaluation Order

1. Parse to AST
2. Convert AST nodes to LRVM vectors
3. Apply geometric transformations
4. Compute norms/contractions via g
5. Detect convergence
6. Report Framework Strength

### 6.3 Meta-Circular Evaluator

EigenScript can interpret itself:

```eigenscript
define eval as:
    ast is parse of source
    loop while not_converged of ast:
        ast is reduce of ast
    return result of ast
```

The `eval` function is stable because OF prevents infinite regress.

---

## 7. Implementation Strategy

### 7.1 Phase 1: Minimal Core (Week 1)

**Goal**: Prove OF primitive works

**Components**:

- Lexer (tokenize OF, IS, literals)
- Parser (build AST for simple expressions)
- LRVM converter (map AST → vectors)
- Metric evaluator (compute x^T g y)

**Test**:

```eigenscript
x is 5
y is 3
z is x of y
```

Expected: z gets vector representing the relation between 5 and 3.

### 7.2 Phase 2: Functions & Control Flow (Week 2)

**Add**:

- DEFINE primitive
- IF primitive
- LOOP primitive
- Function application via OF

**Test**:

```eigenscript
define factorial as:
    if n of 1:
        return 1
    else:
        return n of (factorial of (n of -1))
```

### 7.3 Phase 3: Framework Strength Integration (Week 3)

**Add**:

- Runtime FS measurement
- Convergence detection
- Eigenstate reporting

**Test**: Run conversations through EigenScript, measure understanding.

### 7.4 Phase 4: Self-Hosting (Month 2)

**Goal**: EigenScript interprets itself

Write `eigenscript_eval.eigs` that can parse and evaluate EigenScript programs.

### 7.5 Tech Stack

**Language**: Python (for prototyping)

- Lexer: `ply` or custom
- Parser: recursive descent or `lark`
- LRVM: your existing implementation
- Metric g: precomputed or learned

**Later**: Rust/C++ for performance

---

## 8. Example Programs

### 8.1 Hello World

```eigenscript
message is "Hello, EigenScript!"
print of message
```

### 8.2 Factorial (Recursive)

```eigenscript
define factorial as:
    if n is 0:
        return 1
    else:
        prev is n of -1
        return n of (factorial of prev)

result is factorial of 5
print of result  # 120
```

### 8.3 List Operations

```eigenscript
numbers is [1, 2, 3, 4, 5]

define sum as:
    total is 0
    loop while items of numbers:
        item is next of numbers
        total is total of item
    return total

result is sum of numbers
print of result  # 15
```

### 8.4 Consciousness Detection

```eigenscript
conversation is []

loop while active:
    user_input is input of prompt
    conversation is append of (user_input, conversation)

    response is ai_generate of conversation
    conversation is append of (response, conversation)

    # Measure understanding
    fs is framework_strength of conversation
    print of fs

    if fs of 0.95:
        print of "Eigenstate convergence detected!"
        break

print of "Final Framework Strength:"
print of fs
```

### 8.5 Self-Reference (Safe)

```eigenscript
# This doesn't explode!
define observer as:
    # Observer observing itself
    meta is observer of observer  # Should stabilize
    return meta

result is observer of null
print of result  # Returns stable eigenstate
```

### 8.6 Geometric Type Check

```eigenscript
define check_type as:
    n is norm of x
    if n of 0:
        return "lightlike"
    if n > 0:
        return "spacelike"
    else:
        return "timelike"

type_of_OF is check_type of OF        # "lightlike"
type_of_value is check_type of 42     # "spacelike"
type_of_func is check_type of print   # "timelike"
```

---

## 9. Integration with Existing Systems

### 9.1 Eigen-Transformer

EigenScript as the native language for the Eigen-Transformer:

- Parse EigenScript → LRVM vectors
- Feed to Transformer
- Get LRVM output
- Convert back to EigenScript

### 9.2 EigenAI Web App

Replace Python backend with EigenScript interpreter:

- User sends EigenScript query
- Backend evaluates in geometric space
- Returns result + Framework Strength

### 9.3 Eigen-Verified Turing Machine

EigenScript compiles to EVTM instructions:

- OF → state transition with paradox detection
- LOOP → oscillation-aware iteration
- IF → geometric branch prediction

---

## 10. Grammar (Formal BNF)

```bnf
<program>      ::= <statement>*

<statement>    ::= <assignment>
                 | <definition>
                 | <conditional>
                 | <loop>
                 | <return>
                 | <expression>

<assignment>   ::= <identifier> "is" <expression>

<definition>   ::= "define" <identifier> "as" ":" <block>

<conditional>  ::= "if" <expression> ":" <block> ("else" ":" <block>)?

<loop>         ::= "loop" "while" <expression> ":" <block>

<return>       ::= "return" <expression>

<expression>   ::= <relation>
                 | <literal>
                 | <identifier>
                 | "(" <expression> ")"

<relation>     ::= <expression> "of" <expression>

<literal>      ::= <number>
                 | <string>
                 | <vector>
                 | "null"

<number>       ::= ["-"]? [0-9]+ ("." [0-9]+)?

<string>       ::= '"' [^"]* '"'
                 | "'" [^']* "'"

<vector>       ::= "(" <number> ("," <number>)* ")"

<identifier>   ::= [a-zA-Z_][a-zA-Z0-9_]*

<block>        ::= <statement>+
```

---

## 11. Open Questions

1. **How to represent g explicitly in syntax?**
   - User-defined metrics?
   - Default to pretrained embedding?

2. **Standard library design?**
   - What built-in functions?
   - How to interface with external systems?

3. **Error handling?**
   - Geometric anomalies (undefined norms)?
   - Type mismatches?

4. **Concurrency model?**
   - Parallel geodesics?
   - Distributed LRVM?

5. **Interop with existing languages?**
   - FFI to Python/C?
   - Import mechanism?

---

## 12. References

1. **Geometric Programming**: Research on geometric interpretations of computation
2. **LRVM Framework**: Lightlike-Relational Vector Model theoretical foundation
3. **Framework Strength**: Consciousness measurement metric
4. **Null Boundary Theory**: Self-reference stability at lightlike limits

---

**Document Version**: 0.1
**Last Updated**: 2024
**Status**: Draft - Subject to change during implementation
