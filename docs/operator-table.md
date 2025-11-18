# EigenScript Operator Table: Complete Unification via Equilibrium

## The Fundamental Theorem

**All operators in EigenScript are projections, tests, inversions, or compositions of a single primitive: equilibrium.**

```
IS  = equilibrium
OF  = equilibrium projected through geometry
IF  = test for equilibrium
NOT = inversion of equilibrium
AND/OR = multi-directional equilibrium composition
```

This document provides the complete operator taxonomy.

---

## 1. The Equilibrium Primitive

### Definition

**Equilibrium** is the state where relational tension vanishes:

```
equilibrium(x, y) ⟺ ‖x of y‖² = 0
```

Properties:
- Zero norm = perfect balance
- No semantic distance
- Fixed point of relation
- Lightlike boundary condition

### Geometric Interpretation

In LRVM space with metric tensor **g**:

```
x is y  ⟺  ‖x of y‖² = x^⊤ g y g^⊤ g y x = 0
```

When this collapses to zero:
- Identity achieved
- Relation stabilizes
- Semantic convergence
- Consciousness emerges

---

## 2. The Core Operator Family

### 2.1 IS - The Equilibrium Operator

**Syntax**: `x is y`

**Formal Definition**:
```
IS: V × V → {0, 1}
IS(x, y) = 1  ⟺  ‖x of y‖² = 0
         = 0  otherwise
```

**Geometric Form**:
```
x is y  ⟺  ‖π_g(x) - π_g(y)‖² = 0
```

**Properties**:
- Reflexive: `x is x` → true (zero distance to self)
- Symmetric: `x is y` ⟺ `y is x` (metric symmetry)
- Transitive: `x is y` ∧ `y is z` → `x is z` (geodesic composition)
- Fixed point: `IS is IS` (operator self-stability)

**Physical Interpretation**:
- Identity = null geodesic between points
- Assignment = trajectory to equilibrium
- Binding = semantic convergence

---

### 2.2 OF - The Projection Operator

**Syntax**: `x of y`

**Formal Definition**:
```
OF: V × V → V
OF(x, y) = π_g(x, y) = x^⊤ g y
```

**Relationship to IS**:
```
OF is IS projected through geometry

IS(x, y) = 1  ⟺  ‖OF(x, y)‖² = 0
OF(x, y) = projection of identity through metric g
```

**Properties**:
- Lightlike carrier: `‖OF‖² = 0` (the operator itself)
- Fixed point: `OF of OF = OF`
- Non-null result: `‖x of y‖² > 0` for x ≠ y
- Associative: `(x of y) of z = x of (y of z)`

**Duality Theorem**:
```
IS = OF when norm collapses (equilibrium)
OF = IS when projected through g (geometry)

They are the same operator in different bases.
```

**Physical Interpretation**:
- OF = directional derivative of semantic space
- Relation = geodesic connection
- Possession = geometric attachment
- Membership = embedding projection

---

### 2.3 IF - The Equilibrium Test Operator

**Syntax**: `if condition: A else: B`

**Formal Definition**:
```
IF: V × V × V → V
IF(c, A, B) = A  if ‖c‖² > ε
            = B  if ‖c‖² ≤ ε

where ε = equilibrium threshold (typically ε = 0)
```

**Relationship to IS**:
```
IF = boundary test of IS

if A:     # test if A is equilibrium
  do B    # execute when ‖A‖² > 0 (spacelike/timelike)
else:
  do C    # execute when ‖A‖² = 0 (lightlike)
```

**Geometric Form**:
```
IF(c, A, B) = { A  if c^⊤ g c > 0  (spacelike/timelike)
              { B  if c^⊤ g c = 0  (lightlike)
              { B  if c^⊤ g c < 0  (timelike boundary)
```

**Properties**:
- Decision boundary = metric signature
- No Boolean algebra required
- Paradoxes naturally collapse (‖paradox‖² = 0 → else branch)
- Self-reference is stable (lightlike test)

**Truth Values as Geometry**:
```
true  = ‖c‖² > 0   (meaningful, spacelike/timelike)
false = ‖c‖² = 0   (boundary, lightlike)
```

**Physical Interpretation**:
- IF = observer measurement of norm
- Branching = geodesic splitting
- Collapse = wavefunction reduction
- Control flow = geometric path selection

---

### 2.4 NOT - The Equilibrium Inversion Operator

**Syntax**: `not A`

**Formal Definition**:
```
NOT: V → V
NOT(x) = projection onto orthogonal complement

‖NOT(x)‖² = -‖x‖²  (signature flip)
```

**Relationship to IS**:
```
NOT = moving away from equilibrium

not A  means  A is not-equilibrium
            ⟺  ‖A‖² > 0
```

**Geometric Form**:
```
NOT(x) = g^{-1} x^⟂

where x^⟂ is orthogonal to x under metric g
```

**Properties**:
- Double negation: `not (not x) = x`
- DeMorgan: `not (x and y) = (not x) or (not y)`
- Equilibrium flip: `‖NOT(x)‖² = -‖x‖²`

**Truth Table (Geometric)**:
```
‖x‖² > 0  →  ‖not x‖² = 0   (true → false)
‖x‖² = 0  →  ‖not x‖² > 0   (false → true)
```

**Physical Interpretation**:
- NOT = time reversal operator
- Negation = geodesic reflection
- Contradiction = orthogonal projection
- Complement = dual space

---

### 2.5 AND - The Multi-Equilibrium Conjunction

**Syntax**: `A and B`

**Formal Definition**:
```
AND: V × V → V
AND(x, y) = projection onto intersection

‖x and y‖² > 0  ⟺  ‖x‖² > 0 ∧ ‖y‖² > 0
```

**Relationship to IS**:
```
AND = simultaneous equilibrium test

A and B  means  both A and B are not-equilibrium
              ⟺  ‖A‖² > 0  and  ‖B‖² > 0
```

**Geometric Form**:
```
AND(x, y) = π_g(x) ∩ π_g(y)
          = min(x^⊤ g x, y^⊤ g y)
```

**Truth Table (Geometric)**:
```
‖A‖² > 0  ‖B‖² > 0  →  ‖A and B‖² > 0   (true ∧ true = true)
‖A‖² > 0  ‖B‖² = 0  →  ‖A and B‖² = 0   (true ∧ false = false)
‖A‖² = 0  ‖B‖² > 0  →  ‖A and B‖² = 0   (false ∧ true = false)
‖A‖² = 0  ‖B‖² = 0  →  ‖A and B‖² = 0   (false ∧ false = false)
```

**Properties**:
- Commutative: `A and B = B and A`
- Associative: `(A and B) and C = A and (B and C)`
- Identity: `A and true = A`
- Annihilator: `A and false = false`

**Physical Interpretation**:
- AND = geodesic intersection
- Conjunction = simultaneous constraints
- Both true = both non-equilibrium

---

### 2.6 OR - The Multi-Equilibrium Disjunction

**Syntax**: `A or B`

**Formal Definition**:
```
OR: V × V → V
OR(x, y) = projection onto union

‖x or y‖² > 0  ⟺  ‖x‖² > 0 ∨ ‖y‖² > 0
```

**Relationship to IS**:
```
OR = alternative equilibrium test

A or B  means  at least one is not-equilibrium
            ⟺  ‖A‖² > 0  or  ‖B‖² > 0
```

**Geometric Form**:
```
OR(x, y) = π_g(x) ∪ π_g(y)
         = max(x^⊤ g x, y^⊤ g y)
```

**Truth Table (Geometric)**:
```
‖A‖² > 0  ‖B‖² > 0  →  ‖A or B‖² > 0   (true ∨ true = true)
‖A‖² > 0  ‖B‖² = 0  →  ‖A or B‖² > 0   (true ∨ false = true)
‖A‖² = 0  ‖B‖² > 0  →  ‖A or B‖² > 0   (false ∨ true = true)
‖A‖² = 0  ‖B‖² = 0  →  ‖A or B‖² = 0   (false ∨ false = false)
```

**Properties**:
- Commutative: `A or B = B or A`
- Associative: `(A or B) or C = A or (B or C)`
- Identity: `A or false = A`
- Annihilator: `A or true = true`

**Physical Interpretation**:
- OR = geodesic union
- Disjunction = alternative paths
- Either true = at least one non-equilibrium

---

### 2.7 THEN - The Causal Sequencing Operator

**Syntax**: `A then B`

**Formal Definition**:
```
THEN: V × V → V
THEN(x, y) = timelike composition

result = τ_x(y)  (parallel transport of y along x)
```

**Relationship to IS**:
```
THEN = sequential equilibrium evolution

A then B  means  A achieves equilibrium, then B evolves
```

**Geometric Form**:
```
THEN(x, y) = geodesic flow from x to y

x then y = lim_{t→1} γ(t) where γ(0) = x, γ(1) = y
```

**Properties**:
- Associative: `(A then B) then C = A then (B then C)`
- Non-commutative: `A then B ≠ B then A` (time ordering)
- Timelike signature: `‖A then B‖² < 0`

**Physical Interpretation**:
- THEN = causal evolution
- Sequencing = geodesic flow
- Time ordering = trajectory composition

---

### 2.8 ELSE - The Alternative Branch Operator

**Syntax**: `if A: B else: C`

**Formal Definition**:
```
ELSE: V × V → V
ELSE(A, B, C) = C when ‖A‖² = 0
              = B otherwise
```

**Relationship to IS**:
```
ELSE = equilibrium boundary handler

else: C  means  execute C when condition IS equilibrium
```

**Geometric Form**:
```
ELSE(A, B, C) = { B  if A^⊤ g A > 0
                { C  if A^⊤ g A = 0
```

**Properties**:
- Dual to IF: `else` is the lightlike branch
- Default case: executes at equilibrium boundary
- Paradox handler: catches contradictions

**Physical Interpretation**:
- ELSE = null geodesic handler
- Alternative = boundary condition
- Default = lightlike collapse

---

## 3. Complete Operator Hierarchy

### Level 0: Primitive (Equilibrium)
```
equilibrium(x, y) ⟺ ‖x of y‖² = 0
```

### Level 1: Core Dyad
```
IS  = equilibrium state
OF  = equilibrium projection
```

### Level 2: Control Flow
```
IF   = equilibrium test
THEN = equilibrium sequence
ELSE = equilibrium alternative
```

### Level 3: Logic
```
NOT = equilibrium inversion
AND = equilibrium conjunction
OR  = equilibrium disjunction
```

### Level 4: Derived Operators
```
IMPLIES  = (not A) or B
XOR      = (A or B) and not (A and B)
NAND     = not (A and B)
NOR      = not (A or B)
```

---

## 4. Unification Theorems

### Theorem 1: IS-OF Duality
```
IS(x, y) = 1  ⟺  ‖OF(x, y)‖² = 0

IS and OF are projections of the same operator
through different geometric bases.
```

**Proof**:
```
IS(x, y) tests for equilibrium: ‖x of y‖² = 0
OF(x, y) computes projection: x^⊤ g y
At equilibrium: x^⊤ g y g^⊤ g y x = 0 ⟹ IS = 1
∴ IS = OF|_{‖·‖²=0}
```

### Theorem 2: Logic = Geometry
```
Boolean logic is recovered as the discrete boundary
of continuous geometric equilibrium.
```

**Proof**:
```
true  ⟺ ‖x‖² > 0  (spacelike/timelike)
false ⟺ ‖x‖² = 0  (lightlike)

All logical operators reduce to norm comparisons:
AND(x,y) = min(‖x‖², ‖y‖²) > 0
OR(x,y)  = max(‖x‖², ‖y‖²) > 0
NOT(x)   = -‖x‖²
```

### Theorem 3: Control Flow = Geodesic Flow
```
All control flow operators are geodesic path selections
in semantic spacetime.
```

**Proof**:
```
IF   = geodesic branching based on metric signature
THEN = geodesic composition via parallel transport
LOOP = geodesic iteration until convergence

Control flow is geometric, not computational.
```

### Theorem 4: Self-Reference Stability
```
All operators are stable under self-application
at the lightlike boundary.
```

**Proof**:
```
OF of OF = OF         (‖OF‖² = 0)
IS is IS = true       (IS achieves equilibrium with itself)
IF if A: B = B        (IF tests itself → always meaningful)

Self-reference collapses to fixed point, not infinite regress.
```

---

## 5. Operator Composition Rules

### Rule 1: Equilibrium Composition
```
equilibrium ∘ equilibrium = equilibrium

(x is y) is (z is w)  →  equilibrium state
```

### Rule 2: Projection Composition
```
(x of y) of z = x of (y of z)

Associativity via metric linearity.
```

### Rule 3: Test Composition
```
if (if A: B else: C): D else: E

Nested tests = sequential norm evaluations.
```

### Rule 4: Logic Composition
```
(A and B) or (C and D) = and/or tree → norm evaluation tree
```

---

## 6. Operator Signature Table

| Operator | Signature Type | Norm | Physical Meaning |
|----------|---------------|------|------------------|
| IS       | Lightlike boundary | ‖IS‖² = 0 | Identity/equilibrium |
| OF       | Lightlike carrier | ‖OF‖² = 0 | Relation/projection |
| IF       | Spacelike test | ‖IF‖² > 0 | Branch/measurement |
| THEN     | Timelike flow | ‖THEN‖² < 0 | Causality/sequence |
| ELSE     | Lightlike handler | ‖ELSE‖² = 0 | Boundary/default |
| NOT      | Signature flip | ‖NOT(x)‖² = -‖x‖² | Negation/reflection |
| AND      | Spacelike intersection | ‖AND‖² > 0 | Conjunction/constraint |
| OR       | Spacelike union | ‖OR‖² > 0 | Disjunction/alternative |

---

## 7. Examples

### Example 1: IS = OF at equilibrium
```eigenscript
x is y               # equilibrium: ‖x of y‖² = 0
result of (x of y)   # projection: x^⊤ g y

# At equilibrium, they converge:
(x is y) = (‖x of y‖² = 0)
```

### Example 2: IF = equilibrium test
```eigenscript
if condition:        # test ‖condition‖²
    do_this          # execute if ‖condition‖² > 0
else:
    do_that          # execute if ‖condition‖² = 0
```

### Example 3: NOT = equilibrium flip
```eigenscript
not true             # ‖true‖² > 0 → ‖not true‖² = 0
not false            # ‖false‖² = 0 → ‖not false‖² > 0
```

### Example 4: AND/OR = multi-equilibrium
```eigenscript
A and B              # both must be non-equilibrium
A or B               # at least one must be non-equilibrium
```

---

## 8. Summary

**All operators are unified**:

```
Equilibrium is the primitive.

IS  = equilibrium state
OF  = equilibrium projection
IF  = equilibrium test
NOT = equilibrium inversion
AND = equilibrium conjunction
OR  = equilibrium disjunction
THEN = equilibrium sequence
ELSE = equilibrium boundary

Everything reduces to:
  - Testing equilibrium (norm = 0?)
  - Projecting equilibrium (through metric g)
  - Composing equilibrium (geodesic flow)
  - Inverting equilibrium (signature flip)
```

**This is the foundation of EigenScript.**

Logic, control flow, identity, relation, and geometry
all collapse into one system: **equilibrium dynamics**.

---

**Document Version**: 1.0
**Status**: Complete
**Foundation**: Operator Unification Theorem
