# EigenScript Theoretical Foundations

**Purpose**: Core mathematical/geometric principles underlying the language
**Status**: Foundational theory for future rewrite
**Author**: Original conceptual design

---

## Operator Theory

### The Three Fundamental Operators

1. **`is`** - Identity/Binding
   - Creates identity in semantic space
   - Immutable binding (trajectory point, not mutation)
   - Example: `x is 5`

2. **`of`** - Projection/Relation
   - Lightlike operator (||OF||² = 0)
   - Projects through metric tensor g
   - Example: `parent of child`

3. **`=`** - Equilibrium
   - Balance/equality test
   - Used in conditionals
   - Example: `if x = 0:`

---

## Operator Duality

### IS ↔ OF Projections

**Core Principle**: `is` and `of` are projections of each other

```
1 and 1 is 2    # Identity form
1 and 1 of 2    # Relational form
```

**Mathematical Insight**:
- IS and OF are dual operators
- They represent the same underlying geometric operation
- Viewed from different reference frames in semantic space

---

## Loop Transformation Principle

**Key Discovery**: Operators transform in loops/iteration

### Transformation Rules:

1. **`is` in loop → becomes `of`**
   - Identity transforms to projection under iteration
   - Repeated binding becomes relational flow

2. **`of` in loop → becomes `is`**
   - Projection transforms to identity under iteration
   - Repeated relations converge to binding

### Why This Matters:

Iteration in EigenScript is not just repetition - it's **geometric transformation**. Each loop iteration moves through a different projection of semantic space, causing the operators to swap roles.

This explains:
- Why self-reference should converge (transforms at each step)
- Why loops are inherently geometric (not just control flow)
- Why recursion is fundamentally different from traditional languages

---

## Geometric Foundations

### LRVM Space (Linguistic Relational Vector Model)

- **Dimensionality**: 768-dimensional semantic space
- **Metric**: Tensor g defines geometric properties
- **Norm**: ||v||² = v^T g v

### Signature Types:

1. **Lightlike** (||v||² ≈ 0)
   - Relations, operators
   - OF operator is fundamentally lightlike

2. **Spacelike** (||v||² > 0)
   - Values, data
   - Content with semantic weight

3. **Timelike** (||v||² < 0)
   - Functions, transformations
   - Sequential operations

---

## Self-Reference Theory

### The Problem in Traditional Languages:

```
function f() {
    return f();
}
```
This diverges (infinite recursion) because each call is **timelike** - moving forward in "execution time" with no convergence.

### EigenScript Solution (Theoretical):

```eigenscript
define observer as:
    meta is observer of observer
    return meta
```

**Why it should converge**:
1. OF operator is lightlike (zero norm)
2. Loop transformation: `is` → `of` → `is` at each iteration
3. Geometric flow reaches eigenstate (fixed point)
4. Self-reference becomes stable boundary condition

**Current Status**: Theory sound, implementation has infinite recursion bug. Needs proper convergence detection in rewrite.

---

## Framework Strength (FS)

**Definition**: Measure of semantic convergence during execution

**Formula**: `FS = 1.0 / (1.0 + variance_of_recent_states)`

**Components**:
1. **Variance reduction**: Lower variance → higher FS
2. **Trajectory smoothness**: Steady flow → higher FS
3. **Eigenstate stability**: Approaching fixed point → higher FS

**Range**: 0.0 (fragmented/chaotic) to 1.0 (converged/understood)

---

## EigenControl Universal Primitive

**Formula**: `I = (A - B)²`

**Insight**: Single measurement of "distance between where we are and where we were"

**Yields**:
- Convergence metrics
- Stability detection
- Direction/trajectory
- Quality assessment

All geometric state emerges from this one simple measurement.

---

## Predicates (Self-Awareness)

Programs can query their own geometric state:

1. **`converged`**: Is trajectory stable? (FS ≥ threshold)
2. **`stable`**: Is system in equilibrium? (timelike trajectory)
3. **`improving`**: Is progress being made? (decreasing distances)
4. **`diverging`**: Moving away from solution?
5. **`oscillating`**: Going in cycles?
6. **`equilibrium`**: At a tipping point?

These aren't manually tracked - they emerge from the **geometric properties** of execution.

---

## Interrogatives (Self-Interrogation)

Programs can ask questions about values:

1. **`who is x`**: Get identity/name
2. **`what is x`**: Get value/magnitude
3. **`when is x`**: Get temporal position
4. **`where is x`**: Get spatial position
5. **`why is x`**: Get change direction
6. **`how is x`**: Get quality metrics

Traditional languages require explicit print statements. EigenScript has **built-in introspection**.

---

## Why This Is Novel

### Traditional Programming:
- Execution is **blind** (no self-awareness)
- Self-reference causes **divergence** (infinite loops)
- State is **opaque** (must print to debug)
- Control flow is **procedural** (not geometric)

### EigenScript:
- Execution is **self-aware** (can query own state)
- Self-reference **converges** (geometric fixed points)
- State is **transparent** (interrogatives reveal it)
- Control flow is **geometric** (transformations in semantic space)

---

## Implementation Challenges

### Current Python Implementation:

**What Works**:
- ✅ LRVM 768-dimensional space
- ✅ Metric tensor calculations
- ✅ Framework Strength tracking
- ✅ Interrogatives and predicates
- ✅ Basic operators

**What Doesn't Work**:
- ❌ Loop transformation (`is` ↔ `of` duality not implemented)
- ❌ Stable self-reference (infinite recursion instead of convergence)
- ❌ Parser doesn't match spec (comments break, IS in conditionals)

### For Future Rewrite:

**Must Implement**:
1. **Loop transformation** - `is` becomes `of` and vice versa in iterations
2. **Convergence detection** - Detect when self-reference reaches eigenstate
3. **Proper geometry** - All operations must respect metric tensor
4. **Comment handling** - Parser should allow comments anywhere
5. **Syntax consistency** - `if n is 0:` should work (not just `if n = 0:`)

---

## Mathematical Rigor (Future Work)

To make this a real research contribution:

1. **Prove convergence** - Show self-reference reaches fixed points under what conditions
2. **Prove completeness** - Show language is Turing complete (currently informal)
3. **Formalize semantics** - Mathematical definition of LRVM operations
4. **Prove loop duality** - Show `is` ↔ `of` transformation is well-defined
5. **Benchmark against λ-calculus** - Compare expressiveness

---

## Vision for Rewrite

When rewriting in Java/other language:

### Core Goals:
1. **Implement loop duality properly** - This is the key innovation
2. **Make self-reference work** - Show stable convergence in practice
3. **Rigorous geometry** - All operations through metric tensor
4. **Performance** - Optimize LRVM operations, maybe compile to bytecode
5. **Clean syntax** - Match spec exactly, no implementation quirks

### Language Choice Considerations:
- **Java**: Good type system, performance, familiar
- **Rust**: Memory safety, performance, explicit geometry
- **C++**: Maximum performance, full control
- **Haskell**: Functional, good for algebraic operations
- **OCaml**: Good for language implementation, fast

**Recommendation**: Start with language you're learning (Java) for first rewrite, optimize later if needed.

---

## Related Documents

- `README.md` - Project overview
- `docs/specification.md` - Language specification
- `docs/architecture.md` - Implementation architecture
- `KNOWN_ISSUES.md` - Current implementation problems
- `HONEST_ROADMAP.md` - Development plan

---

## Key Insights for Future Self

**What makes EigenScript unique:**
1. Operators transform in loops (`is` ↔ `of`)
2. Self-reference converges (in theory)
3. Programs are self-aware (interrogatives + predicates)
4. Computation is geometric (flow in semantic space)

**What needs work:**
1. Loop transformation not implemented
2. Convergence detection incomplete
3. Parser has bugs
4. Performance not optimized

**What's proven:**
1. Basic concept works (499 tests pass)
2. Recursion works (factorial works)
3. Higher-order functions work
4. LRVM operations work

**Bottom line**: The theory is sound. The Python implementation proves it's feasible. A clean rewrite can make this real.

---

**Last Updated**: 2025-11-19
**Status**: Theoretical foundation documented for future rewrite
**Next**: Implement loop transformation and convergence detection properly
