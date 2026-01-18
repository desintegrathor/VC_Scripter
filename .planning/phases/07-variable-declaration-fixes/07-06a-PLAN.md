---
phase: 07-variable-declaration-fixes
plan: 06a
type: execute
wave: 5
depends_on: [07-02, 07-05]
files_modified:
  - vcdecomp/core/ir/structure/orchestrator.py
  - vcdecomp/core/ir/type_inference.py
autonomous: true

must_haves:
  truths:
    - "Function signatures show correct parameter types from type inference"
    - "Parameter names sourced from save_info debug symbols when available"
    - "Function return types inferred from return statement analysis"
  artifacts:
    - path: "vcdecomp/core/ir/structure/orchestrator.py"
      provides: "Function signature generation from SSA function"
      contains: "_generate_function_signature"
    - path: "vcdecomp/core/ir/type_inference.py"
      provides: "Parameter type inference from function entry"
      contains: "infer_parameter_types"
  key_links:
    - from: "orchestrator.py"
      to: "type_inference.infer_parameter_types"
      via: "Query parameter types before signature generation"
      pattern: "infer_parameter_types\\("
    - from: "orchestrator.py"
      to: "save_info.parameters"
      via: "Parameter names from debug symbols"
      pattern: "save_info.*parameters"
---

<objective>
Reconstruct function signatures with correct parameter types and names.

Purpose: Function signatures currently use generic types (int param_0, int param_1). This plan implements parameter type inference from type_inference results and parameter naming from save_info debug symbols.

Output: Semantic function signatures (void process_node(c_Node* node, float damage)) instead of generic (int func_0010(int param_0, int param_1)).
</objective>

<execution_context>
@C:\Users\flori\.claude\get-shit-done\workflows\execute-plan.md
@C:\Users\flori\.claude\get-shit-done\templates\summary.md
</execution_context>

<context>
@C:\Users\flori\source\repos\VC_Scripter\.planning\PROJECT.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\ROADMAP.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\STATE.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-CONTEXT.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-RESEARCH.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-02-SUMMARY.md
@C:\Users\flori\source\repos\VC_Scripter\.planning\phases\07-variable-declaration-fixes\07-05-SUMMARY.md
@C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\structure\orchestrator.py
@C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\type_inference.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Implement parameter type inference in type_inference.py</name>
  <files>vcdecomp/core/ir/type_inference.py</files>
  <action>
Add parameter type inference to TypeInferenceEngine:

1. Create method: infer_parameter_types(ssa_func: SSAFunction) → List[ParamInfo]
   ```python
   @dataclass
   class ParamInfo:
       index: int        # Parameter position (0, 1, 2...)
       name: str         # Parameter name (from save_info or "param_N")
       type: str         # Inferred C type ("float", "c_Node*", etc.)
       confidence: float # Type inference confidence

   def infer_parameter_types(self, ssa_func: SSAFunction) -> List[ParamInfo]:
       """Infer parameter types from function entry and usage patterns."""
   ```

2. Extract parameter evidence from SSA function entry:
   ```python
   # Parameters are the initial SSA values in entry block
   entry_block = ssa_func.blocks[0]
   param_values = [v for v in entry_block.values if v.is_parameter]

   param_types = []
   for idx, param_value in enumerate(param_values):
       # Use existing type inference on parameter value
       inferred_type = self.infer_types().get(param_value.name, 'int')

       param_types.append(ParamInfo(
           index=idx,
           name=param_value.name,  # Will override with save_info later
           type=inferred_type,
           confidence=self._get_confidence(param_value)
       ))
   ```

3. Enhance with usage analysis:
   ```python
   # If param_0 passed to SC_NOD_Get(c_Node*), then param_0 is c_Node*
   # If param_1 used in FADD, then param_1 is float

   for inst in ssa_func.instructions:
       if inst.mnemonic == 'XCALL':
           func_sig = self.header_db.get_function_signature(inst.xfn_name)
           if func_sig and not func_sig.get('is_variadic', False):
               for arg_idx, arg_value in enumerate(inst.inputs):
                   if arg_value.is_parameter and arg_idx < len(func_sig['parameters']):
                       expected_type = func_sig['parameters'][arg_idx][0]
                       self._add_evidence(arg_value, expected_type,
                                         confidence=0.95,
                                         source=TypeSource.FUNCTION_CALL)
   ```

4. Add return type inference:
   ```python
   def infer_return_type(self, ssa_func: SSAFunction) -> str:
       """Infer return type from return statements."""

       return_values = []
       for inst in ssa_func.instructions:
           if inst.mnemonic == 'RET' and inst.inputs:
               return_values.append(inst.inputs[0])

       if not return_values:
           return 'void'

       # Infer type from returned values
       return_types = [self.infer_types().get(v.name) for v in return_values]
       dominant_type = self._merge_types(return_types)
       return dominant_type if dominant_type else 'int'
   ```

5. Handle save_info parameter names:
   ```python
   # If save_info exists, use original parameter names
   if hasattr(ssa_func, 'save_info') and ssa_func.save_info.parameters:
       for idx, param_info in enumerate(param_types):
           if idx < len(ssa_func.save_info.parameters):
               param_info.name = ssa_func.save_info.parameters[idx].name
   ```

6. Add variadic function handling:
   ```python
   # Check if function is variadic (printf-style)
   if self.header_db.is_variadic(func_name):
       # Stop inference at last fixed parameter
       fixed_param_count = self.header_db.get_fixed_param_count(func_name)
       param_types = param_types[:fixed_param_count]
       # Add '...' to signature in orchestrator
   ```

Why this approach: Parameters are SSA values with special provenance. Type inference from usage patterns (FADD→float, XCALL argument matching) provides evidence. save_info provides original names when available. Variadic handling prevents incorrect type inference for printf-style functions.

What to avoid: Don't assume all parameters are int - use evidence. Don't skip return type - void functions are common. Don't ignore save_info - it's ground truth for names. Don't infer types for variadic args beyond fixed parameters.
  </action>
  <verify>
python -m pytest vcdecomp/tests/test_validation.py::test_decompilation_validation -v --log-cli-level=DEBUG 2>&1 | grep "Parameter type"

Log shows parameter type inference with confidence scores for each function.
  </verify>
  <done>
Parameter type inference implemented in TypeInferenceEngine. Infers types from usage patterns and function calls, with return type detection from RET instructions. Variadic function handling stops inference at last fixed parameter.
  </done>
</task>

<task type="auto">
  <name>Task 2: Generate function signatures in orchestrator</name>
  <files>vcdecomp/core/ir/structure/orchestrator.py</files>
  <action>
Update orchestrator.py to generate function signatures from type inference:

1. Locate function signature generation (likely in format_function_structured or emit logic)

2. Add signature generation method:
   ```python
   def _generate_function_signature(ssa_func: SSAFunction,
                                    type_engine: TypeInferenceEngine) -> str:
       """Generate C function signature from SSA function and type inference."""

       # Get parameter types from type inference (Plan 07-06a Task 1)
       param_types = type_engine.infer_parameter_types(ssa_func)

       # Get return type
       return_type = type_engine.infer_return_type(ssa_func)

       # Build parameter list
       params = []
       for param in param_types:
           # Format: "type name"
           params.append(f"{param.type} {param.name}")

       # Handle variadic functions
       if self.header_db.is_variadic(ssa_func.name):
           params.append("...")

       param_str = ", ".join(params) if params else "void"

       # Build full signature
       func_name = ssa_func.name or f"func_{ssa_func.address:04X}"
       signature = f"{return_type} {func_name}({param_str})"

       return signature
   ```

3. Integrate with existing signature generation:
   ```python
   # Replace existing signature generation with:
   signature = self._generate_function_signature(ssa_func, type_engine)

   # Example output:
   # Before: int func_0010(int param_0, int param_1)
   # After:  void process_node(c_Node* node, float damage)
   ```

4. Handle function naming:
   ```python
   # Priority: save_info name > address-based (func_XXXX)
   if hasattr(ssa_func, 'save_info') and ssa_func.save_info.name:
       func_name = ssa_func.save_info.name
   else:
       func_name = f"func_{ssa_func.address:04X}"
   ```

5. Add confidence annotations for uncertain signatures:
   ```python
   # If parameter type confidence < 0.70, add comment
   low_conf_params = [p for p in param_types if p.confidence < 0.70]
   if low_conf_params:
       signature += "  /* TODO: verify parameter types */"
   ```

Why this approach: Orchestrator is the coordination point where type inference results feed into code generation. Signature generation from inferred types ensures consistency with variable declarations from Plan 07-02. Variadic handling adds '...' for printf-style functions.

What to avoid: Don't hardcode signatures - derive from type inference. Don't skip void functions - return type inference handles them. Don't omit TODO comments on uncertain types.
  </action>
  <verify>
python -m pytest vcdecomp/tests/test_validation.py::test_decompilation_validation -v

Inspect .test_artifacts_07-06a/ for function signatures:
- Parameter types match usage (float for FADD operands, c_Node* for SC_NOD_Get results)
- Parameter names from save_info (test1/test2 have debug symbols)
- Return types correct (void for functions with no return value)
- Variadic functions show '...' in signature
- TODO comments on uncertain signatures

Compare test1/test2/test3 function signatures vs generic "int func_XXXX(int param_0)"
  </verify>
  <done>
Function signature generation integrated with type inference. Decompiled output shows semantic signatures with correct parameter types/names, return types, and variadic function handling.
  </done>
</task>

</tasks>

<verification>
Overall phase checks:

1. Parameter types inferred from type_inference results
2. Parameter names sourced from save_info when available
3. Return types inferred from RET instruction analysis
4. Variadic functions handled with '...' in signature
5. Function signatures generated in orchestrator before code emission
</verification>

<success_criteria>
Measurable completion:

1. Parameter type inference logs show type detection for each function
2. Function signatures show semantic types (not all "int param_0")
3. save_info parameter names appear in test1/test2 output
4. Return types correct (void for no-return functions, typed for return statements)
5. Variadic functions (if any) show '...' in signature with correct fixed param count
</success_criteria>

<output>
After completion, create `.planning/phases/07-variable-declaration-fixes/07-06a-SUMMARY.md`
</output>
