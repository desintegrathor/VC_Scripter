# Expression Module Refactoring Plan

## Current State

- **expr.py**: 4099 lines (MONOLITHIC)
  - Helper functions: ~400 lines
  - ExpressionFormatter class: ~3420 lines with 52 methods
  - Supporting functions: ~280 lines

## Problem

The `ExpressionFormatter` class is a classic "God Class" with too many responsibilities:

1. Type analysis and struct resolution
2. Variable naming (semantic, parameters, globals)
3. Constant and literal formatting
4. Array and pointer operations
5. Expression rendering (infix, unary, call, phi, store)
6. Field tracking and struct type detection
7. String literal detection
8. Text database integration

## Proposed Modular Structure

```
vcdecomp/core/ir/expr/
├── __init__.py              # Re-exports (ExpressionFormatter, format_block_expressions)
├── constants.py             # Float/constant detection helpers
│   ├── _is_likely_float()
│   ├── _format_float()
│   └── Float pattern constants
├── type_utils.py            # Type parsing and detection
│   ├── _parse_xfn_arg_types()
│   ├── _is_numeric_type()
│   ├── _get_operand_type_from_mnemonic()
│   └── TYPE_NAMES dict
├── negation.py              # Expression negation (Ghidra-style)
│   ├── negate_comparison_op()
│   ├── negate_condition_expr()
│   └── COMPARISON_NEGATION mapping
├── models.py                # Data classes
│   └── FormattedExpression
├── operators.py             # Operator mappings
│   ├── INFIX_OPS
│   ├── UNARY_PREFIX
│   ├── COMPARISON_OPS
│   └── CAST_OPS
├── formatter/               # Split ExpressionFormatter into focused classes
│   ├── __init__.py
│   ├── base.py             # Base formatter with core state
│   │   └── ExpressionFormatterBase (constructor + shared state)
│   ├── naming.py           # Variable and semantic naming
│   │   ├── _assign_semantic_names()
│   │   ├── _get_semantic_name()
│   │   ├── _assign_parameter_names()
│   │   ├── _resolve_global_names()
│   │   ├── _detect_loop_counters()
│   │   └── _value_name()
│   ├── types.py            # Type analysis and struct detection
│   │   ├── _analyze_struct_types()
│   │   ├── _get_heritage_type()
│   │   ├── _update_struct_type()
│   │   ├── _detect_target_field_type()
│   │   └── _resolve_field_name()
│   ├── constants.py        # Constant resolution
│   │   ├── _try_resolve_constant()
│   │   ├── _format_constant_value()
│   │   ├── _check_string_literal()
│   │   ├── _escape_string()
│   │   ├── _is_string_literal()
│   │   ├── _substitute_constant()
│   │   └── _get_constant_int()
│   ├── pointers.py         # Pointer and array formatting
│   │   ├── _detect_array_indexing()
│   │   ├── _format_pointer_target()
│   │   ├── _is_address_expression()
│   │   ├── _extract_var_from_pointer()
│   │   └── _is_constant_array_notation()
│   ├── values.py           # Value rendering
│   │   ├── render_value()
│   │   ├── _render_value()
│   │   ├── _render_value_impl()
│   │   ├── _can_inline()
│   │   ├── _load_literal()
│   │   └── _parse_data_offset()
│   ├── expressions.py      # Expression formatting
│   │   ├── _format_infix()
│   │   ├── _format_unary()
│   │   ├── _format_call()
│   │   ├── _format_phi()
│   │   └── _inline_expression()
│   └── stores.py           # Store operation formatting
│       ├── _format_store()
│       ├── _format_target()
│       ├── _track_text_id_assignment()
│       └── _is_parametric_alias()
└── block_format.py          # Block-level formatting
    ├── format_block_expressions()
    └── _is_degenerate_phi()
```

## Refactoring Strategy

### Phase 1: Extract Helper Modules (Low Risk)
1. Create `constants.py` - extract float detection functions
2. Create `type_utils.py` - extract type parsing functions
3. Create `negation.py` - extract negation functions
4. Create `models.py` - extract FormattedExpression
5. Create `operators.py` - extract operator dicts
6. Update imports in expr.py to use new modules

### Phase 2: Split ExpressionFormatter by Responsibility (Medium Risk)
1. Create `formatter/base.py` - constructor + shared state only
2. Create mixins for each responsibility area:
   - `NamingMixin` - naming methods
   - `TypesMixin` - type analysis methods
   - `ConstantsMixin` - constant handling
   - `PointersMixin` - pointer/array formatting
   - `ValuesMixin` - value rendering
   - `ExpressionsMixin` - expression formatting
   - `StoresMixin` - store formatting
3. Compose `ExpressionFormatter` from base + mixins
4. Test thoroughly after each mixin extraction

### Phase 3: Refactor to Composition (Higher Risk)
1. Convert mixins to separate strategy classes
2. Update ExpressionFormatter to delegate to strategies
3. This enables better testing and reusability

## Benefits

- **Maintainability**: Each module has single responsibility
- **Testability**: Can test each component independently
- **Readability**: Easier to find and understand code
- **Extensibility**: Can replace/extend individual components
- **Reduced Cognitive Load**: Smaller files easier to work with

## Risks

- The ExpressionFormatter has complex internal state sharing
- Methods frequently call each other across responsibilities
- Breaking encapsulation boundaries may introduce bugs
- Extensive testing required after refactoring

## Testing Strategy

1. Capture current output for all test scripts
2. Refactor incrementally with regression testing after each step
3. Use validation system to verify bytecode equivalence
4. Check decompiled output for cosmetic changes

## Timeline Estimate

- Phase 1 (Helpers): 2-3 hours
- Phase 2 (Mixins): 6-8 hours
- Phase 3 (Composition): 4-6 hours
- Testing: 3-4 hours
- **Total**: 15-21 hours

## Priority

**MEDIUM** - The code works but is hard to maintain. Tackle this when:
- Adding new expression formatting features
- Fixing bugs in specific formatting areas
- Improving code organization

Current priority is implementing Ghidra algorithms (heritage, jumptables).
