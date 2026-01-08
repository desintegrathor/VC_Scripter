# Structure.py Dependency Analysis

**File**: `vcdecomp/core/ir/structure.py`
**Size**: 3,250 lines
**Date**: 2026-01-07

## Executive Summary

This document maps all internal and external dependencies in structure.py to guide the refactoring into focused modules. The analysis identifies:
- 5 data classes
- 32 functions (2 public entry points, 30 internal helpers)
- 7 external module dependencies
- 4 external consumers
- Complex internal call graph with clear clustering around functionality

---

## 1. External Dependencies (Imports)

### Standard Library
```python
from typing import Dict, Set, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
```

### Internal vcdecomp Modules
```python
from ..disasm import opcodes                              # Opcode resolution, type information
from .ssa import SSAFunction                              # SSA data structures
from .expr import format_block_expressions, FormattedExpression, ExpressionFormatter, format_instruction
from .cfg import CFG, NaturalLoop, find_all_loops, find_loops_in_function, dominates
from ...parsing.symbol_db import SymbolDatabase          # Symbol information
from .parenthesization import ExpressionContext, is_simple_expression
```

**Dependency Summary:**
- `opcodes`: Used throughout for opcode resolution, type checking, conditional jump detection
- `ssa`: Core data structure, used by almost all functions
- `expr`: Expression formatting and rendering
- `cfg`: Control flow graph analysis
- `symbol_db`: Optional symbol information lookup
- `parenthesization`: Expression context and simplification

---

## 2. External Consumers (Who imports structure.py)

### Public API Functions (Must be preserved)
1. **`vcdecomp/__main__.py`**
   - Imports: `format_structured_function`, `format_structured_function_named`
   - Usage: Main decompilation entry points

2. **`vcdecomp/gui/main_window.py`**
   - Imports: `format_structured_function_named`
   - Usage: GUI decompilation

3. **`vcdecomp/tests/test_compound_conditions.py`**
   - Imports: `_detect_short_circuit_pattern`, `CompoundCondition`
   - Usage: Testing internal pattern detection (⚠️ tests import internals)

**Migration Impact**:
- Public API must be maintained in `__init__.py`
- Test may need updating to import from new module location

---

## 3. Data Classes

### 3.1 CaseInfo (Lines ~44-53)
**Purpose**: Information about one case in a switch statement
**Dependencies**: None (pure data)
**Fields**:
- `value: int` - Case constant
- `block_id: int` - Entry block
- `body_blocks: Set[int]` - All blocks in case
- `has_break: bool` - Whether case ends with break

**Target Module**: `patterns/models.py`

### 3.2 SwitchPattern (Lines ~57-74)
**Purpose**: Detected switch/case pattern
**Dependencies**: Uses `CaseInfo`
**Fields**:
- `test_var: str` - Variable being tested
- `header_block: int` - Switch entry point
- `cases: List[CaseInfo]` - All cases
- `default_block: Optional[int]` - Default case
- `default_body_blocks: Set[int]` - Default case blocks
- `exit_block: Optional[int]` - Common exit
- `all_blocks: Set[int]` - All switch blocks

**Target Module**: `patterns/models.py`

### 3.3 IfElsePattern (Lines ~677-692)
**Purpose**: Detected if/else pattern
**Dependencies**: Uses `CompoundCondition`
**Fields**:
- `condition: str` - Condition expression
- `true_block: int` - True branch entry
- `false_block: Optional[int]` - False branch entry
- `merge_block: Optional[int]` - Join point
- `true_blocks: Set[int]` - All true branch blocks
- `false_blocks: Set[int]` - All false branch blocks
- `header_block: int` - If statement entry
- `compound_condition: Optional[CompoundCondition]` - Short-circuit info

**Target Module**: `patterns/models.py`

### 3.4 CompoundCondition (Lines ~694-717)
**Purpose**: Short-circuit (&&/||) condition information
**Dependencies**: None (pure data)
**Fields**:
- `operator: str` - "&&" or "||"
- `conditions: List[str]` - Sub-conditions
- `blocks: List[int]` - Blocks in chain
- `true_target: Optional[int]` - Where to go if true
- `false_target: Optional[int]` - Where to go if false

**Target Module**: `patterns/models.py`

### 3.5 ForLoopInfo (Lines ~719-726)
**Purpose**: Detected for-loop pattern
**Dependencies**: None (pure data)
**Fields**:
- `init: Optional[str]` - Initialization
- `condition: Optional[str]` - Loop condition
- `increment: Optional[str]` - Increment expression
- `loop: NaturalLoop` - Associated loop structure

**Target Module**: `patterns/models.py`

---

## 4. Utility Functions

### 4.1 _load_symbol_db() (Lines 28-40)
**Purpose**: Load symbol database from compiler/symbol_db.json
**Dependencies**:
- External: `pathlib.Path`
- Internal: `SymbolDatabase.load()`
**Called by**: `format_structured_function()`, `format_structured_function_named()`
**Target Module**: `utils/helpers.py`

### 4.2 _build_start_map(cfg) (Lines 77-78)
**Purpose**: Build mapping from instruction address to block ID
**Dependencies**: Uses `cfg.blocks`
**Called by**: `format_structured_function()`, `format_structured_function_named()`
**Target Module**: `utils/helpers.py`

### 4.3 _dominates(cfg, a, b) (Lines 81-93)
**Purpose**: Check if block A dominates block B
**Dependencies**: Uses `cfg.idom`
**Called by**: `format_structured_function()`
**Target Module**: `utils/helpers.py`

### 4.4 _is_control_flow_only(ssa_block, resolver) (Lines 300-327)
**Purpose**: Check if block contains only control flow (no side effects)
**Dependencies**: `opcodes.OpcodeResolver`
**Called by**: Multiple rendering functions
**Target Module**: `utils/helpers.py`

---

## 5. Block Formatting Functions

### 5.1 _format_block_lines_filtered() (Lines 96-139)
**Purpose**: Format block with SSA value filtering
**Dependencies**:
- `format_block_expressions()`
- `ExpressionFormatter`
**Called by**: `_render_blocks_with_loops()`
**Target Module**: `emit/block_formatter.py`

### 5.2 _format_block_lines() (Lines 141-298)
**Purpose**: Format block with nested if/else detection
**Dependencies**:
- Calls: `format_block_expressions()`, `_trace_value_to_function_call()`, `_render_if_else_recursive()`, `_combine_conditions()`
- Uses: `SSAFunction`, `ExpressionFormatter`
**Called by**: Multiple rendering and detection functions
**Target Module**: `emit/block_formatter.py`

---

## 6. Control Flow Analysis Functions

### 6.1 _get_loop_for_block(block_id, loops) (Lines 659-666)
**Purpose**: Find which loop contains a given block
**Dependencies**: Uses `NaturalLoop`
**Called by**: `format_structured_function_named()`
**Target Module**: `analysis/flow.py`

### 6.2 _is_back_edge_target(cfg, source, target, loops) (Lines 668-675)
**Purpose**: Check if edge is a loop back edge
**Dependencies**: Uses `NaturalLoop`
**Called by**: `format_structured_function_named()`
**Target Module**: `analysis/flow.py`

### 6.3 _find_if_body_blocks(cfg, entry, stop_blocks, resolver) (Lines 1161-1197)
**Purpose**: Find all blocks belonging to an if/else branch
**Dependencies**: `CFG`, `opcodes.OpcodeResolver`
**Called by**: `_detect_if_else_pattern()`
**Target Module**: `analysis/flow.py`

### 6.4 _find_case_body_blocks(cfg, case_entry, stop_blocks, resolver) (Lines 2011-2056)
**Purpose**: Find all blocks belonging to a switch case
**Dependencies**: `CFG`, `opcodes.OpcodeResolver`
**Called by**: `_detect_switch_patterns()`
**Target Module**: `analysis/flow.py`

### 6.5 _find_common_successor(cfg, block_a, block_b) (Lines 1199-1233)
**Purpose**: Find common successor of two blocks (merge point)
**Dependencies**: `CFG`
**Called by**: `_detect_if_else_pattern()`
**Target Module**: `analysis/flow.py`

### 6.6 _is_jmp_after_jz(block, resolver) (Lines 1235-1261)
**Purpose**: Check if block is just a JMP following a JZ
**Dependencies**: `opcodes.OpcodeResolver`
**Called by**: `_find_common_true_target()`
**Target Module**: `analysis/flow.py`

### 6.7 _find_all_jz_targets(block, resolver) (Lines 1263-1292)
**Purpose**: Find all JZ target addresses in a block
**Dependencies**: `opcodes.OpcodeResolver`
**Called by**: `_detect_short_circuit_pattern()`
**Target Module**: `analysis/flow.py`

### 6.8 _find_common_true_target(cfg, blocks, resolver, start_to_block) (Lines 1294-1329)
**Purpose**: Find common true target for AND chain
**Dependencies**: Calls `_is_jmp_after_jz()`
**Called by**: `_detect_short_circuit_pattern()`
**Target Module**: `analysis/flow.py`

---

## 7. Condition Extraction Functions

### 7.1 _extract_condition_from_block(ssa_func, block_id, formatter, negate) (Lines 1331-1385)
**Purpose**: Extract condition expression from a conditional jump block
**Dependencies**:
- Uses: `SSAFunction`, `ExpressionFormatter`, `ExpressionContext`
- Calls: `is_simple_expression()`
**Called by**: `_detect_short_circuit_pattern()`, `_detect_if_else_pattern()`
**Target Module**: `analysis/condition.py`

### 7.2 _extract_condition_expr() (Lines 1387-1389)
**Purpose**: Legacy wrapper for `_extract_condition_from_block()`
**Dependencies**: Calls `_extract_condition_from_block()`
**Called by**: None (legacy)
**Target Module**: `analysis/condition.py` (or remove)

### 7.3 _combine_conditions(conditions, operator, preserve_style) (Lines 1420-1468)
**Purpose**: Combine multiple conditions with && or ||
**Dependencies**: Recursive, handles `CompoundCondition`
**Called by**: `_render_if_else_recursive()`, self (recursive)
**Target Module**: `analysis/condition.py`

### 7.4 _collect_and_chain(start_block_id, cfg, resolver, start_to_block, visited) (Lines 1631-1722)
**Purpose**: Collect blocks forming an AND chain
**Dependencies**:
- Uses: `CFG`, `opcodes.OpcodeResolver`
- Calls: self (recursive)
**Called by**: `_detect_short_circuit_pattern()`
**Target Module**: `analysis/condition.py`

---

## 8. Value Tracing Functions

### 8.1 _trace_value_to_function_call(ssa_func, value, formatter, max_depth) (Lines 1549-1628)
**Purpose**: Trace SSA value back to function call
**Dependencies**:
- Uses: `SSAFunction`, `ExpressionFormatter`
- Calls: `format_instruction()`, self (recursive)
**Called by**: `_format_block_lines()`, self (recursive)
**Target Module**: `analysis/value_trace.py`

### 8.2 _trace_value_to_global(value, formatter, visited) (Lines 2058-2145)
**Purpose**: Trace SSA value to global variable name
**Dependencies**:
- Uses: `ExpressionFormatter`
- Calls: self (recursive)
**Called by**: `_detect_switch_patterns()`, self (recursive)
**Target Module**: `analysis/value_trace.py`

### 8.3 _trace_value_to_parameter(value, formatter, ssa_func) (Lines 2147-2217)
**Purpose**: Trace SSA value to function parameter
**Dependencies**: Uses `SSAFunction`, `ExpressionFormatter`
**Called by**: `_detect_switch_patterns()`
**Target Module**: `analysis/value_trace.py`

### 8.4 _find_switch_variable_from_nearby_gcp(block, ssa_func, formatter) (Lines 2219-2275)
**Purpose**: Find switch variable from nearby GCP instruction
**Dependencies**: Uses `SSAFunction`, `ExpressionFormatter`
**Called by**: `_detect_switch_patterns()`
**Target Module**: `analysis/value_trace.py`

---

## 9. Variable Collection Functions

### 9.1 _collect_local_variables(ssa_func, func_block_ids, formatter) (Lines 2530-2708)
**Purpose**: Collect and declare local variables with type inference
**Dependencies**:
- Uses: `SSAFunction`, `ExpressionFormatter`, `opcodes.ResultType`
- Complex logic with array detection
**Called by**: `format_structured_function_named()`
**Target Module**: `analysis/variables.py`

---

## 10. Pattern Detection Functions

### 10.1 _detect_early_return_pattern(cfg, block_id, start_to_block, resolver, exit_block) (Lines 1470-1547)
**Purpose**: Detect early return pattern in switch cases
**Dependencies**: Uses `CFG`, `opcodes.OpcodeResolver`
**Called by**: `format_structured_function_named()` (in switch case handling)
**Target Module**: `patterns/if_else.py`

### 10.2 _detect_short_circuit_pattern(cfg, block_id, start_to_block, resolver, ssa_func, formatter) (Lines 1724-1835)
**Purpose**: Detect short-circuit && or || patterns
**Dependencies**:
- Uses: `CompoundCondition`
- Calls: `_collect_and_chain()`, `_extract_condition_from_block()`, `_find_all_jz_targets()`, `_find_common_true_target()`, self (recursive)
**Called by**: `_detect_if_else_pattern()`, self (recursive)
**Target Module**: `patterns/compound.py`

### 10.3 _detect_if_else_pattern(cfg, block_id, start_to_block, resolver, visited_ifs, func_loops, **kwargs) (Lines 1837-2009)
**Purpose**: Detect if/else patterns
**Dependencies**:
- Uses: `IfElsePattern`, `CFG`, `opcodes.OpcodeResolver`
- Calls: `_detect_short_circuit_pattern()`, `_find_common_successor()`, `_find_if_body_blocks()`
**Called by**: `format_structured_function_named()`
**Target Module**: `patterns/if_else.py`

### 10.4 _detect_switch_patterns(ssa_func, func_block_ids, formatter, start_to_block) (Lines 2277-2528)
**Purpose**: Detect switch/case patterns
**Dependencies**:
- Uses: `SwitchPattern`, `CaseInfo`, `SSAFunction`
- Calls: `_trace_value_to_parameter()`, `_trace_value_to_global()`, `_find_switch_variable_from_nearby_gcp()`, `_find_case_body_blocks()`
**Called by**: `format_structured_function_named()`
**Target Module**: `patterns/switch_case.py`

### 10.5 _detect_for_loop(loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map) (Lines 878-1159)
**Purpose**: Detect for-loop patterns
**Dependencies**:
- Uses: `ForLoopInfo`, `NaturalLoop`
- Complex analysis of initialization, condition, increment
**Called by**: `_render_blocks_with_loops()`
**Target Module**: `patterns/loops.py`

---

## 11. Code Emission Functions

### 11.1 _render_if_else_recursive(ssa_func, pattern, indent, formatter, resolver, **kwargs) (Lines 329-558)
**Purpose**: Recursively render if/else patterns
**Dependencies**:
- Uses: `IfElsePattern`, `CompoundCondition`
- Calls: `_combine_conditions()`, `_format_block_lines()`, self (recursive)
**Called by**: `_format_block_lines()`, self (recursive)
**Target Module**: `emit/code_emitter.py`

### 11.2 _render_blocks_with_loops(cfg, blocks, base_indent, ssa_func, formatter, resolver, **kwargs) (Lines 728-876)
**Purpose**: Render blocks with loop detection
**Dependencies**:
- Uses: `CFG`, `NaturalLoop`
- Calls: `_detect_for_loop()`, `_is_control_flow_only()`, `_format_block_lines_filtered()`, `_format_block_lines()`
**Called by**: `format_structured_function_named()` (for switch case/default bodies)
**Target Module**: `emit/code_emitter.py`

---

## 12. Public Entry Points

### 12.1 format_structured_function(ssa_func) (Lines 560-657)
**Purpose**: Simple structured output (legacy/basic)
**Dependencies**:
- Calls: `_build_start_map()`, `_load_symbol_db()`, `_format_block_lines()`, `_dominates()`
**Called by**: External (`__main__.py`)
**Target Module**: `orchestrator.py`

### 12.2 format_structured_function_named(ssa_func, func_name, entry_addr, end_addr, function_bounds) (Lines 2710-3250)
**Purpose**: Main decompilation entry point with full pattern detection
**Dependencies**:
- Calls: Almost all other functions in the file
- Massive function (~540 lines)
**Called by**: External (`__main__.py`, `gui/main_window.py`)
**Target Module**: `orchestrator.py`

---

## 13. Function Call Graph

### Utility Layer (No dependencies on other structure.py functions)
```
_load_symbol_db()
_build_start_map(cfg)
_dominates(cfg, a, b)
_is_control_flow_only(ssa_block, resolver)
```

### Analysis Layer (Uses utilities)
```
Flow Analysis:
├── _get_loop_for_block(block_id, loops)
├── _is_back_edge_target(cfg, source, target, loops)
├── _find_if_body_blocks(cfg, entry, stop_blocks, resolver)
├── _find_case_body_blocks(cfg, case_entry, stop_blocks, resolver)
├── _find_common_successor(cfg, block_a, block_b)
├── _is_jmp_after_jz(block, resolver)
├── _find_all_jz_targets(block, resolver)
└── _find_common_true_target(cfg, blocks, resolver, start_to_block)
    └── calls: _is_jmp_after_jz()

Condition Analysis:
├── _extract_condition_from_block(ssa_func, block_id, formatter, negate)
├── _combine_conditions(conditions, operator, preserve_style) [recursive]
└── _collect_and_chain(start_block_id, cfg, resolver, start_to_block, visited) [recursive]

Value Tracing:
├── _trace_value_to_function_call(ssa_func, value, formatter, max_depth) [recursive]
├── _trace_value_to_global(value, formatter, visited) [recursive]
├── _trace_value_to_parameter(value, formatter, ssa_func)
└── _find_switch_variable_from_nearby_gcp(block, ssa_func, formatter)

Variables:
└── _collect_local_variables(ssa_func, func_block_ids, formatter)
```

### Pattern Detection Layer (Uses analysis layer)
```
├── _detect_early_return_pattern(cfg, block_id, start_to_block, resolver, exit_block)
├── _detect_short_circuit_pattern(...) [recursive]
│   └── calls: _collect_and_chain(), _extract_condition_from_block(),
│       _find_all_jz_targets(), _find_common_true_target()
├── _detect_if_else_pattern(...)
│   └── calls: _detect_short_circuit_pattern(), _find_common_successor(),
│       _find_if_body_blocks()
├── _detect_switch_patterns(...)
│   └── calls: _trace_value_to_parameter(), _trace_value_to_global(),
│       _find_switch_variable_from_nearby_gcp(), _find_case_body_blocks()
└── _detect_for_loop(...)
```

### Emission Layer (Uses all layers)
```
├── _format_block_lines_filtered(...)
├── _format_block_lines(...) [complex]
│   └── calls: _trace_value_to_function_call(), _render_if_else_recursive(),
│       _combine_conditions()
├── _render_if_else_recursive(...) [recursive]
│   └── calls: _combine_conditions(), _format_block_lines()
└── _render_blocks_with_loops(...)
    └── calls: _detect_for_loop(), _is_control_flow_only(),
        _format_block_lines_filtered(), _format_block_lines()
```

### Entry Points (Orchestrators)
```
├── format_structured_function(ssa_func) [SIMPLE/LEGACY]
│   └── calls: _build_start_map(), _load_symbol_db(), _format_block_lines(), _dominates()
└── format_structured_function_named(...) [MAIN ENTRY POINT - 540 lines!]
    └── calls: _build_start_map(), _load_symbol_db(), _detect_switch_patterns(),
        _collect_local_variables(), _detect_if_else_pattern(), _detect_early_return_pattern(),
        _render_blocks_with_loops(), _is_control_flow_only(), _format_block_lines(),
        _is_back_edge_target(), _get_loop_for_block()
```

---

## 14. Critical Dependencies and Risks

### Circular Dependency Risks
1. **_format_block_lines ↔ _render_if_else_recursive**
   - Both call each other for nested if/else handling
   - **Mitigation**: Keep both in same module OR use dependency injection

2. **_detect_short_circuit_pattern (recursive)**
   - Calls itself for nested short-circuit conditions
   - **Mitigation**: No issue, recursive calls are fine

3. **_combine_conditions (recursive)**
   - Calls itself for nested compound conditions
   - **Mitigation**: No issue, recursive calls are fine

### Shared State
- **SHOW_BLOCK_COMMENTS** global constant
  - Used by multiple functions
  - **Mitigation**: Move to `utils/helpers.py` or config

### Complex Cross-Module Dependencies
- `format_structured_function_named()` calls functions from ALL categories
- **Mitigation**: This is the orchestrator, it SHOULD depend on everything

---

## 15. Module Dependency Plan

### Extraction Order (Bottom-up)
1. **Phase 1**: Data models (no dependencies)
   - `patterns/models.py`: CaseInfo, SwitchPattern, IfElsePattern, CompoundCondition, ForLoopInfo

2. **Phase 2**: Utilities (minimal dependencies)
   - `utils/helpers.py`: _load_symbol_db, _build_start_map, _dominates, _is_control_flow_only, SHOW_BLOCK_COMMENTS

3. **Phase 3**: Analysis functions
   - `analysis/flow.py`: All _find_* and flow analysis functions
   - `analysis/condition.py`: Condition extraction and combination
   - `analysis/value_trace.py`: All _trace_* functions
   - `analysis/variables.py`: _collect_local_variables

4. **Phase 4**: Pattern detection
   - `patterns/compound.py`: _detect_short_circuit_pattern, _collect_and_chain
   - `patterns/if_else.py`: _detect_if_else_pattern, _detect_early_return_pattern
   - `patterns/switch_case.py`: _detect_switch_patterns
   - `patterns/loops.py`: _detect_for_loop

5. **Phase 5**: Code emission
   - `emit/block_formatter.py`: _format_block_lines, _format_block_lines_filtered
   - `emit/code_emitter.py`: _render_if_else_recursive, _render_blocks_with_loops

6. **Phase 6**: Orchestration
   - `orchestrator.py`: format_structured_function, format_structured_function_named
   - `__init__.py`: Public API re-exports

### Module Dependency Graph
```
patterns/models.py (no deps)
    ↑
utils/helpers.py (external deps only)
    ↑
analysis/flow.py (utils)
analysis/condition.py (utils)
analysis/value_trace.py (utils)
analysis/variables.py (utils)
    ↑
patterns/compound.py (models, analysis/condition, analysis/flow)
patterns/if_else.py (models, analysis/condition, analysis/flow)
patterns/switch_case.py (models, analysis/value_trace, analysis/flow)
patterns/loops.py (models, analysis/flow)
    ↑
emit/block_formatter.py (models, analysis/condition, analysis/value_trace)
emit/code_emitter.py (models, patterns/*, emit/block_formatter)
    ↑
orchestrator.py (ALL modules)
    ↑
__init__.py (orchestrator)
```

---

## 16. Data Flow Analysis

### Input (Entry Points)
```
SSAFunction → format_structured_function → String output
SSAFunction + metadata → format_structured_function_named → String output
```

### Processing Pipeline
```
1. Load symbol DB (optional)
2. Build address→block mapping
3. Detect patterns:
   - Switch/case patterns
   - If/else patterns
   - Loop patterns
   - For-loop patterns
4. Collect local variables
5. Emit structured code with detected patterns
```

### Key Data Structures Passed Between Functions
- **CFG**: Control flow graph (passed to most analysis functions)
- **SSAFunction**: SSA representation (passed to most functions)
- **ExpressionFormatter**: Expression rendering (passed to most functions)
- **start_to_block**: Dict[int, int] address→block mapping (passed widely)
- **Pattern objects**: IfElsePattern, SwitchPattern, ForLoopInfo (created by detection, consumed by emission)

---

## 17. Recommendations

### Immediate Actions
1. ✅ **Create this dependency analysis document** (DONE)
2. Create detailed module architecture document
3. Plan extraction order to avoid breaking changes

### Critical Considerations
1. **Backward Compatibility**: Maintain public API in `__init__.py`
2. **Test Updates**: Update `test_compound_conditions.py` to import from new locations
3. **Circular Dependencies**: Keep `_format_block_lines` and `_render_if_else_recursive` in same module
4. **Progressive Extraction**: Extract in dependency order (bottom-up)

### Success Metrics
- Each module < 500 lines
- No circular dependencies (except intentional recursive calls)
- All tests pass
- Decompilation output identical to before

---

## 18. Appendix: Complete Function List with Line Numbers

```
Line   28: _load_symbol_db()
Line   44: class CaseInfo
Line   57: class SwitchPattern
Line   77: _build_start_map()
Line   81: _dominates()
Line   96: _format_block_lines_filtered()
Line  141: _format_block_lines()
Line  300: _is_control_flow_only()
Line  329: _render_if_else_recursive()
Line  560: format_structured_function() [PUBLIC]
Line  659: _get_loop_for_block()
Line  668: _is_back_edge_target()
Line  677: class IfElsePattern
Line  694: class CompoundCondition
Line  719: class ForLoopInfo
Line  728: _render_blocks_with_loops()
Line  878: _detect_for_loop()
Line 1161: _find_if_body_blocks()
Line 1199: _find_common_successor()
Line 1235: _is_jmp_after_jz()
Line 1263: _find_all_jz_targets()
Line 1294: _find_common_true_target()
Line 1331: _extract_condition_from_block()
Line 1387: _extract_condition_expr()
Line 1420: _combine_conditions()
Line 1470: _detect_early_return_pattern()
Line 1549: _trace_value_to_function_call()
Line 1631: _collect_and_chain()
Line 1724: _detect_short_circuit_pattern()
Line 1837: _detect_if_else_pattern()
Line 2011: _find_case_body_blocks()
Line 2058: _trace_value_to_global()
Line 2147: _trace_value_to_parameter()
Line 2219: _find_switch_variable_from_nearby_gcp()
Line 2277: _detect_switch_patterns()
Line 2530: _collect_local_variables()
Line 2710: format_structured_function_named() [PUBLIC - MAIN]
```

---

**End of Dependency Analysis**
