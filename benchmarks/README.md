# EigenScript Benchmarks

This directory contains benchmark scripts for measuring EigenScript performance.

## Running Benchmarks

To run a benchmark, use the `--benchmark` or `-b` flag:

```bash
python -m eigenscript benchmarks/factorial_bench.eigs --benchmark
```

## Available Benchmarks

- `factorial_bench.eigs` - Recursive factorial computation
- `fibonacci_bench.eigs` - Recursive Fibonacci sequence
- `list_operations_bench.eigs` - List manipulation and higher-order functions
- `math_bench.eigs` - Mathematical functions performance
- `loop_bench.eigs` - Loop and iteration performance

## Benchmark Output

The benchmark flag provides:
- **Execution Time**: Total time to run the program
- **Peak Memory**: Maximum memory used during execution
- **Source Lines**: Number of lines in the source file
- **Tokens**: Number of tokens parsed

## Tips

1. Run multiple times to account for variance
2. Use larger inputs for more stable timing measurements
3. Compare similar algorithms to evaluate performance trade-offs
4. Consider using `--verbose` for additional execution details
