# Coding Conventions

**Analysis Date:** 2026-01-17

## Naming Patterns

**Files:**
- Module files: snake_case (e.g., `stack_lifter.py`, `bytecode_compare.py`, `global_resolver.py`)
- Test files: `test_` prefix (e.g., `test_structure_patterns.py`, `test_validation_workflow.py`)
- Package imports: `__init__.py` in every package directory

**Functions:**
- snake_case for all functions (e.g., `build_cfg`, `lift_function`, `format_block_expressions`)
- Private/internal functions: `_` prefix (e.g., `_to_signed`, `_derive_alias`, `_detect_if_else_pattern`)
- Test functions: `test_` prefix (e.g., `test_hitable_decompilation`, `test_validation_orchestrator_initialization`)

**Variables:**
- snake_case for locals and parameters (e.g., `block_id`, `entry_block`, `resolver`, `opcode_variant`)
- Module-level constants: UPPER_SNAKE_CASE (e.g., `VARIANT_CHOICES`, `OPERATOR_PRECEDENCE`, `SHOW_BLOCK_COMMENTS`)
- Dictionary constants with data: UPPER_SNAKE_CASE (e.g., `SCM_CONSTANTS`, `STRUCTURES_BY_SIZE`)

**Types:**
- Classes: PascalCase (e.g., `BasicBlock`, `CFG`, `ValidationOrchestrator`, `SyntaxHighlighter`)
- Dataclasses: PascalCase (e.g., `StackValue`, `LiftedInstruction`, `CaseInfo`, `SwitchPattern`)
- Enums: PascalCase with UPPER_SNAKE_CASE values (e.g., `ExpressionContext.IN_CONDITION`, `DifferenceType.HEADER`)

## Code Style

**Formatting:**
- No formal formatter configured (no `.prettierrc`, `.black`, or similar config files detected)
- Indentation: 4 spaces (Python standard)
- Line length: Generally kept under 100-120 characters
- Blank lines: 2 blank lines between top-level definitions, 1 within classes

**Linting:**
- No linter configuration files detected (no `.flake8`, `.pylintrc`, `pyproject.toml`)
- Code follows PEP 8 style conventions by inspection

## Import Organization

**Order:**
1. Future imports first: `from __future__ import annotations` (used in most modern modules)
2. Standard library imports (e.g., `import sys`, `import logging`, `from pathlib import Path`)
3. Third-party imports (e.g., `from PyQt6.QtWidgets import QMainWindow`, `import pytest`)
4. Local package imports (e.g., `from .core.ir.cfg import build_cfg`, `from ..disasm import opcodes`)

**Path Aliases:**
- Relative imports within package: `from .core.loader import SCRFile`, `from ..disasm import opcodes`
- Parent package imports: `from ..loader.scr_loader import SCRFile`
- Sibling package imports: `from .patterns.models import SwitchPattern`

**Pattern:**
```python
from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from .compiler_wrapper import SCMPWrapper
from .bytecode_compare import BytecodeComparator
```

## Error Handling

**Patterns:**
- Explicit exception raising with descriptive messages
- FileNotFoundError for missing files: `raise FileNotFoundError(f"Compiler directory not found: {self.compiler_dir}")`
- ValueError for invalid inputs: `raise ValueError(f"Unknown SCR opcode variant '{variant}'. Valid values: auto, {valid}")`
- AttributeError for invalid module attributes: `raise AttributeError(f"module {__name__} has no attribute {name}")`

**Validation:**
- Early validation in `__init__` methods
- Check file existence before processing: `if not scmp_exe.exists(): raise FileNotFoundError(...)`
- Return None for optional failures, raise exceptions for critical failures

## Logging

**Framework:** Python standard library `logging` module

**Patterns:**
- Module-level logger: `logger = logging.getLogger(__name__)`
- Used in: `vcdecomp/parsing/header_parser.py`, `vcdecomp/core/loader/data_strings.py`, `vcdecomp/core/ir/function_detector.py`, `vcdecomp/validation/cache.py`, `vcdecomp/validation/validator.py`

**Log Levels:**
- `logger.debug()`: Detailed information for diagnosing (e.g., found RET addresses, struct parsing)
- `logger.info()`: Confirmation of expected behavior (e.g., "Detected 28 functions", "Extracted 156 strings")
- `logger.warning()`: Unexpected but recoverable situations (e.g., "pycparser failed, using regex fallback")
- `logger.error()`: Error conditions (e.g., "Failed to parse header file")

**Examples:**
```python
logger.info(f"Initialized ValidationOrchestrator with compiler_dir={self.compiler_dir}")
logger.debug(f"Found {len(call_targets)} CALL targets: {sorted(call_targets)}")
logger.warning(f"pycparser failed: {e}, using regex fallback")
```

## Comments

**When to Comment:**
- Module docstrings: Every module has a docstring describing purpose
- Function docstrings: Complex functions have detailed docstrings with Args/Returns
- Inline comments: Used for non-obvious logic, heuristics, or workarounds
- FIX comments: Used to mark bug fixes with context (e.g., `# FIX 2: Use BYTE offset, not dword index!`)

**Docstring Style:**
- Triple-quoted strings using `"""`
- Module-level: Brief description with usage examples
- Function-level: Description, Args, Returns sections (not strict Google/NumPy style)
- Class-level: Description with Attributes section

**Examples:**
```python
"""
Stack-based VM lifting utilities.

Converts sequences of instructions into pseudo-register operations
by tracking the evaluation stack.
"""

def _detect_for_loop(loop: NaturalLoop, cfg, instructions, ...) -> Optional[ForLoopInfo]:
    """
    Detect for-loop pattern in a natural loop.

    Args:
        loop: Natural loop structure
        cfg: Control flow graph
        instructions: SSA instructions
        ...

    Returns:
        ForLoopInfo if detected, None otherwise
    """
```

## Function Design

**Size:** Average ~50-150 lines per function. Complex analysis functions can be 200-300 lines.

**Parameters:**
- Use type hints consistently: `def build_cfg(scr: SCRFile, resolver: Optional[opcodes.OpcodeResolver] = None) -> CFG`
- Optional parameters use `Optional[Type]` or union types: `Path | str` (Python 3.10+ style)
- Default values for optional params: `timeout: int = 30`, `cache_enabled: bool = True`

**Return Values:**
- Explicit return types in signatures: `-> str`, `-> ValidationResult`, `-> Optional[ForLoopInfo]`
- Return `None` for optional results, not empty values
- Return dataclasses for structured data

## Module Design

**Exports:**
- Explicit `__all__` not used
- Public API: Functions/classes without `_` prefix
- Private implementation: Functions with `_` prefix (e.g., `_to_signed`, `_infer_phi_type`)

**Barrel Files:**
- `__init__.py` files used for package imports
- Re-export common types: `from .patterns.models import SwitchPattern, IfElsePattern` in `structure/patterns/__init__.py`

**Structure:**
- Package organization by functionality: `structure/patterns/`, `structure/analysis/`, `structure/emit/`
- Avoid circular dependencies (successfully refactored structure package from monolithic to modular)

## Type Hints

**Coverage:** High usage across codebase (~87% based on project context)

**Patterns:**
- `from __future__ import annotations` enables forward references
- Use standard types: `Dict`, `List`, `Set`, `Optional`, `Tuple` from `typing`
- Use dataclasses for structured data with automatic type checking
- Union types with `|` for Python 3.10+ compatibility

**Examples:**
```python
from __future__ import annotations
from typing import Dict, List, Optional, Set

def format_structured_function(ssa_func: SSAFunction) -> str:
    ...

@dataclass
class ValidationOrchestrator:
    compiler_dir: Path | str
    include_dirs: Optional[List[Path | str]] = None
    timeout: int = 30
```

## Special Patterns

**Dataclasses:**
- Heavy use for data structures: `BasicBlock`, `CFG`, `StackValue`, `CaseInfo`, `ValidationResult`
- Use `field(default_factory=...)` for mutable defaults
- `__post_init__` for validation and derived fields

**Context Managers:**
- Used for temporary directories in validation: `tempfile.mkdtemp()` with cleanup
- File operations use `Path` objects, not context managers for simple reads

**Platform-Specific Code:**
```python
# Fix for Windows console - force UTF-8 output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

---

*Convention analysis: 2026-01-17*
