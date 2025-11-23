#!/usr/bin/env python3
"""
EigenScript Compiler CLI
Compile .eigs files to LLVM IR or native code
"""

import sys
import os
import argparse

from eigenscript.lexer import Tokenizer
from eigenscript.parser.ast_builder import Parser
from eigenscript.compiler.codegen.llvm_backend import LLVMCodeGenerator
from llvmlite import binding as llvm


def compile_file(
    input_file: str,
    output_file: str = None,
    emit_llvm: bool = True,
    verify: bool = True,
    link_exec: bool = False,
    opt_level: int = 0,
):
    """Compile an EigenScript file to LLVM IR, object code, or executable."""

    # Read source file
    try:
        with open(input_file, "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return 1
    except Exception as e:
        print(f"Error reading file: {e}")
        return 1

    # Determine output file
    if output_file is None:
        base = os.path.splitext(input_file)[0]
        output_file = f"{base}.ll" if emit_llvm else f"{base}.o"

    print(f"Compiling {input_file} -> {output_file}")

    try:
        # Tokenize
        tokenizer = Tokenizer(source_code)
        tokens = tokenizer.tokenize()
        print(f"  ✓ Tokenized: {len(tokens)} tokens")

        # Parse
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"  ✓ Parsed: {len(ast.statements)} statements")

        # Generate LLVM IR
        codegen = LLVMCodeGenerator()
        llvm_ir = codegen.compile(ast.statements)
        print(f"  ✓ Generated LLVM IR")

        # Parse and verify LLVM module
        llvm_module = llvm.parse_assembly(llvm_ir)
        if verify:
            try:
                llvm_module.verify()
                print(f"  ✓ Verification passed")
            except Exception as verify_error:
                print(f"  ✗ Verification failed: {verify_error}")
                return 1

        # Link runtime bitcode for LTO (Link-Time Optimization)
        # This enables inlining of C runtime functions
        llvm_module = codegen.link_runtime_bitcode(llvm_module)
        print(f"  ✓ Linked runtime bitcode (LTO enabled)")

        # Apply optimizations if requested (using New Pass Manager)
        if opt_level > 0:
            # Create pipeline tuning options
            pto = llvm.create_pipeline_tuning_options()
            pto.speed_level = opt_level  # 0-3: optimization level
            pto.size_level = 0  # Optimize for speed, not size

            # Enable function inlining at all levels
            # This is crucial for EigenScript since runtime calls are frequent
            pto.inline_threshold = 225  # Default LLVM inline threshold

            # Tune inlining aggressiveness based on opt level
            if opt_level == 1:
                # -O1: Conservative inlining (small functions only)
                pto.inline_threshold = 75
            elif opt_level == 2:
                # -O2: Standard inlining (balanced)
                pto.inline_threshold = 225
            elif opt_level == 3:
                # -O3: Aggressive inlining (may increase code size)
                pto.inline_threshold = 375

            # Enable vectorization for O2 and above
            # Trade-off: Better throughput, but larger binaries
            if opt_level >= 2:
                pto.loop_vectorization = True  # Vectorize loops
                pto.slp_vectorization = True  # Vectorize straight-line code
                pto.loop_interleaving = True  # Unroll and interleave loops
                pto.loop_unrolling = True  # Unroll small loops

            # Create target machine for context-aware optimization
            target = llvm.Target.from_default_triple()
            target_machine = target.create_target_machine()

            # Create pass builder and get optimization pipeline
            pass_builder = llvm.create_pass_builder(target_machine, pto)
            mpm = pass_builder.getModulePassManager()

            # Run optimizations (pass_builder needed for context)
            mpm.run(llvm_module, pass_builder)

            # Print optimization summary
            opt_features = []
            if opt_level >= 1:
                opt_features.append("inlining")
            if opt_level >= 2:
                opt_features.append("vectorization")
            if opt_level >= 3:
                opt_features.append("aggressive")
            print(f"  ✓ Optimized (level {opt_level}: {', '.join(opt_features)})")

            # Get optimized IR
            llvm_ir = str(llvm_module)

        # Emit output
        if emit_llvm:
            # Save LLVM IR
            with open(output_file, "w") as f:
                f.write(llvm_ir)
            print(f"  ✓ Written to {output_file}")
        else:
            # Compile to object file
            llvm_module = llvm.parse_assembly(llvm_ir)
            llvm_module.verify()

            target = llvm.Target.from_default_triple()
            target_machine = target.create_target_machine()

            with open(output_file, "wb") as f:
                f.write(target_machine.emit_object(llvm_module))
            print(f"  ✓ Compiled to {output_file}")

        # Link to executable if requested
        if link_exec:
            base = os.path.splitext(input_file)[0]
            obj_file = f"{base}.o" if emit_llvm else output_file
            exec_file = f"{base}.exe"

            # If we emitted LLVM, first compile to object
            if emit_llvm:
                llvm_module = llvm.parse_assembly(llvm_ir)
                llvm_module.verify()
                target = llvm.Target.from_default_triple()
                target_machine = target.create_target_machine()
                with open(obj_file, "wb") as f:
                    f.write(target_machine.emit_object(llvm_module))

            # Ensure runtime is compiled
            import subprocess

            runtime_dir = os.path.join(os.path.dirname(__file__), "../runtime")
            runtime_c = os.path.join(runtime_dir, "eigenvalue.c")
            runtime_o = os.path.join(runtime_dir, "eigenvalue.o")

            # Compile runtime if needed
            if not os.path.exists(runtime_o) or os.path.getmtime(
                runtime_c
            ) > os.path.getmtime(runtime_o):
                print(f"  → Compiling runtime library...")
                result = subprocess.run(
                    ["gcc", "-c", runtime_c, "-o", runtime_o, "-fPIC"],
                    capture_output=True,
                    text=True,
                    cwd=runtime_dir,
                )
                if result.returncode != 0:
                    print(f"  ✗ Runtime compilation failed: {result.stderr}")
                    return 1

            # Link with runtime (NO shell=True to prevent command injection)
            result = subprocess.run(
                ["gcc", obj_file, runtime_o, "-o", exec_file, "-lm"],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print(f"  ✓ Linked to {exec_file}")
            else:
                print(f"  ✗ Linking failed: {result.stderr}")
                return 1

        print(f"\n✅ Compilation successful!")
        return 0

    except Exception as e:
        print(f"\n❌ Compilation failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="EigenScript Compiler - Compile .eigs files to LLVM IR or native code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s program.eigs              # Compile to LLVM IR (program.ll)
  %(prog)s program.eigs -o out.ll    # Specify output file
  %(prog)s program.eigs --obj        # Compile to object file (program.o)
  %(prog)s program.eigs --exec       # Compile and link to executable (program.exe)
  %(prog)s program.eigs -O2 --exec   # Compile with -O2 optimizations
  %(prog)s program.eigs --no-verify  # Skip verification
        """,
    )

    parser.add_argument("input", help="Input EigenScript file (.eigs)")
    parser.add_argument(
        "-o", "--output", help="Output file (default: input with .ll or .o extension)"
    )
    parser.add_argument(
        "--obj", action="store_true", help="Compile to object file instead of LLVM IR"
    )
    parser.add_argument(
        "--exec", action="store_true", help="Compile and link to executable"
    )
    parser.add_argument(
        "--no-verify", action="store_true", help="Skip LLVM module verification"
    )
    parser.add_argument(
        "-O",
        "--optimize",
        type=int,
        choices=[0, 1, 2, 3],
        default=0,
        help="""Optimization level:
  0 = No optimization (fast compile, slower execution)
  1 = Basic optimizations (conservative inlining, small code size increase)
  2 = Standard optimizations (balanced inlining + vectorization, ~2-5x faster) [RECOMMENDED]
  3 = Aggressive optimizations (heavy inlining, large code size, ~2-10x faster)""",
    )

    args = parser.parse_args()

    # Compile
    exit_code = compile_file(
        input_file=args.input,
        output_file=args.output,
        emit_llvm=not args.obj,
        verify=not args.no_verify,
        link_exec=args.exec,
        opt_level=args.optimize,
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
