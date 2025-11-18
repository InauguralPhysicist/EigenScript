# Phase 6 Implementation Guide: Essential Features

**Goal**: Add critical features for real-world EigenScript adoption

**Duration**: 12 weeks (Q1 2025)

**Priority**: Critical path for "anything another language can do"

---

## Overview

This guide provides detailed technical specifications for implementing the highest-priority features in Phase 6:

1. File I/O Operations (Sprints 1-2)
2. Error Handling System (Sprints 3-4)
3. JSON and Serialization (Sprints 5-6)
4. Advanced Data Structures (Sprints 7-9)
5. Standard Library Math & Collections (Sprints 10-12)

---

## 1. File I/O Operations (Sprints 1-2: 2 weeks)

### Goal
Enable EigenScript programs to read/write files, check file existence, and traverse directories.

### API Design

#### Core Functions

```eigenscript
# Read entire file as string
content is read_file of "data.txt"

# Read file as lines
lines is read_lines of "data.txt"

# Write string to file
write_file of ["output.txt", "Hello, World!"]

# Append to file
append_file of ["log.txt", "New log entry\n"]

# Read binary file
bytes is read_bytes of "image.png"

# Write binary file
write_bytes of ["output.bin", byte_data]

# Check if file exists
exists is file_exists of "config.json"

# Get file info
info is file_info of "document.pdf"
# Returns: {size: 1024, modified: timestamp, created: timestamp}

# Delete file
delete_file of "temp.txt"

# List directory
files is list_dir of "."
files is list_dir of "/home/user"

# Create directory
make_dir of "new_folder"

# Join paths (platform-independent)
path is path_join of ["folder", "subfolder", "file.txt"]

# Get file extension
ext is path_ext of "document.pdf"  # ".pdf"

# Get filename without extension
name is path_name of "document.pdf"  # "document"

# Get absolute path
abs is path_abs of "relative/path.txt"
```

### Implementation Details

#### File: `src/eigenscript/builtins_io.py`

```python
"""
File I/O built-in functions for EigenScript.
"""
import os
from pathlib import Path
from typing import Any
from eigenscript.semantic.lrvm import LRVMVector, LRVMSpace
from eigenscript.builtins import BuiltinFunction, decode_vector


def builtin_read_file(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Read entire file as string.
    
    Example:
        content is read_file of "data.txt"
    """
    filename = decode_vector(arg, space, metric)
    
    if not isinstance(filename, str):
        raise TypeError(f"read_file requires a string filename")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return space.embed_string(content)
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {filename}")
    except PermissionError:
        raise RuntimeError(f"Permission denied: {filename}")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")


def builtin_read_lines(arg: LRVMVector, space: LRVMSpace, metric: Any = None):
    """
    Read file as list of lines.
    
    Example:
        lines is read_lines of "data.txt"
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    filename = decode_vector(arg, space, metric)
    
    if not isinstance(filename, str):
        raise TypeError(f"read_lines requires a string filename")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Convert lines to LRVM vectors (strip newlines)
        line_vectors = [space.embed_string(line.rstrip('\n')) for line in lines]
        return EigenList(line_vectors)
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {filename}")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")


def builtin_write_file(args, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Write string to file.
    
    Example:
        write_file of ["output.txt", "Hello, World!"]
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    if not isinstance(args, EigenList) or len(args.elements) != 2:
        raise TypeError("write_file requires [filename, content]")
    
    filename = decode_vector(args.elements[0], space, metric)
    content = decode_vector(args.elements[1], space, metric)
    
    if not isinstance(filename, str):
        raise TypeError("Filename must be a string")
    
    if not isinstance(content, str):
        # Convert to string
        content = str(content)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return space.zero_vector()
    except PermissionError:
        raise RuntimeError(f"Permission denied: {filename}")
    except Exception as e:
        raise RuntimeError(f"Error writing file: {e}")


def builtin_append_file(args, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """Append string to file."""
    from eigenscript.evaluator.interpreter import EigenList
    
    if not isinstance(args, EigenList) or len(args.elements) != 2:
        raise TypeError("append_file requires [filename, content]")
    
    filename = decode_vector(args.elements[0], space, metric)
    content = decode_vector(args.elements[1], space, metric)
    
    if not isinstance(filename, str):
        raise TypeError("Filename must be a string")
    
    if not isinstance(content, str):
        content = str(content)
    
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(content)
        return space.zero_vector()
    except Exception as e:
        raise RuntimeError(f"Error appending to file: {e}")


def builtin_file_exists(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Check if file exists.
    
    Example:
        exists is file_exists of "config.json"
    """
    filename = decode_vector(arg, space, metric)
    
    if not isinstance(filename, str):
        raise TypeError("file_exists requires a string filename")
    
    exists = os.path.exists(filename)
    return space.embed_scalar(1.0 if exists else 0.0)


def builtin_list_dir(arg: LRVMVector, space: LRVMSpace, metric: Any = None):
    """
    List files in directory.
    
    Example:
        files is list_dir of "."
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    dirname = decode_vector(arg, space, metric)
    
    if not isinstance(dirname, str):
        raise TypeError("list_dir requires a string directory path")
    
    try:
        entries = os.listdir(dirname)
        entry_vectors = [space.embed_string(entry) for entry in sorted(entries)]
        return EigenList(entry_vectors)
    except FileNotFoundError:
        raise RuntimeError(f"Directory not found: {dirname}")
    except PermissionError:
        raise RuntimeError(f"Permission denied: {dirname}")
    except Exception as e:
        raise RuntimeError(f"Error listing directory: {e}")


def builtin_make_dir(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """Create a directory."""
    dirname = decode_vector(arg, space, metric)
    
    if not isinstance(dirname, str):
        raise TypeError("make_dir requires a string directory path")
    
    try:
        os.makedirs(dirname, exist_ok=True)
        return space.zero_vector()
    except Exception as e:
        raise RuntimeError(f"Error creating directory: {e}")


def builtin_delete_file(arg: LRVMVector, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """Delete a file."""
    filename = decode_vector(arg, space, metric)
    
    if not isinstance(filename, str):
        raise TypeError("delete_file requires a string filename")
    
    try:
        os.remove(filename)
        return space.zero_vector()
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {filename}")
    except Exception as e:
        raise RuntimeError(f"Error deleting file: {e}")


def builtin_path_join(args, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """Join path components."""
    from eigenscript.evaluator.interpreter import EigenList
    
    if not isinstance(args, EigenList):
        raise TypeError("path_join requires a list of path components")
    
    components = []
    for elem in args.elements:
        component = decode_vector(elem, space, metric)
        if not isinstance(component, str):
            raise TypeError("All path components must be strings")
        components.append(component)
    
    joined_path = os.path.join(*components)
    return space.embed_string(joined_path)


def get_io_builtins(space: LRVMSpace) -> dict:
    """Get file I/O built-in functions."""
    return {
        "read_file": BuiltinFunction("read_file", builtin_read_file, "Read file as string"),
        "read_lines": BuiltinFunction("read_lines", builtin_read_lines, "Read file as list of lines"),
        "write_file": BuiltinFunction("write_file", builtin_write_file, "Write string to file"),
        "append_file": BuiltinFunction("append_file", builtin_append_file, "Append to file"),
        "file_exists": BuiltinFunction("file_exists", builtin_file_exists, "Check if file exists"),
        "list_dir": BuiltinFunction("list_dir", builtin_list_dir, "List directory contents"),
        "make_dir": BuiltinFunction("make_dir", builtin_make_dir, "Create directory"),
        "delete_file": BuiltinFunction("delete_file", builtin_delete_file, "Delete file"),
        "path_join": BuiltinFunction("path_join", builtin_path_join, "Join path components"),
    }
```

#### Integration

Update `src/eigenscript/builtins.py`:
```python
from eigenscript.builtins_io import get_io_builtins

def get_builtins(space: LRVMSpace) -> dict:
    """Get all built-in functions."""
    builtins = {
        # Existing builtins...
    }
    
    # Add I/O builtins
    builtins.update(get_io_builtins(space))
    
    return builtins
```

### Testing

#### File: `tests/test_file_io.py`

```python
"""Tests for file I/O operations."""
import pytest
import tempfile
import os
from pathlib import Path
from eigenscript.evaluator import Interpreter


class TestFileIO:
    """Test file I/O operations."""
    
    def test_write_and_read_file(self, tmp_path):
        """Test writing and reading a file."""
        code = f'''
        filepath is "{tmp_path}/test.txt"
        content is "Hello, EigenScript!"
        
        write_file of [filepath, content]
        read_content is read_file of filepath
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Check that file was created
        assert (tmp_path / "test.txt").exists()
        
        # Check that content was read correctly
        read_content = interpreter.environment.lookup("read_content")
        # Decode and verify
    
    def test_read_lines(self, tmp_path):
        """Test reading file as lines."""
        # Create test file
        test_file = tmp_path / "lines.txt"
        test_file.write_text("line1\nline2\nline3\n")
        
        code = f'''
        lines is read_lines of "{test_file}"
        count is len of lines
        first is lines[0]
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify count
        # Verify first line
    
    def test_file_exists(self, tmp_path):
        """Test file existence checking."""
        test_file = tmp_path / "exists.txt"
        test_file.write_text("content")
        
        code = f'''
        exists1 is file_exists of "{test_file}"
        exists2 is file_exists of "{tmp_path}/nonexistent.txt"
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify exists1 is true, exists2 is false
    
    def test_list_dir(self, tmp_path):
        """Test directory listing."""
        # Create test files
        (tmp_path / "file1.txt").write_text("content")
        (tmp_path / "file2.txt").write_text("content")
        
        code = f'''
        files is list_dir of "{tmp_path}"
        count is len of files
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify count >= 2
```

### Deliverables

✅ Sprints 1-2 Complete When:
- [ ] All I/O functions implemented in `builtins_io.py`
- [ ] Functions integrated into main builtins
- [ ] Comprehensive test suite passing (>90% coverage)
- [ ] Documentation updated with examples
- [ ] Example programs using file I/O

---

## 2. Error Handling System (Sprints 3-4: 3 weeks)

### Goal
Add try/catch/finally blocks and integrate with EigenScript's geometric error detection.

### Syntax Design

```eigenscript
# Basic try/catch
try:
    result is risky_operation of data
catch:
    print of "An error occurred"
    result is null

# Catch specific error types
try:
    value is parse_int of "not_a_number"
catch ValueError:
    print of "Invalid integer"
catch:
    print of "Unknown error"

# Finally block (always executes)
try:
    file is open_file of "data.txt"
    process of file
catch:
    print of "Error processing file"
finally:
    close_file of file

# Geometric error handling
try:
    result is complex_calculation of data
    
    # Check geometric properties
    if diverging:
        raise of "Computation diverging"
    
    return result
catch GeometricError:
    print of "Geometric computation failed"
    return null
```

### AST Nodes

#### File: `src/eigenscript/parser/ast_builder.py`

Add new node types:

```python
@dataclass
class TryStatement:
    """Try/catch/finally statement."""
    try_block: List[Statement]
    catch_clauses: List['CatchClause']
    finally_block: Optional[List[Statement]] = None

@dataclass
class CatchClause:
    """Catch clause in try/catch."""
    error_type: Optional[str] = None  # None means catch all
    error_var: Optional[str] = None   # Variable to bind error to
    block: List[Statement] = field(default_factory=list)

@dataclass
class RaiseStatement:
    """Raise an error."""
    error: Expression  # Error message or object
```

### Error Types

#### File: `src/eigenscript/errors.py`

```python
"""
EigenScript error types.
"""

class EigenScriptError(Exception):
    """Base class for EigenScript errors."""
    pass

class RuntimeError(EigenScriptError):
    """Runtime error."""
    pass

class TypeError(EigenScriptError):
    """Type error."""
    pass

class ValueError(EigenScriptError):
    """Value error."""
    pass

class FileError(EigenScriptError):
    """File I/O error."""
    pass

class GeometricError(EigenScriptError):
    """Error related to geometric computation."""
    
    def __init__(self, message: str, divergence_metric: float = None):
        super().__init__(message)
        self.divergence_metric = divergence_metric
```

### Interpreter Integration

#### File: `src/eigenscript/evaluator/interpreter.py`

Add try/catch evaluation:

```python
def _eval_try_statement(self, node: TryStatement) -> LRVMVector:
    """
    Evaluate try/catch/finally statement.
    """
    result = self.space.zero_vector()
    error_caught = False
    
    try:
        # Execute try block
        for stmt in node.try_block:
            result = self.eval(stmt)
        
    except Exception as e:
        # Try to match with catch clauses
        for catch_clause in node.catch_clauses:
            if catch_clause.error_type is None:
                # Catch all
                error_caught = True
            else:
                # Check if error matches type
                error_class = self._get_error_class(catch_clause.error_type)
                if isinstance(e, error_class):
                    error_caught = True
            
            if error_caught:
                # Bind error to variable if specified
                if catch_clause.error_var:
                    error_message = str(e)
                    error_vector = self.space.embed_string(error_message)
                    self.environment.bind(catch_clause.error_var, error_vector)
                
                # Execute catch block
                for stmt in catch_clause.block:
                    result = self.eval(stmt)
                break
        
        # If no catch clause matched, re-raise
        if not error_caught:
            raise
    
    finally:
        # Always execute finally block
        if node.finally_block:
            for stmt in node.finally_block:
                self.eval(stmt)
    
    return result


def _get_error_class(self, error_type: str):
    """Map error type name to Python class."""
    from eigenscript import errors
    
    error_map = {
        'RuntimeError': errors.RuntimeError,
        'TypeError': errors.TypeError,
        'ValueError': errors.ValueError,
        'FileError': errors.FileError,
        'GeometricError': errors.GeometricError,
    }
    
    return error_map.get(error_type, Exception)


def _eval_raise_statement(self, node: RaiseStatement) -> LRVMVector:
    """Raise an error."""
    error_msg_vector = self.eval(node.error)
    error_msg = decode_vector(error_msg_vector, self.space, self.metric)
    
    # Check if this is a geometric error (diverging computation)
    if self.framework_strength < 0.5:  # Arbitrary threshold
        raise errors.GeometricError(
            str(error_msg),
            divergence_metric=1.0 - self.framework_strength
        )
    else:
        raise errors.RuntimeError(str(error_msg))
```

### Geometric Error Detection

Integrate with semantic predicates:

```eigenscript
define safe_compute as:
    try:
        result is complex_calculation of data
        
        # Geometric error detection
        if diverging:
            raise of "Computation is diverging"
        
        if oscillating:
            raise of "Computation is oscillating"
        
        if not converged:
            print of "Warning: Not yet converged"
        
        return result
        
    catch GeometricError as err:
        print of "Geometric error detected"
        print of err
        return null
```

### Testing

#### File: `tests/test_error_handling.py`

```python
"""Tests for error handling."""
import pytest
from eigenscript.evaluator import Interpreter
from eigenscript import errors


class TestErrorHandling:
    """Test try/catch/finally."""
    
    def test_basic_try_catch(self):
        """Test basic try/catch."""
        code = '''
        try:
            x is 10 / 0
        catch:
            x is -1
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # x should be -1 (error was caught)
    
    def test_specific_error_type(self):
        """Test catching specific error types."""
        code = '''
        try:
            x is parse_int of "not_a_number"
        catch ValueError:
            x is 0
        catch:
            x is -1
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # x should be 0 (ValueError caught)
    
    def test_finally_block(self):
        """Test finally block execution."""
        code = '''
        executed is 0
        
        try:
            x is 10
        finally:
            executed is 1
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # executed should be 1
    
    def test_geometric_error(self):
        """Test geometric error detection."""
        code = '''
        define divergent_compute as:
            # Simulate divergent computation
            x is n * 1000
            if diverging:
                raise of "Divergence detected"
            return x
        
        try:
            result is divergent_compute of 5
        catch GeometricError:
            result is null
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Should catch geometric error
```

### Deliverables

✅ Sprints 3-4 Complete When:
- [ ] TRY/CATCH/FINALLY syntax implemented
- [ ] Error types defined
- [ ] Geometric error detection integrated
- [ ] Test suite passing (>85% coverage)
- [ ] Documentation with examples

---

## 3. JSON and Serialization (Sprints 5-6: 2 weeks)

### Goal
Enable parsing and generating JSON, CSV, and EigenScript native format.

### API Design

```eigenscript
# Parse JSON
json_str is '{"name": "Alice", "age": 30, "active": true}'
data is parse_json of json_str
name is data["name"]
age is data["age"]

# Generate JSON
person is {name: "Bob", age: 25, active: true}
json_output is to_json of person

# Pretty print JSON
pretty_json is to_json_pretty of person

# Parse CSV
csv_data is read_csv of "data.csv"
first_row is csv_data[0]

# Write CSV
rows is [[1, 2, 3], [4, 5, 6]]
write_csv of ["output.csv", rows]

# EigenScript native serialization (preserves geometric metadata)
data is {x: 10, y: 20, z: 30}
serialized is eigen_serialize of data
write_file of ["data.eigen", serialized]

# Deserialize
loaded_data is eigen_deserialize of (read_file of "data.eigen")
```

### Implementation

#### File: `src/eigenscript/builtins_json.py`

```python
"""
JSON and serialization built-in functions.
"""
import json
import csv
from typing import Any
from eigenscript.semantic.lrvm import LRVMVector, LRVMSpace
from eigenscript.builtins import BuiltinFunction, decode_vector


def builtin_parse_json(arg: LRVMVector, space: LRVMSpace, metric: Any = None):
    """
    Parse JSON string to EigenScript data structure.
    """
    from eigenscript.evaluator.interpreter import EigenList
    
    json_str = decode_vector(arg, space, metric)
    
    if not isinstance(json_str, str):
        raise TypeError("parse_json requires a string")
    
    try:
        data = json.loads(json_str)
        return _python_to_eigen(data, space)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON: {e}")


def builtin_to_json(arg, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Convert EigenScript data to JSON string.
    """
    python_data = _eigen_to_python(arg, space, metric)
    
    try:
        json_str = json.dumps(python_data)
        return space.embed_string(json_str)
    except (TypeError, ValueError) as e:
        raise RuntimeError(f"Cannot serialize to JSON: {e}")


def builtin_to_json_pretty(arg, space: LRVMSpace, metric: Any = None) -> LRVMVector:
    """
    Convert EigenScript data to pretty-printed JSON.
    """
    python_data = _eigen_to_python(arg, space, metric)
    
    try:
        json_str = json.dumps(python_data, indent=2, sort_keys=True)
        return space.embed_string(json_str)
    except (TypeError, ValueError) as e:
        raise RuntimeError(f"Cannot serialize to JSON: {e}")


def _python_to_eigen(data: Any, space: LRVMSpace):
    """Convert Python data to EigenScript representation."""
    from eigenscript.evaluator.interpreter import EigenList
    
    if data is None:
        return space.zero_vector()
    elif isinstance(data, bool):
        return space.embed_scalar(1.0 if data else 0.0)
    elif isinstance(data, (int, float)):
        return space.embed_scalar(float(data))
    elif isinstance(data, str):
        return space.embed_string(data)
    elif isinstance(data, list):
        elements = [_python_to_eigen(item, space) for item in data]
        return EigenList(elements)
    elif isinstance(data, dict):
        # Represent dict as list of [key, value] pairs for now
        # TODO: Implement proper dictionary type in Sprint 7-9
        pairs = []
        for key, value in data.items():
            key_vec = space.embed_string(str(key))
            value_vec = _python_to_eigen(value, space)
            pairs.append(EigenList([key_vec, value_vec]))
        return EigenList(pairs)
    else:
        raise TypeError(f"Cannot convert {type(data)} to EigenScript")


def _eigen_to_python(data, space: LRVMSpace, metric: Any = None) -> Any:
    """Convert EigenScript data to Python for JSON serialization."""
    from eigenscript.evaluator.interpreter import EigenList
    
    if isinstance(data, EigenList):
        # Try to detect if this is a dictionary (list of [key, value] pairs)
        if len(data.elements) > 0:
            first = data.elements[0]
            if isinstance(first, EigenList) and len(first.elements) == 2:
                # Looks like a dictionary
                result = {}
                for pair in data.elements:
                    if isinstance(pair, EigenList) and len(pair.elements) == 2:
                        key = decode_vector(pair.elements[0], space, metric)
                        value = _eigen_to_python(pair.elements[1], space, metric)
                        result[str(key)] = value
                return result
        
        # Regular list
        return [_eigen_to_python(elem, space, metric) for elem in data.elements]
    else:
        # LRVM vector - decode to Python value
        return decode_vector(data, space, metric)


def get_json_builtins(space: LRVMSpace) -> dict:
    """Get JSON/serialization built-in functions."""
    return {
        "parse_json": BuiltinFunction("parse_json", builtin_parse_json, "Parse JSON string"),
        "to_json": BuiltinFunction("to_json", builtin_to_json, "Convert to JSON string"),
        "to_json_pretty": BuiltinFunction("to_json_pretty", builtin_to_json_pretty, "Convert to pretty JSON"),
    }
```

### Testing

#### File: `tests/test_json.py`

```python
"""Tests for JSON operations."""
import pytest
from eigenscript.evaluator import Interpreter


class TestJSON:
    """Test JSON parsing and generation."""
    
    def test_parse_json_object(self):
        """Test parsing JSON object."""
        code = '''
        json_str is '{"name": "Alice", "age": 30}'
        data is parse_json of json_str
        name is data["name"]
        age is data["age"]
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify name and age
    
    def test_parse_json_array(self):
        """Test parsing JSON array."""
        code = '''
        json_str is '[1, 2, 3, 4, 5]'
        data is parse_json of json_str
        count is len of data
        first is data[0]
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify count and first element
    
    def test_to_json(self):
        """Test generating JSON."""
        code = '''
        data is [1, 2, 3]
        json_str is to_json of data
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify JSON string
```

### Deliverables

✅ Sprints 5-6 Complete When:
- [ ] JSON parsing and generation working
- [ ] CSV support implemented
- [ ] Test suite passing (>85% coverage)
- [ ] Documentation with examples

---

## 4. Advanced Data Structures (Sprints 7-9: 3 weeks)

### Goal
Implement dictionaries, sets, and tuples with geometric foundations.

### Dictionary Design

```eigenscript
# Create dictionary
person is {name: "Alice", age: 30, city: "NYC"}

# Access by key
name is person["name"]
age is person["age"]

# Set value
person["email"] is "alice@example.com"

# Check if key exists
has_phone is "phone" in person  # false

# Get keys and values
keys is person.keys of null
values is person.values of null

# Iterate over dictionary
loop key in keys:
    value is person[key]
    print of key
    print of value

# Dictionary methods
size is person.size of null
person.remove of "city"
```

### Set Design

```eigenscript
# Create set
numbers is {1, 2, 3, 4, 5}
unique is set of [1, 2, 2, 3, 3, 3]  # Results in {1, 2, 3}

# Set operations
a is {1, 2, 3}
b is {3, 4, 5}

union is a.union of b        # {1, 2, 3, 4, 5}
intersection is a.intersect of b  # {3}
difference is a.diff of b    # {1, 2}

# Membership
contains is 2 in a  # true

# Add and remove
a.add of 6
a.remove of 1
```

### Tuple Design

```eigenscript
# Create tuple (immutable)
coords is (10, 20, 30)

# Access by index
x is coords[0]
y is coords[1]

# Cannot modify (error)
# coords[0] is 15  # ERROR: Tuples are immutable

# Unpack
(x, y, z) is coords
```

### Implementation Approach

Implement using geometric principles:
- **Dictionary**: Key-value pairs as tensor contractions
- **Set**: Unique elements via norm signatures
- **Tuple**: Immutable list (frozen LRVM vector)

#### File: `src/eigenscript/evaluator/structures.py`

```python
"""
Advanced data structures for EigenScript.
"""
from dataclasses import dataclass, field
from typing import List, Any, Dict as PyDict
from eigenscript.semantic.lrvm import LRVMVector, LRVMSpace


@dataclass
class EigenDict:
    """
    Dictionary (map) in EigenScript.
    
    Implemented as list of key-value pairs with geometric hashing.
    """
    pairs: List[tuple[LRVMVector, Any]] = field(default_factory=list)
    
    def get(self, key: LRVMVector, space: LRVMSpace, default: Any = None) -> Any:
        """Get value by key."""
        for k, v in self.pairs:
            # Check if keys are equal (geometric equality)
            if space.is_equal(k, key):
                return v
        return default
    
    def set(self, key: LRVMVector, value: Any) -> None:
        """Set value for key."""
        # Update existing key or add new pair
        for i, (k, v) in enumerate(self.pairs):
            if space.is_equal(k, key):
                self.pairs[i] = (key, value)
                return
        
        self.pairs.append((key, value))
    
    def contains(self, key: LRVMVector, space: LRVMSpace) -> bool:
        """Check if key exists."""
        return self.get(key, space) is not None
    
    def keys(self) -> List[LRVMVector]:
        """Get all keys."""
        return [k for k, v in self.pairs]
    
    def values(self) -> List[Any]:
        """Get all values."""
        return [v for k, v in self.pairs]


@dataclass
class EigenSet:
    """
    Set (unique collection) in EigenScript.
    
    Implemented using geometric norms for uniqueness.
    """
    elements: List[LRVMVector] = field(default_factory=list)
    
    def add(self, elem: LRVMVector, space: LRVMSpace) -> None:
        """Add element if not already present."""
        if not self.contains(elem, space):
            self.elements.append(elem)
    
    def contains(self, elem: LRVMVector, space: LRVMSpace) -> bool:
        """Check if element is in set."""
        for e in self.elements:
            if space.is_equal(e, elem):
                return True
        return False
    
    def remove(self, elem: LRVMVector, space: LRVMSpace) -> None:
        """Remove element from set."""
        self.elements = [e for e in self.elements if not space.is_equal(e, elem)]
    
    def union(self, other: 'EigenSet', space: LRVMSpace) -> 'EigenSet':
        """Union of two sets."""
        result = EigenSet(self.elements.copy())
        for elem in other.elements:
            result.add(elem, space)
        return result
    
    def intersection(self, other: 'EigenSet', space: LRVMSpace) -> 'EigenSet':
        """Intersection of two sets."""
        result = EigenSet()
        for elem in self.elements:
            if other.contains(elem, space):
                result.add(elem, space)
        return result


@dataclass
class EigenTuple:
    """
    Tuple (immutable sequence) in EigenScript.
    
    Like EigenList but immutable.
    """
    elements: tuple[LRVMVector, ...] = field(default_factory=tuple)
    
    def __getitem__(self, index: int) -> LRVMVector:
        """Get element by index."""
        return self.elements[index]
    
    def __len__(self) -> int:
        """Get length."""
        return len(self.elements)
    
    def __setitem__(self, index: int, value: LRVMVector):
        """Prevent modification."""
        raise RuntimeError("Tuples are immutable")
```

### Testing

#### File: `tests/test_data_structures.py`

```python
"""Tests for advanced data structures."""
import pytest
from eigenscript.evaluator import Interpreter


class TestDictionary:
    """Test dictionary operations."""
    
    def test_create_and_access(self):
        """Test creating and accessing dictionary."""
        code = '''
        person is {name: "Alice", age: 30}
        name is person["name"]
        age is person["age"]
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify name and age


class TestSet:
    """Test set operations."""
    
    def test_create_unique_set(self):
        """Test creating set removes duplicates."""
        code = '''
        numbers is {1, 2, 2, 3, 3, 3}
        count is len of numbers
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify count is 3


class TestTuple:
    """Test tuple operations."""
    
    def test_immutable_tuple(self):
        """Test that tuples cannot be modified."""
        code = '''
        coords is (10, 20, 30)
        try:
            coords[0] is 15
        catch:
            error_caught is 1
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify error was caught
```

### Deliverables

✅ Sprints 7-9 Complete When:
- [ ] Dictionary type implemented
- [ ] Set type implemented
- [ ] Tuple type implemented
- [ ] All operations working (get, set, add, remove, union, etc.)
- [ ] Test suite passing (>85% coverage)
- [ ] Documentation with examples

---

## 5. Standard Library Math & Collections (Sprints 10-12: 2 weeks)

### Goal
Expand standard library with essential math and collection utilities.

### Math Module

```eigenscript
use std:math

# Trigonometry
angle is math.sin of 1.57    # ~1.0
cos_val is math.cos of 0     # 1.0
tan_val is math.tan of 0.785 # ~1.0

# Logarithms and exponentials
log_val is math.log of 100    # ~4.605
log10_val is math.log10 of 100 # 2.0
exp_val is math.exp of 1      # ~2.718

# Powers and roots
pow_val is math.pow of [2, 8]  # 256
sqrt_val is math.sqrt of 16   # 4.0
cbrt_val is math.cbrt of 27   # 3.0

# Rounding
ceil_val is math.ceil of 3.2   # 4
floor_val is math.floor of 3.8 # 3
round_val is math.round of 3.5 # 4

# Constants
pi is math.PI
e is math.E

# Random
random_float is math.random of null        # [0, 1)
random_int is math.randint of [1, 10]      # [1, 10]
random_choice is math.choice of [1, 2, 3, 4, 5]

# Statistics
numbers is [1, 2, 3, 4, 5]
avg is math.mean of numbers        # 3.0
median_val is math.median of numbers # 3.0
variance is math.variance of numbers
std_dev is math.stdev of numbers
```

### Collections Module

```eigenscript
use std:collections

# Counter (frequency counting)
items is ["a", "b", "a", "c", "a", "b"]
counter is collections.Counter of items
# counter = {a: 3, b: 2, c: 1}

most_common is counter.most_common of 2
# [("a", 3), ("b", 2)]

# DefaultDict (with default values)
scores is collections.DefaultDict of 0
scores["alice"] is scores["alice"] + 10  # No key error

# OrderedDict (preserves insertion order)
ordered is collections.OrderedDict of null
ordered["first"] is 1
ordered["second"] is 2

# Deque (double-ended queue)
queue is collections.Deque of null
queue.append of 1
queue.appendleft of 0
first is queue.popleft of null
```

### Implementation Structure

```
src/eigenscript/stdlib/
├── __init__.py
├── math.py       # Math module
├── collections.py # Collections utilities
├── string.py     # String utilities (expand existing)
└── itertools.py  # Iteration utilities (future)
```

### Testing

#### File: `tests/test_stdlib_math.py`

```python
"""Tests for standard library math module."""
import pytest
import math as py_math
from eigenscript.evaluator import Interpreter


class TestMath:
    """Test math module functions."""
    
    def test_trigonometry(self):
        """Test trig functions."""
        code = '''
        use std:math
        
        sin_val is math.sin of 1.5708  # π/2
        cos_val is math.cos of 0
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify values are close to expected
    
    def test_statistics(self):
        """Test statistical functions."""
        code = '''
        use std:math
        
        numbers is [1, 2, 3, 4, 5]
        avg is math.mean of numbers
        median_val is math.median of numbers
        '''
        
        interpreter = Interpreter()
        interpreter.eval(code)
        
        # Verify mean is 3.0, median is 3.0
```

### Deliverables

✅ Sprints 10-12 Complete When:
- [ ] Math module implemented with all functions
- [ ] Collections utilities implemented
- [ ] Module system working (use std:math)
- [ ] Test suite passing (>85% coverage)
- [ ] Documentation with examples

---

## Phase 6 Success Criteria

At the end of 12 weeks, EigenScript will have:

1. ✅ **File I/O**: Read/write files, directory operations
2. ✅ **Error Handling**: Try/catch/finally with geometric errors
3. ✅ **JSON/CSV**: Parse and generate structured data
4. ✅ **Advanced Data Structures**: Dictionaries, sets, tuples
5. ✅ **Expanded Math Library**: Trig, log, exp, stats, random
6. ✅ **70% Feature Parity**: Can handle most real-world tasks

### Validation Examples

Create these example programs to validate Phase 6:

1. **Data Processing Pipeline**
```eigenscript
# Load CSV, transform, save as JSON
data is read_csv of "input.csv"
transformed is map of [process_row, data]
json_output is to_json_pretty of transformed
write_file of ["output.json", json_output]
```

2. **Error-Resilient File Processor**
```eigenscript
define process_file as:
    try:
        content is read_file of filename
        result is parse_json of content
        return result
    catch FileError:
        print of "File not found"
        return null
    catch ValueError:
        print of "Invalid JSON"
        return null
    finally:
        print of "Processing complete"
```

3. **Statistical Analysis**
```eigenscript
use std:math

# Load data
numbers is [1, 5, 3, 8, 2, 9, 4, 7, 6]

# Compute statistics
avg is math.mean of numbers
median_val is math.median of numbers
std_dev is math.stdev of numbers

# Create report
report is {
    mean: avg,
    median: median_val,
    stdev: std_dev,
    count: len of numbers
}

# Save report
write_file of ["report.json", to_json_pretty of report]
```

---

## Timeline & Resources

### Sprint Schedule (12 weeks)

| Sprint | Weeks | Feature | Team Size |
|--------|-------|---------|-----------|
| 1-2 | 1-2 | File I/O | 1-2 devs |
| 3-4 | 3-5 | Error Handling | 1-2 devs |
| 5-6 | 6-7 | JSON/Serialization | 1 dev |
| 7-9 | 8-10 | Data Structures | 2 devs |
| 10-12 | 11-12 | Math/Collections | 1-2 devs |

### Resource Requirements
- **Developers**: 2-3 full-time
- **Testing**: Continuous (integrated into each sprint)
- **Documentation**: 1 technical writer (part-time)
- **Code Review**: Weekly reviews

### Risk Mitigation
- **Risk**: Features take longer than estimated
  - **Mitigation**: Buffer time in sprints 9 and 12
- **Risk**: Integration issues
  - **Mitigation**: Integration tests from day 1
- **Risk**: Performance degradation
  - **Mitigation**: Benchmark tests, profile regularly

---

## Next Steps

1. **Week 1**: Set up development branches for Phase 6
2. **Week 1-2**: Implement File I/O (Sprint 1-2)
3. **Week 3**: Review and merge File I/O
4. **Week 3-5**: Implement Error Handling (Sprint 3-4)
5. Continue through all sprints...

**Start Date**: Q1 2025
**Target Completion**: End of Q1 2025 (12 weeks)

---

**Document Status**: ✅ Complete Technical Guide
**Next Action**: Begin Sprint 1 (File I/O Implementation)
**Owner**: EigenScript Core Development Team
