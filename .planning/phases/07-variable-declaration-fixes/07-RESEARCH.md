# Phase 7: Variable Declaration Fixes - Research

**Researched:** 2026-01-18
**Domain:** Type inference, variable declaration, and semantic reconstruction
**Confidence:** MEDIUM

## Summary

Phase 7 addresses variable and type declaration quality in the decompiler. The current implementation has a sophisticated type inference engine (`type_inference.py`) and global resolver (`global_resolver.py`), but critical gaps exist in how types propagate from stack operations to declarations. Phase 6 verification revealed Pattern 2 (type mismatches) as a blocker requiring stack_lifter.py refactoring.

The decompiler uses a multi-pass architecture: stack_lifter.py tracks types during SSA construction, type_inference.py performs dataflow analysis, and variables.py generates declarations. However, these systems don't integrate fully - stack_lifter assigns generic `opcodes.ResultType.UNKNOWN` too often, which cascades to incorrect declarations.

**Primary recommendation:** Fix type propagation at the source (stack_lifter.py) rather than compensating downstream. Integrate type_inference.py results back into SSA values before declaration generation.

## Standard Stack

The established approach for decompiler type inference combines opcode analysis, dataflow propagation, and external signature integration:

### Core
| Component | Version | Purpose | Why Standard |
|-----------|---------|---------|--------------|
| type_inference.py | Current | Evidence-based type inference with confidence scoring | Industry-standard weighted voting approach |
| stack_lifter.py | Current | SSA construction with type tracking | Stack-based VM decompilation requires this |
| global_resolver.py | Current | Global variable detection and naming | Pattern-based with header integration |
| structures.py | Current | Struct field definitions from SDK | Domain-specific knowledge base |
| headers/database.py | Current | Function signature lookup | External ground truth source |

### Supporting
| Library | Purpose | When to Use |
|---------|---------|-------------|
| opcodes.py | Opcode-to-type mapping (FADD→float, IADD→int) | Primary type evidence source |
| constant_propagation.py | Constant value tracking | Type inference from literal values |
| field_tracker.py | Struct field access patterns | Infer struct types from usage |
| variable_renaming.py | Semantic name assignment | Readability after types resolved |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Evidence-based voting | ML type inference (STRIDE, CodeTIDAL5) | Requires training corpus, higher accuracy but slower |
| SDK headers | Reverse engineer types | Complete but requires manual work for 700+ functions |
| Opcode-based | Taint analysis | More precise but computationally expensive |

**Installation:**
```bash
# Current dependencies (already in project)
# No additional packages needed - pure Python implementation
```

## Architecture Patterns

### Recommended Type Inference Flow
```
stack_lifter.py (SSA construction)
├── Opcode analysis → ResultType enum
├── Stack simulation → Value tracking
└── Produces: SSAValue with initial value_type

type_inference.py (Dataflow analysis)
├── Collect evidence from instructions
├── Propagate through assignments
├── Merge PHI nodes
└── Produces: Dict[var_name, inferred_type]

variables.py (Declaration generation)
├── Collect variables from SSA
├── Query type_inference results
├── Apply struct patterns
└── Produces: List[declaration_strings]
```

### Pattern 1: Opcode-to-Type Mapping
**What:** Extract type evidence from instruction opcodes
**When to use:** First pass, highest confidence evidence
**Example:**
```python
# Source: vcdecomp/core/ir/type_inference.py:250-274
if mnemonic in self.float_ops:
    info.add_evidence(TypeEvidence(
        confidence=0.95,
        source=TypeSource.INSTRUCTION,
        inferred_type='float',
        reason=f'{inst.mnemonic} requires float operands'
    ))
```

### Pattern 2: Function Signature Propagation
**What:** Use external function signatures to constrain argument types
**When to use:** XCALL instructions with known function signatures
**Example:**
```python
# Source: vcdecomp/core/ir/type_inference.py:452-498
func_sig = self.header_db.get_function_signature(func_name)
param_types = [param[0] for param in func_sig['parameters']]
for i, value in enumerate(inst.inputs):
    if i < len(param_types):
        info.add_evidence(TypeEvidence(
            confidence=0.98,  # High - header signatures are ground truth
            source=TypeSource.FUNCTION_CALL,
            inferred_type=param_types[i],
            reason=f'Passed to {func_name} parameter {i}'
        ))
```

### Pattern 3: Dataflow Propagation
**What:** Propagate types through assignments and PHI nodes
**When to use:** After initial evidence collection
**Example:**
```python
# Source: vcdecomp/core/ir/type_inference.py:621-689
# Forward: a = b → type(a) = type(b)
# Backward: FADD(a, b) → a,b must be float
# PHI merge: PHI(a:int, b:int, c:float) → dominant type with confidence penalty
```

### Pattern 4: Struct Type Inference from Function Calls
**What:** Infer local variable struct types from function call patterns
**When to use:** When variable passed as &local_X to function expecting struct*
**Example:**
```python
# Source: vcdecomp/core/ir/structure/analysis/variables.py:112-163
# SC_P_GetInfo(&local_5) → local_5 is s_SC_P_getinfo
struct_type = infer_struct_from_function(call_name, arg_idx)
if struct_type:
    inferred_struct_types[var_name] = struct_type
```

### Anti-Patterns to Avoid
- **Generic fallback too early:** Don't default to `int` or `dword` before exhausting evidence sources
- **Type overwrite without confidence:** Preserve high-confidence types, only override if new evidence is stronger
- **Ignoring conversion opcodes:** ITOF, FTOI are explicit type evidence (0.99 confidence)
- **Skipping PHI merge:** Control flow merges need type reconciliation or declarations will be wrong

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Type inference weights | Manual confidence tuning | Evidence-based voting (type_inference.py) | Handles conflicts, extensible, testable |
| Struct field lookup | Parse headers on-the-fly | HeaderDatabase + JSON cache | Fast, offline, version-controlled |
| Global vs local detection | Heuristics only | GADR/LADR opcodes + save_info validation | Opcodes are ground truth, save_info has source names |
| Function signature matching | Regex or string parsing | HeaderDatabase.get_function_signature() | Handles overloads, parameter types, return types |
| Array dimension inference | Guess from size | Loop bound analysis (variables.py:165-253) | Finds actual usage bounds from comparisons |

**Key insight:** Type inference is inherently uncertain - use confidence scoring and evidence tracking rather than boolean type assignment. This allows downstream passes to make informed decisions (e.g., add TODO comments for low-confidence types).

## Common Pitfalls

### Pitfall 1: Stack Lifter Type Blindness
**What goes wrong:** stack_lifter.py assigns `ResultType.UNKNOWN` to most values, forcing downstream inference to work from scratch
**Why it happens:** Opcodes like GCP, LCP produce addresses (pointers), but the type of the pointed-to value is unknown
**How to avoid:**
- Dereference chain tracking: GCP → DCP → actual type
- Look ahead to next instruction: GCP + DCP(int) → int value
- Integrate type_inference.py results back into SSA values
**Warning signs:**
- High percentage of `dword` declarations
- Type mismatches in function calls (Pattern 2 from Phase 6)

### Pitfall 2: Global Variable Offset Confusion
**What goes wrong:** GADR/GCP arg1 is DWORD offset, but global tracking uses BYTE offset - misalignment causes wrong variables
**Why it happens:** Different parts of codebase use different offset units
**How to avoid:** Always convert: `byte_offset = dword_offset * 4` when accessing globals dict
**Warning signs:**
- Globals dictionary has wrong keys
- Global names don't match save_info
- Array detection fails

### Pitfall 3: Type Propagation Decay
**What goes wrong:** Type confidence decreases through propagation (0.05 decay per hop), reaching below threshold and being discarded
**Why it happens:** Propagation is lossy by design to avoid false positives
**How to avoid:**
- Set propagation_min_confidence appropriately (currently 0.70)
- Use direct evidence sources (opcodes, function calls) before propagation
- Multiple evidence sources compound confidence
**Warning signs:**
- Variables with obvious types (used in FADD) still declared as `int`
- Long SSA chains lose type information

### Pitfall 4: Struct vs Array Confusion
**What goes wrong:** Struct field access (base + offset) looks identical to array indexing (base + index * size)
**Why it happens:** Both use ADD instruction, distinction requires pattern analysis
**How to avoid:**
- Check if offsets are consecutive multiples (array) or irregular (struct)
- Look for field access patterns (.x, .y, .z at 0, 4, 8 → vector)
- Consult HeaderDatabase for known struct types
**Warning signs:**
- Vector3 declared as `int[3]` instead of `c_Vector3`
- Struct fields shown as array indices

## Code Examples

Verified patterns from official sources:

### Type Evidence Collection
```python
# Source: vcdecomp/core/ir/type_inference.py:200-249
def _analyze_instruction(self, inst: SSAInstruction):
    mnemonic = inst.mnemonic

    # Float operations
    if mnemonic in self.float_ops:
        for value in inst.inputs + inst.outputs:
            info = self._get_or_create_type_info(value.name)
            info.add_evidence(TypeEvidence(
                confidence=0.95,
                source=TypeSource.INSTRUCTION,
                inferred_type='float',
                reason=f'{mnemonic} requires/produces float'
            ))

    # Type conversions (explicit evidence)
    elif mnemonic in self.conversions:
        from_type, to_type = self.conversions[mnemonic]
        # Input is from_type (0.99 confidence)
        # Output is to_type (0.99 confidence)
```

### Global Variable Type Inference
```python
# Source: vcdecomp/core/ir/global_resolver.py:461-530
def _infer_global_types(self):
    # Run TypeInferenceEngine on entire function
    inferred_types = self.type_inference.infer_types()

    # Match SSA values to global offsets
    for inst in instructions:
        if inst.mnemonic in ['GCP', 'GLD', 'GADR']:
            byte_offset = inst.arg1 * 4  # CRITICAL: convert DWORD to BYTE
            output_value = inst.outputs[0]
            inferred_type = inferred_types.get(output_value.name)

            # CRITICAL: Skip void* from address ops (GADR)
            if inferred_type not in ['void*', 'ptr']:
                self.globals[byte_offset].inferred_type = inferred_type
```

### Declaration with Type Priority
```python
# Source: vcdecomp/core/ir/structure/analysis/variables.py:72-108
# Priority order for type assignment:
# 1. Inferred struct types (from function calls) - HIGHEST
# 2. Struct ranges (from field tracker)
# 3. SSA value type (opcodes.ResultType)
# 4. Default (int)

if display_name in inferred_struct_types:
    var_type = inferred_struct_types[display_name]
elif var_name in formatter._struct_ranges:
    var_type = struct_info[2]  # Struct name from tuple
elif value.value_type == opcodes.ResultType.FLOAT:
    var_type = "float"
else:
    var_type = default_type
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| All variables as `dword` | Evidence-based type inference | Type inference added ~2024 | Most variables still `dword` due to stack_lifter gaps |
| Global naming: `data_X` | Pattern-based + save_info + SGI constants | Global resolver enhanced ~2024 | Better names but offsets still confuse |
| Struct fields: `field_0` | Header lookup + pattern matching | Structures.py added ~2023 | Works for known types only |
| Function params: unnamed | HeaderDatabase integration | Headers module added ~2024 | 700+ signatures available |

**Deprecated/outdated:**
- Manual type annotations in test files: Type inference should handle this
- Hardcoded struct definitions in expr.py: Now in structures.py database
- Global detection without save_info: save_info section contains ground truth names

## Open Questions

Things that couldn't be fully resolved:

1. **Stack lifter integration timing**
   - What we know: type_inference.py exists but results aren't fed back to SSA
   - What's unclear: Best injection point - during SSA construction or after?
   - Recommendation: Two-pass approach - initial types in stack_lifter, refinement in type_inference, then update SSA values before declaration generation

2. **Pattern 2 root cause scope**
   - What we know: Pattern 2 (type mismatches) deferred from Phase 6, requires stack_lifter refactoring
   - What's unclear: Specific stack_lifter changes needed (filed Phase 6 docs only say "refactoring needed")
   - Recommendation: Investigate test1/test2/test3 actual Pattern 2 errors, trace back to stack_lifter code generating wrong types

3. **Array dimension calculation accuracy**
   - What we know: Loop bound analysis exists (variables.py:165-253) but conservative
   - What's unclear: How to handle dynamic bounds or non-constant loop limits
   - Recommendation: Use conservative size with TODO comment when uncertain

4. **Header database completeness**
   - What we know: sc_global.json and sc_def.json exist with 700+ functions
   - What's unclear: Coverage percentage, missing signatures impact
   - Recommendation: Audit XFN table against header database, log missing signatures

5. **Multi-dimensional array reconstruction**
   - What we know: Context decision says "detect 2D/3D arrays from nested indexing patterns"
   - What's unclear: Current implementation status - does variables.py handle this?
   - Recommendation: Search for nested MUL patterns (arr[i*width + j] → arr[i][j])

## Sources

### Primary (HIGH confidence)
- vcdecomp/core/ir/type_inference.py - Complete type inference engine with evidence tracking
- vcdecomp/core/ir/stack_lifter.py - SSA construction with initial type assignment
- vcdecomp/core/ir/global_resolver.py - Global variable detection with type inference integration
- vcdecomp/core/ir/structure/analysis/variables.py - Declaration generation with multi-source type priority
- vcdecomp/core/headers/database.py - Function signature and constant lookup
- vcdecomp/core/structures.py - SDK struct definitions
- original-resources/h/sc_global.h - 700+ function signatures (ground truth)
- original-resources/h/sc_def.h - Constant definitions

### Secondary (MEDIUM confidence)
- [Binary type inference in Ghidra](https://blog.trailofbits.com/2024/02/07/binary-type-inference-in-ghidra/) - BTIGhidra inter-procedural analysis approach
- [Type Inference for Decompiled Code](https://www.binarly.io/blog/type-inference-for-decompiled-code-from-hidden-semantics-to-structured-insights) - Binarly's type inference framework
- [TRex: Practical Type Reconstruction](https://www.andrew.cmu.edu/user/bparno/papers/trex.pdf) - Lattice-based typing for binary code
- [Reconstruction of Composite Types for Decompilation](https://www.researchgate.net/publication/220703660_Reconstruction_of_Composite_Types_for_Decompilation) - Struct field recovery techniques

### Tertiary (LOW confidence)
- [STRIDE: Simple Type Recognition](https://arxiv.org/html/2407.02733v1) - ML-based type inference (non-neural faster than transformers)
- [Learning Type Inference for Enhanced Dataflow Analysis](https://arxiv.org/abs/2310.00673) - CodeTIDAL5 transformer model (71.27% accuracy)
- [Method of Type Inference Based on Dataflow Analysis](https://ieeexplore.ieee.org/document/5362985) - Academic hierarchical lattice approach

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All components exist in codebase, verified by reading source
- Architecture: MEDIUM - Flow understood but integration gaps exist (stack_lifter → type_inference → variables)
- Pitfalls: HIGH - Identified from actual Phase 6 failures (Pattern 2) and code review

**Research date:** 2026-01-18
**Valid until:** 2026-02-17 (30 days - type inference approaches are stable)

**Key findings for planning:**
1. Type inference engine exists and is sophisticated - don't rebuild it
2. Gap is in stack_lifter.py initial type assignment - fix at source
3. Integration points are clear: SSA construction → type inference → declaration generation
4. Phase 6 Pattern 2 is the validation test - must fix those specific type mismatches
5. Headers database provides ground truth for 700+ functions - leverage this
6. save_info section contains original variable names - highest priority source
