# Phase 7: Variable Declaration Fixes - Context

**Gathered:** 2026-01-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Correct variable and type declaration generation for local variables, global variables, arrays, struct field access, and function parameters. The decompiler must reconstruct semantic types from low-level bytecode, moving beyond generic `dword` types to proper C type declarations that match the original source code.

This phase focuses on type inference, scope detection, array reconstruction, and struct field naming. It does NOT include new validation features, control flow fixes, or expression reconstruction (those are other phases).

</domain>

<decisions>
## Implementation Decisions

### Type Inference Strategy
- **Hybrid approach:** Opcode-based inference first (IADD→int, FADD→float), then name pattern heuristics (vec→s_SC_vector, enum_→enum)
- **External headers required:** Use sc_global.h and sc_def.h as foundational type databases
- **Additional headers:** Support optional headers in vcdecomp/compiler/inc/ folder (script-specific includes)
- **Scripting SDK integration:** Use original-resources/Scripting_SDK.txt for comprehensive function signatures and conventions
- **Dataflow propagation:** Full dataflow analysis - propagate types through assignments and function calls (if x = SC_NOD_Get() and SC_NOD_Get returns c_Node*, then x is c_Node*)
- **Ambiguity handling:** Add TODO comments when type inference fails, with goal of zero unknown types at end (/* TODO: infer type from context */)

### Global vs Local Detection
- **Detection method:** Hybrid approach - use GADR/LADR opcodes combined with data segment validation
- **Global variable naming:** Conditional - use debug symbols when present (test1/test2), generate synthetic names (data_X) otherwise
- **Declaration placement:** Top of file before all functions (traditional C style)
- **Local scope:** Function-level scope - declare all local variables at function start (C89 style, matches original compiler)

### Array Reconstruction
- **Detection method:** Hybrid - both index pattern analysis (array[i] access) and memory layout analysis (contiguous allocations)
- **Dimension calculation:** Exact size from memory allocation (stack/data segment size ÷ element size)
- **Multi-dimensional arrays:** Yes - detect 2D/3D arrays and reconstruct as arr[x][y][z] from nested indexing patterns (arr[i*width + j] → arr[i][j])
- **Uncertain bounds:** Use conservative size with TODO comment (e.g., arr[MAX_OBSERVED*2] /* TODO: verify array size */)

### Struct Field Naming
- **Field name source:** Hybrid - lookup struct type in headers (sc_def.h) first, fall back to generic names (field_0, field_4) when type unknown
- **Type inference:** Yes - pattern matching on field accesses (if .x, .y, .z at offsets 0,4,8 → likely s_SC_vector)
- **Nested access:** Full chain with arrow operators (obj->node->pos->x) for readability and semantic accuracy
- **Pointer vs direct:** Yes - infer from addressing mode (indirect addressing → pointer syntax obj->field, direct → obj.field)

### Claude's Discretion
- Header database implementation details (caching, parsing strategy)
- Exact heuristics for name pattern matching (regex vs string matching)
- Performance optimization for dataflow analysis
- Error message formatting for TODO comments

</decisions>

<specifics>
## Specific Ideas

- **Goal:** Zero unknown types at the end - the decompiler should be sophisticated enough to infer all types correctly
- **Header locations:**
  - Core headers: vcdecomp/compiler/inc/sc_global.h, sc_def.h
  - Optional headers: vcdecomp/compiler/inc/*.h (script-specific)
  - Documentation: original-resources/Scripting_SDK.txt (comprehensive reference)
- **Type propagation example:** If SC_NOD_Get() returns c_Node* (from header), and x = SC_NOD_Get(), then x should be declared as c_Node* (not dword)
- **Array example:** arr[i*width + j] bytecode pattern should reconstruct as arr[i][j] with proper 2D declaration
- **Struct inference example:** Access pattern .x, .y, .z at offsets 0, 4, 8 → recognize as s_SC_vector type

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope

</deferred>

---

*Phase: 07-variable-declaration-fixes*
*Context gathered: 2026-01-18*
