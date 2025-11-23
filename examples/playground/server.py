#!/usr/bin/env python3
"""
EigenSpace Compilation Server
Hosts the compiler as a local API for the interactive playground.
"""

import http.server
import socketserver
import json
import subprocess
import os
import sys
import tempfile
import shutil
from pathlib import Path

PORT = 8080
# Find paths relative to this file's location
SCRIPT_DIR = Path(__file__).parent
COMPILER_PATH = SCRIPT_DIR / "../../src/eigenscript/compiler/cli/compile.py"
RUNTIME_DIR = SCRIPT_DIR / "../../src/eigenscript/compiler/runtime"


class CompilerHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that compiles EigenScript code to WebAssembly."""
    
    def end_headers(self):
        """Add CORS headers to allow frontend requests."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests."""
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/compile':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            source_code = data.get('code', '')

            # Create temp directory for compilation
            with tempfile.TemporaryDirectory() as tmpdir:
                source_file = os.path.join(tmpdir, "main.eigs")
                wasm_file = os.path.join(tmpdir, "main.wasm")
                
                # Write source
                with open(source_file, "w") as f:
                    f.write(source_code)
                
                # Run Compiler
                # Use eigenscript-compile if installed, otherwise use direct Python invocation
                try:
                    # First try using the installed CLI
                    cmd = [
                        "eigenscript-compile",
                        source_file,
                        "--target", "wasm32-unknown-unknown",
                        "--exec",
                        "-o", wasm_file
                    ]
                    
                    print(f"🔨 Compiling: {' '.join(cmd)}")
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=tmpdir)
                except FileNotFoundError:
                    # Fallback to direct Python invocation
                    cmd = [
                        sys.executable, str(COMPILER_PATH.resolve()),
                        source_file,
                        "--target", "wasm32-unknown-unknown",
                        "--exec",
                        "-o", wasm_file
                    ]
                    
                    print(f"🔨 Compiling: {' '.join(cmd)}")
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=tmpdir)
                
                if result.returncode != 0:
                    # Compilation Failed
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    error_message = result.stderr if result.stderr else result.stdout
                    response = {"error": error_message}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    print(f"❌ Compilation failed: {error_message}")
                else:
                    # Compilation Success
                    if os.path.exists(wasm_file):
                        with open(wasm_file, "rb") as f:
                            wasm_bytes = f.read()
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/wasm')
                        self.end_headers()
                        self.wfile.write(wasm_bytes)
                        print(f"✅ Compilation successful! Generated {len(wasm_bytes)} bytes")
                    else:
                        # WASM file wasn't created
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {"error": "Compilation succeeded but WASM file not found"}
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                        print(f"❌ WASM file not found after compilation")
        else:
            # Serve static files from the playground directory
            super().do_GET()


def main():
    """Start the EigenSpace compilation server."""
    print("=" * 60)
    print("🚀 EigenSpace Compilation Server")
    print("=" * 60)
    print(f"📍 Server running at http://localhost:{PORT}")
    print(f"📂 Serving files from: {SCRIPT_DIR.resolve()}")
    print(f"🔧 Compiler: {COMPILER_PATH.resolve()}")
    print(f"⚙️  Runtime: {RUNTIME_DIR.resolve()}")
    print()
    print("📋 Endpoints:")
    print(f"   • POST /compile - Compile EigenScript to WASM")
    print(f"   • GET  /        - Serve playground HTML")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Change to the playground directory so static files are served correctly
    os.chdir(SCRIPT_DIR)
    
    try:
        with socketserver.TCPServer(("", PORT), CompilerHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()
